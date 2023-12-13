import argparse
import os
from typing import Optional, Tuple

import torch
from nvidia.dali.plugin.base_iterator import LastBatchPolicy
from nvidia.dali.plugin.pytorch import DALIGenericIterator
from torch.utils.tensorboard import SummaryWriter
from tqdm import tqdm, trange

import IODA.dali_pipeline
import IODA.resume
import IODA.utils


def train(
    model: torch.nn.Module,
    optimizer: torch.optim.Optimizer,
    loss_fn: torch.nn.Module,
    epoch_start: int,
    image_size: Tuple[int, int],
    args: argparse.Namespace,
    log: Optional[SummaryWriter] = None,
) -> None:
    """
    Parameters
    ----------
    epoch: int
        Epoch to start in case of resuming from a previous run.

    """
    model.train()

    # Automatically select the fastest cudnn backend
    torch.backends.cudnn.benchmark = True

    local_rank = int(os.environ["LOCAL_RANK"])
    local_world_size = int(os.environ["LOCAL_WORLD_SIZE"])
    file_list_train = args.train
    sequence_length = args.sequence_length
    stride = args.stride
    step = args.step
    batch_size = args.batch_size
    workers = args.workers
    epochs = args.epochs - epoch_start
    checkpoint = args.checkpoint

    if local_rank == 0 and epochs == 0:
        "Training is skipped since model is already fully trained"
    elif local_rank == 0:
        "Starting training"

    scaler = torch.cuda.amp.grad_scaler.GradScaler()

    dali_iter = DALIGenericIterator(
        IODA.dali_pipeline.dali_video_pipe(
            file_list=file_list_train,
            image_size=image_size,
            sequence_length=sequence_length,
            stride=stride,
            step=step,
            device_id=local_rank,
            num_gpus=local_world_size,
            batch_size=batch_size,
            num_threads=workers,
        ),
        ["data", "labels", "frames"],
        reader_name="Reader",
        auto_reset=True,
        last_batch_padded=False,
        last_batch_policy=LastBatchPolicy.FILL,
    )

    disable_pbar = False if local_rank == 0 else True

    for epoch in trange(epochs, desc="Epochs", disable=disable_pbar):
        # Logging for tensorboard
        losses = []
        targets = []
        predictions = []

        for it in (
            pbar := tqdm(
                dali_iter,
                leave=False,
                disable=disable_pbar,
            )
        ):
            optimizer.zero_grad()
            with torch.cuda.amp.autocast_mode.autocast():  # Mixed precision
                pred = model(it[0]["data"])
                loss = loss_fn(pred, it[0]["labels"].long().view(-1))
            scaler.scale(loss).backward()
            scaler.step(optimizer)
            scaler.update()

            pbar.set_description("Loss: {:.8f}".format(loss))

            if log is not None:
                predictions.append(
                    torch.topk(torch.nn.functional.softmax(pred, 1), k=1)[1].view(-1)
                )
                losses.append(loss.view(1))
                targets.append(it[0]["labels"].view(-1))

        torch.distributed.barrier()

        # All processes should see same parameters as they all start from same
        # random parameters and gradients are synchronized in backward passes.
        # Therefore, saving it in one process is sufficient.
        if local_rank == 0:
            IODA.resume.save_checkpoint(
                checkpoint, epoch + 1, model, optimizer, loss_fn
            )

        if log is not None:
            IODA.utils.log_train(
                torch.cat(targets),
                torch.cat(predictions),
                torch.cat(losses),
                epoch,
                log,
            )
