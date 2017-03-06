import os
from tqdm import tqdm
from glob import glob


def real_real_path(path):
    """Takes a path and returns the absolute path using expanduser and realpath"""
    return os.path.realpath(os.path.expanduser(path))


def record(record_dir='~/.autoscrot', speed=1.0):
    print(locals())


def export(record_dir='~/.autoscrot', output_file='output.mp4'):
    print(locals())


def status(record_dir='~/.autoscrot'):
    record_dir = real_real_path(record_dir)
    scrots = glob(os.path.join(record_dir, "autoscrot.*.png"))
    print("{} autoscrot files in recording directory {}".format(len(scrots), record_dir))


def clear(record_dir='~/.autoscrot'):
    record_dir = real_real_path(record_dir)
    scrots = glob(os.path.join(record_dir, "autoscrot.*.png"))
    for f in tqdm(scrots):
        os.remove(f)
