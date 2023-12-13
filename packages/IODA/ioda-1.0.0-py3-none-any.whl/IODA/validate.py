import argparse
import os
from typing import Optional, Tuple

import torch
from numpy import savetxt
from nvidia.dali.plugin.base_iterator import LastBatchPolicy
from nvidia.dali.plugin.pytorch import DALIGenericIterator
from torch.utils.tensorboard import SummaryWriter
from tqdm import tqdm

import IODA.dali_pipeline
import IODA.utils


def validate(
    model: torch.nn.Module,
    image_size: Tuple[int, int],
    args: argparse.Namespace,
    log: Optional[SummaryWriter] = None,
) -> None:
    model.eval()

    local_rank = int(os.environ["LOCAL_RANK"])
    local_world_size = int(os.environ["LOCAL_WORLD_SIZE"])
    file_list_val = args.val
    sequence_length = args.sequence_length
    stride = args.stride
    step = args.step
    batch_size = args.batch_size
    workers = args.workers
    out = args.out

    print("Starting validation") if local_rank == 0 else None

    dali_iter = DALIGenericIterator(
        IODA.dali_pipeline.dali_video_pipe(
            file_list=file_list_val,
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
        last_batch_padded=False,
        last_batch_policy=LastBatchPolicy.FILL,
    )

    i_j_ytrue_ypred = torch.tensor((), dtype=torch.int64).to(local_rank)
    model.eval()

    disable_pbar = False if local_rank == 0 else True

    with torch.no_grad():
        for data in tqdm(
            dali_iter,
            leave=False,
            disable=disable_pbar,
        ):
            x, y, i = data[0]["data"], data[0]["labels"], data[0]["frames"]
            _y = torch.topk(torch.nn.functional.softmax(model(x), 1), k=1)[1]

            # Keeping track of frame number (i), labels (y), prediction (_y)
            _i_ytrue_ypred = torch.cat(
                (
                    i.view(-1, 1),
                    y.view(-1, 1),
                    _y.view(-1, 1),
                ),
                1,
            )
            i_j_ytrue_ypred = torch.cat((i_j_ytrue_ypred, _i_ytrue_ypred), 0)

    i_j_ytrue_ypred = IODA.utils.log_validate(i_j_ytrue_ypred, log)
    if i_j_ytrue_ypred is not None:
        savetxt(os.path.join(out, "prediction_gpu.txt"), i_j_ytrue_ypred, fmt="%i")
