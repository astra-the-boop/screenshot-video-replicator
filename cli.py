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
        "--recordtime", "-t",
        type=int,
        default=30,
        help="time recording in seconds",
    )

    parser.add_argument(
        "--outputdir", "-o",
        default="output.mp4",
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
        "--norecord", "-rc",
        action="store_false",
        default=True,
        help="Whether or not to record video frames (store false)",
    )

    parser.add_argument(
        "--norender", "-rn",
        action="store_false",
        default=True,
        help="Whether or not to render the video (store false)",
    )

    parser.add_argument(
        "--nodelprev", "-nd",
        action="store_false",
        default=True,
        help="Whether or not to delete previous screenshots (store false)",
    )

    parser.add_argument(
        "--fps", "-f",
        type=int,
        default=10,
        help="frames per second"
    )

    args = parser.parse_args()
    if args.norecord:
        print("A")
        thingy.record(args.recordtime, remove=args.nodelprev)
    if args.norender:
        print("B")
        thingy.renderFrames(args.inputdir, args.fps)
        thingy.render(args.fps, args.outputdir)

if __name__ == "__main__":
    cli()