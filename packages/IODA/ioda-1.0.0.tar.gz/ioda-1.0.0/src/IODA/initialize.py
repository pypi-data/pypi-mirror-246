import argparse
from typing import Tuple

import torch

import IODA.lstm_alexnet


def initialize(
    args: argparse.Namespace,
) -> Tuple[torch.nn.Module, torch.optim.Optimizer, torch.nn.Module, Tuple[int, int]]:

    weights = (
        torch.tensor(args.class_weights) if args.class_weights is not None else None
    )

    return IODA.lstm_alexnet.initialize(
        batch_size=args.batch_size,
        num_classes=args.num_classes,
        weights=weights,
        transfer_learning=args.transfer_learning,
    )
