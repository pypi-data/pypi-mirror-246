import os
import pathlib
from typing import Tuple

import torch

from IODA.args import parse_validation


def save_checkpoint(
    filename: str,
    epoch: int,
    model: torch.nn.Module,
    optimizer: torch.optim.Optimizer,
    loss_fn: torch.nn.Module,
) -> None:
    """Saves a torch model and everything necessary for restarting a training.
    ----------
    epoch: int
        Fully trained epochs
    """
    pathlib.Path(filename).parent.mkdir(parents=True, exist_ok=True)
    torch.save(
        {
            "epoch": epoch,
            "model_state_dict": model.state_dict(),
            "optimizer_state_dict": optimizer.state_dict(),
            "loss": loss_fn,
        },
        filename,
    )


def load_checkpoint(
    filename: str, model: torch.nn.Module, optimizer: torch.optim.Optimizer
) -> Tuple[torch.nn.Module, int]:
    checkpoint = torch.load(filename)
    optimizer.load_state_dict(checkpoint["optimizer_state_dict"])
    model.load_state_dict(checkpoint["model_state_dict"])

    return (checkpoint["loss"], checkpoint["epoch"])


def resume_if_possible(
    model: torch.nn.Module, optimizer: torch.optim.Optimizer, loss_fn: torch.nn.Module
) -> Tuple[torch.nn.Module, int]:
    local_rank = int(os.environ["LOCAL_RANK"])
    args = parse_validation()

    if pathlib.Path(args.checkpoint).is_file():
        loss_fn, epoch = load_checkpoint(args.checkpoint, model, optimizer)
        if local_rank == 0:
            print("\nResuming from previous iteration!")
            print("Starting epoch {}\n".format(epoch + 1))
    else:
        epoch = 0

    return loss_fn, epoch
