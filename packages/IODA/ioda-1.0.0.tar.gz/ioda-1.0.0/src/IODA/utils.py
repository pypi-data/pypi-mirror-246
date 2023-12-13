import os
from typing import Optional, Union

import numpy as np
import torch
from sklearn.metrics import precision_recall_fscore_support
from torch.utils.tensorboard import SummaryWriter


def gather(tensor: torch.Tensor) -> Optional[torch.Tensor]:
    """
    Gather torch tensors from all processes spawn by torchrun
    and return the result in the local rank with number 0.
    """
    local_rank = int(os.environ["LOCAL_RANK"])
    world_size = int(os.environ["WORLD_SIZE"])

    tensor_list = (
        [torch.ones_like(tensor, device=local_rank) for _ in range(world_size)]
        if local_rank == 0
        else None
    )
    torch.distributed.gather(tensor, tensor_list)

    if local_rank == 0:
        return torch.cat(tensor_list)
    else:
        return None


def log_train(
    targets: torch.Tensor,
    predictions: torch.Tensor,
    losses: torch.Tensor,
    epoch: int,
    log: SummaryWriter,
) -> None:
    """
    Log training data of a DALI pipeline to be shown with tensorboard.
    """
    # We assume that all tensors across machines have the same shape,
    # which is generally true for a DALI pipeline.
    targets_all = gather(targets)
    predictions_all = gather(predictions)
    losses_all = gather(losses)

    if int(os.environ["LOCAL_RANK"]) == 0:
        prec, rec, f1, _ = precision_recall_fscore_support(
            targets_all.cpu().detach().numpy(),
            predictions_all.cpu().detach().numpy(),
            average="weighted",
            zero_division=0,
        )

        log.add_scalar(
            "train/Loss", np.mean(losses_all.cpu().detach().numpy()), global_step=epoch
        )
        log.add_scalar("train/Precision", prec, global_step=epoch)
        log.add_scalar("train/Recall", rec, global_step=epoch)
        log.add_scalar("train/F1-Score", f1, global_step=epoch)


def log_validate(
    i_ytrue_ypred: torch.Tensor, log: Optional[SummaryWriter]
) -> Optional[torch.Tensor]:
    """
    Log validation data of a DALI pipeline to be shown with tensorboard.
    """
    # We assume that all tensors across machines have the same shape,
    # which is generally true for a DALI pipeline.
    i_ytrue_ypred_all = gather(i_ytrue_ypred)

    if int(os.environ["LOCAL_RANK"]) == 0:
        i_ytrue_ypred_all = i_ytrue_ypred_all.cpu().detach().numpy()

        prec, rec, f1, _ = precision_recall_fscore_support(
            i_ytrue_ypred_all[:, 2],
            i_ytrue_ypred_all[:, 1],
            average="weighted",
            zero_division=0,
        )

        log.add_scalar("test/Precision", prec)
        log.add_scalar("test/Recall", rec)
        log.add_scalar("test/F1-Score", f1)

        # Also sort and save predictions as text file
        result = [tuple(row) for row in i_ytrue_ypred_all]
        result = np.unique(result, axis=0)
        result = result[np.lexsort((result[:, 1], result[:, 0]))]

        return i_ytrue_ypred_all

    return None
