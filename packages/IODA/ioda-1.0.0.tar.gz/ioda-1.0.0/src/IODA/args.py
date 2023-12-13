import argparse


def parse_validation() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Training and validation of IODA")
    parser.add_argument(
        "--out",
        default="results",
        help="Path to the result folder containing the trained model and the validation results.",
    )
    parser.add_argument(
        "--checkpoint",
        default="checkpoint/model.pt",
        help="Path for storing the final model. The model checkpoints are stored here as well and get progressively overweritten. If it already exists at programm start, training is resumed from the checkpoint.",
    )
    parser.add_argument(
        "--train",
        required=True,
        help="Path to the file list containing training data with layout: file label [start_frame [end_frame]]. The annotations are assumed to be in the same folder with filename {file}_annotation.txt. Labels must index the rows in the files starting with 0! Otherwise, undefined behaviour will occur. Mutually exclusive with trained-model argument.",
    )
    parser.add_argument(
        "--val",
        required=True,
        help="Path to the file list containing validation data with layout: file label [start_frame [end_frame]].",
    )
    parser.add_argument(
        "--transfer-learning",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="If true transfer learning of the classifier layer, else training of the complete net",
    )
    parser.add_argument(
        "--num-classes",
        default=2,
        type=int,
        help="Number of classes",
    )
    parser.add_argument(
        "--class-weights",
        nargs="*",
        type=float,
        help="Optional weights for each class. Length must be equal to number of classes.",
    )
    parser.add_argument(
        "--sequence-length",
        default=1,
        type=int,
        help="Frames to load per sequence (default: 1).",
    )
    parser.add_argument(
        "--step",
        default=1,
        type=int,
        help="Step between sequences (default: 1).",
    )
    parser.add_argument(
        "--stride",
        default=1,
        type=int,
        help="Distance between consecutive frames in the sequence (default: 1).",
    )
    parser.add_argument(
        "--epochs",
        type=int,
        required=True,
        help="number of total epochs to run",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=256,
        help="Mini-batch size per process (default: 256)",
    )
    parser.add_argument(
        "--workers",
        default=4,
        type=int,
        help="Number of workers per dali pipeline",
    )

    return parser.parse_args()


def parse_anonymize() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Training and validaiton of IODA")
    parser.add_argument(
        "--i", type=str, required=True, help="Path to input video file."
    )
    parser.add_argument(
        "--o",
        required=True,
        help="Path of the resulting anonymized video file.",
    )
    parser.add_argument(
        "--model",
        type=str,
        required=True,
        help="Path to pytorch model. Exclusive with annotation option.",
    )
    parser.add_argument(
        "--sequence-length",
        default=1,
        type=int,
        help="Frames to load per sequence (default: 1).",
    )
    parser.add_argument(
        "--step",
        default=1,
        type=int,
        help="Step between sequences (default: 1).",
    )
    parser.add_argument(
        "--stride",
        default=1,
        type=int,
        help="Distance between consecutive frames in the sequence (default: 1).",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=256,
        help="Mini-batch size per process (default: 256)",
    )
    parser.add_argument(
        "--num-classes",
        default=2,
        type=int,
        help="Number of classes of the trained model",
    )
    parser.add_argument(
        "--workers",
        default=4,
        type=int,
        help="Number of workers per dali pipeline",
    )

    return parser.parse_args()
