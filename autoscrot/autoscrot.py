import argparse
import helpers


def positive_float(n):
    """For Argparse: Defines a postiive float"""
    try:
        n = float(n)
        assert(n > 0)
    except (AssertionError, ValueError):
        raise argparse.ArgumentTypeError("{} is not a positive float.".format(n))
    return n


def creatable_file(path):
    """For Argparse: Defines a file that can be created."""
    pass


def record_dir(path):
    """For Argparse: Defines a directory that has been used as the record_dir."""
    pass


def record(args):
    helpers.record(record_dir=args.record_dir, speed=args.speed)


def export(args):
    helpers.export(record_dir=args.record_dir, output_file=args.output_file)


def clear(args):
    helpers.clear(record_dir=args.record_dir)


def status(args):
    helpers.status(record_dir=args.record_dir)


parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers()

record_subparser = subparsers.add_parser(
    'record',
    help='Record screenshots to be exported. Appends to previous recordings.')
record_subparser.add_argument(
    'speed',
    type=positive_float,
    default=60,
    help='Speed multiplier for recording. Will be the speed at which the video is played.')
record_subparser.add_argument(
    '--record_dir',
    default='~/.autoscrot',
    help='Path to recording directory to record in')
record_subparser.set_defaults(func=record)

export_subparser = subparsers.add_parser(
    'export',
    help='Export recorded data to video file.')
export_subparser.add_argument(
    'output_file',
    default='output.mp4',
    help='Output file path')
export_subparser.add_argument(
    '--record_dir',
    default='~/.autoscrot',
    help='Path to recording directory to export from')
export_subparser.set_defaults(func=export)


status_subparser = subparsers.add_parser(
    'status',
    help='Get info on the recorded data.')
status_subparser.add_argument(
    '--record_dir',
    default='~/.autoscrot',
    help='Path to recording directory to get info on')
status_subparser.set_defaults(func=status)

clear_subparser = subparsers.add_parser(
    'clear',
    help='Clear recording data when done with it (does not clear exported video)')
clear_subparser.add_argument(
    '--record_dir',
    default='~/.autoscrot',
    help='Path to recording directory to clear of recorded data')
clear_subparser.set_defaults(func=clear)

args = parser.parse_args()
args.func(args)
