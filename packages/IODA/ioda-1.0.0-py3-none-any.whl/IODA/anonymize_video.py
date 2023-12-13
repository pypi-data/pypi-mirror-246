import argparse
import os
import subprocess
from typing import Union

import torch
from nvidia.dali.plugin.base_iterator import LastBatchPolicy
from nvidia.dali.plugin.pytorch import DALIGenericIterator
from torch.nn.parallel import DistributedDataParallel as DDP
from tqdm import tqdm

import IODA.dali_pipeline
import IODA.format_net_output
from IODA.args import parse_anonymize
from IODA.lstm_alexnet import LSTMAlexNet
from IODA.utils import gather

# Important: For this configuration to work, the script needs to be spawned by torchrun!
# For command line arguments, see args.py


def IODA_algo(args: argparse.Namespace) -> Union[torch.Tensor, None]:
    """
    Takes a video file as input, anonymizes version it using IODA
    and writes the results to disk. Requires an NVIDA gpu.
    The inputs are defined by command line arguments. See also parse_anonymize.
    """
    local_rank = int(os.environ["LOCAL_RANK"])
    model = LSTMAlexNet(
        num_classes=args.num_classes,
        lstm_size=args.batch_size,
        transfer_learning=True,
    )
    model = DDP(model.to(local_rank), device_ids=[local_rank], output_device=local_rank)
    model.load_state_dict(torch.load(args.model)["model_state_dict"])

    local_rank = int(os.environ["LOCAL_RANK"])
    local_world_size = int(os.environ["LOCAL_WORLD_SIZE"])
    filename = args.i
    sequence_length = args.sequence_length
    stride = args.stride
    step = args.step
    batch_size = args.batch_size
    workers = args.workers

    dali_iter = DALIGenericIterator(
        IODA.dali_pipeline.dali_single_video_pipe(
            filenames=filename,
            image_size=(224, 224),
            sequence_length=sequence_length,
            stride=stride,
            step=step,
            device_id=local_rank,
            num_gpus=local_world_size,
            batch_size=batch_size,
            num_threads=workers,
        ),
        ["data", "frames"],
        reader_name="Reader",
        last_batch_padded=False,
        last_batch_policy=LastBatchPolicy.FILL,
    )

    pred = torch.tensor((), dtype=torch.int64).to(local_rank)
    model.eval()

    disable_pbar = False if local_rank == 0 else True

    with torch.no_grad():
        for data in tqdm(
            dali_iter,
            leave=False,
            disable=disable_pbar,
        ):
            x, i = data[0]["data"], data[0]["frames"]
            _y = torch.topk(torch.nn.functional.softmax(model(x), 1), k=1)[1]

            # Keeping track of frame number (i), prediction (_y)
            i_y = torch.cat(
                (
                    i.view(-1, 1),
                    _y.view(-1, 1),
                ),
                1,
            )

            pred = torch.cat((pred, i_y), 0)

    return gather(pred)


def main():

    local_rank = int(os.environ["LOCAL_RANK"])
    args = parse_anonymize()

    print("Analyzing video") if local_rank == 0 else None

    torch.distributed.init_process_group(backend="nccl")
    outside_frames = IODA_algo(args)

    if local_rank == 0:
        print("Deanonymization")

        outside_frames = IODA.format_net_output.format(outside_frames.cpu().numpy())

        enable_str = ""

        for i in range(outside_frames.shape[0]):
            start = outside_frames[i, 0]
            stop = outside_frames[i, 1]
            enable_str += "between(n,%i,%i)+" % (start, stop)

        # Removes last + sign
        enable_str = enable_str[:-1]

        command = [
            "ffmpeg",
            "-n",
            "-loglevel",
            "error",
            "-stats",
            "-hwaccel",
            "cuda",
            "-hwaccel_output_format",
            "cuda",
            "-i",
            args.i,
            "-vf",
            "drawbox=t=fill:c=black:enable='" + enable_str + "'",
            "-c:a",
            "copy",
            args.o,
        ]

        print(command)
        subprocess.run(command)


if __name__ == "__main__":
    main()
