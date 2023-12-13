from typing import Tuple, Union

import nvidia.dali.fn as fn
import nvidia.dali.types as types
from nvidia.dali.pipeline import Pipeline, pipeline_def


@pipeline_def
def dali_video_pipe(
    file_list: str,
    image_size: Tuple[int, int],
    sequence_length: int,
    stride: int,
    step: int,
    num_gpus: int,
) -> Pipeline:
    """Creates a sharded nvidia-dali pipeline with encoding on the gpu.
    Parameters
    ----------
    file_list : str
        Path to file list with layout: file label [start_frame [end_frame]].
    image_size : tuple
        Images are resized to these dimensions.
    step: int
        Load every n-th frame.
    num_gpus: int
        Total number of gpus spawned.

    Returns
    -------
    nvidia-dali.Pipeline
        Sharded pipeline that automatically controls data sharding to each gpu."""

    shard_id = Pipeline.current().device_id

    images, labels, frames = fn.readers.video_resize(
        device="gpu",
        sequence_length=sequence_length,
        file_list=file_list,
        enable_frame_num=True,
        file_list_frame_num=True,
        file_list_include_preceding_frame=True,  # Just to silence the future warning.
        name="Reader",
        size=image_size,
        stride=stride,
        step=step,
        shard_id=shard_id,
        num_shards=num_gpus,
        pad_sequences=True,  # Allows incomplete sequences. Redundant frames are zero and frame number -1.
        dtype=types.DALIDataType.FLOAT,
        interp_type=types.INTERP_TRIANGULAR,  # good performance and results for downscaling
        normalized=True,  # pixel values: [0,1]
    )
    # Output layout of video reader [N,F,H,W,C]
    # N -batch size, F - sequence length, H - height, W - width, C - Color channels
    # Layout for torchvision [C,H,W]
    # Mean and std are the standard values for alexnet, resnet etc.
    if sequence_length == 1:
        images = fn.squeeze(images, axes=0)
        output_layout = "CHW"
    else:
        output_layout = "FCHW"

    images = fn.crop_mirror_normalize(
        images,
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225],
        output_layout=output_layout,
    )

    return images, labels, frames


@pipeline_def
def dali_single_video_pipe(
    filenames: Union[str, list[str]],
    image_size: Tuple[int, int],
    sequence_length: int,
    stride: int,
    step: int,
    num_gpus: int,
) -> Pipeline:
    """Creates a sharded nvidia-dali pipeline with encoding on the gpu.
    Parameters
    ----------
    file_names : str
        String or list of string of video files to load.
    image_size : tuple
        Images are resized to these dimensions.
    step: int
        Load every n-th frame.
    num_gpus: int
        Total number of gpus spawned.

    Returns
    -------
    nvidia-dali.Pipeline
        Sharded pipeline that automatically controls data sharding to each gpu."""

    shard_id = Pipeline.current().device_id

    images, _, frames = fn.readers.video_resize(
        device="gpu",
        sequence_length=sequence_length,
        filenames=filenames,
        enable_frame_num=True,
        labels=0,
        file_list_include_preceding_frame=True,  # Just to silence the future warning.
        name="Reader",
        size=image_size,
        stride=stride,
        step=step,
        shard_id=shard_id,
        num_shards=num_gpus,
        pad_sequences=True,  # Allows incomplete sequences. Redundant frames are zero and frame number -1.
        dtype=types.DALIDataType.FLOAT,
        interp_type=types.INTERP_TRIANGULAR,  # good performance and results for downscaling
        normalized=True,  # pixel values: [0,1]
    )
    # Output layout of video reader [N,F,H,W,C]
    # N -batch size, F - sequence length, H - height, W - width, C - Color channels
    # Layout for torchvision [C,H,W]
    # Mean and std are the standard values for alexnet, resnet etc.
    if sequence_length == 1:
        images = fn.squeeze(images, axes=0)
        output_layout = "CHW"
    else:
        output_layout = "FCHW"

    images = fn.crop_mirror_normalize(
        images,
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225],
        output_layout=output_layout,
    )

    return images, frames
