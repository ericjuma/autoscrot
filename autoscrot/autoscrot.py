import argparse
import helpers


def positive_float(n):
    try:
        n = float(n)
        assert(n > 0)
    except (AssertionError, ValueError):
        raise argparse.ArgumentTypeError("{} is not a positive float.".format(n))
    return n


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
    '--recorddir',
    default='~/.autoscrot',
    help='Path to recording directory to record in')

export_subparser = subparsers.add_parser(
    'export',
    help='Export recorded data to video file.')
export_subparser.add_argument(
    'file',
    default='output.mp4',
    help='Output file path')
export_subparser.add_argument(
    '--recorddir',
    default='~/.autoscrot',
    help='Path to recording directory to export from')

status_subparser = subparsers.add_parser(
    'status',
    help='Get info on the recorded data.')
status_subparser.add_argument(
    '--recorddir',
    default='~/.autoscrot',
    help='Path to recording directory to get info on')

clear_subparser = subparsers.add_parser(
    'clear',
    help='Clear recording data when done with it (does not clear exported video)')
clear_subparser.add_argument(
    '--recorddir',
    default='~/.autoscrot',
    help='Path to recording directory to clear of recorded data')

parser.parse_args()
