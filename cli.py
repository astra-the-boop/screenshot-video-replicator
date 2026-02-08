import argparse
import os
import main
import thingy

def cli():
    parser = argparse.ArgumentParser(
        description="render a video from screenshots of your desktop :3",
    )

    parser.add_argument(
        "--inputdir", "-i",
        required=True,
        help="path to directory of input video",
    )

    parser.add_argument(
        "--outputdir", "-o",
        default=".",
        help="path to directory of output video",
    )

    parser.add_argument(
        "--x", "-x",
        type=int,
        default=22,
        help="vertical tile",
    )

    parser.add_argument(
        "--y", "-y",
        type=int,
        default=10,
        help="horizontal tile",
    )

    parser.add_argument(
        "--scale", "-s"
        ,type=int,
        default=10,
        help = "sharpness scale (higher = more sharp)"
    )

    parser.add_argument(
        "--norecord", "-r",
        action="store_false",
        help="Whether or not to record video frames",
    )



    args = parser.parse_args()

    os.makedirs(args.frames, exist_ok=True)

