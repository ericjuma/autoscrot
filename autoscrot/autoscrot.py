from uuid import uuid4
import argparse
import helpers
import os


def real_real_path(path):
    """Takes a path and returns the absolute path using expanduser and realpath"""
    return os.path.realpath(os.path.expanduser(path))


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
    path = real_real_path(path)
    parent_dir = os.path.split(path)[0]
    tempfile = os.path.join(parent_dir, str(uuid4()))
    try:
        f = open(tempfile, 'w')
        os.remove(tempfile)
        f.close()
    except (FileNotFoundError, PermissionError) as e:
        raise argparse.ArgumentTypeError(
            "Files cannot be created at path {} because:\n{}".format(path, e))
    return path


def potential_record_dir(path):
    """For Argparse: Defines a directory that could be used as the record_dir."""
    path = real_real_path(path)
    tempfile = os.path.join(path, str(uuid4()))
    try:
        f = open(tempfile, 'w')
        os.remove(tempfile)
        f.close()
    except (FileNotFoundError, PermissionError, NotADirectoryError) as e:
        raise argparse.ArgumentTypeError(
            "{} cannot be used for a record directory because:\n{}.".format(path, e))
    return path


def used_record_dir(path):
    """For Argparse: Defines a directory that has been used as the record_dir."""
    path = real_real_path(path)
    try:
        assert('autoscrot.0.png' in os.listdir(path))
    except AssertionError:
        raise argparse.ArgumentTypeError("{} is not a used record directory".format(path))
    return path


def record(args):
    """Called by argparse to run helper function with arguments from args namespace"""
    helpers.record(record_dir=args.record_dir, speed=args.speed)


def export(args):
    """Called by argparse to run helper function with arguments from args namespace"""
    helpers.export(record_dir=args.record_dir, output_file=args.output_file)


def clear(args):
    """Called by argparse to run helper function with arguments from args namespace"""
    helpers.clear(record_dir=args.record_dir)


def status(args):
    """Called by argparse to run helper function with arguments from args namespace"""
    helpers.status(record_dir=args.record_dir)


# Create arg parser
parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers()

# Create subparser for record subcommand
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
    type=potential_record_dir,
    default='~/.autoscrot',
    help='Path to recording directory to record in')
record_subparser.set_defaults(func=record)

# Create subparser for export subcommand
export_subparser = subparsers.add_parser(
    'export',
    help='Export recorded data to video file.')
export_subparser.add_argument(
    'output_file',
    type=creatable_file,
    default='output.mp4',
    help='Output file path')
export_subparser.add_argument(
    '--record_dir',
    type=potential_record_dir,
    default='~/.autoscrot',
    help='Path to recording directory to export from')
export_subparser.set_defaults(func=export)

# Create subparser for status subcommand
status_subparser = subparsers.add_parser(
    'status',
    help='Get info on the recorded data.')
status_subparser.add_argument(
    '--record_dir',
    type=used_record_dir,
    default='~/.autoscrot',
    help='Path to recording directory to get info on')
status_subparser.set_defaults(func=status)

# Create subparser for clear subcommand
clear_subparser = subparsers.add_parser(
    'clear',
    help='Clear recording data when done with it (does not clear exported video)')
clear_subparser.add_argument(
    '--record_dir',
    type=used_record_dir,
    default='~/.autoscrot',
    help='Path to recording directory to clear of recorded data')
clear_subparser.set_defaults(func=clear)

# Parse args
args = parser.parse_args()

# Call corresponding function to the subcommand that was chosen.
# AttributeError was being thrown when no subcommand was chosen so in this case print help.
try:
    args.func(args)
except AttributeError:
    parser.print_help()
