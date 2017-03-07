import os
from tqdm import tqdm
from glob import glob
import difflib
import time
import filecmp


def expand_path(path):
    """Takes a path and returns the absolute path using expanduser and realpath"""
    return os.path.realpath(os.path.expanduser(path))


def scrot_file_path(record_dir, n):
    return os.path.join(expand_path(bytes(record_dir, encoding='utf-8')),
                        bytes("{}.autoscrot.png".format(n), encoding='utf-8'))


def get_scrotnum(scrot):
    return int(os.path.split(scrot)[1][:-14])


def record(record_dir="~/.autoscrot", speed=60):
    scrots = glob(os.path.join(expand_path(record_dir), "*.autoscrot.png"))
    scrotnum = max([get_scrotnum(i) for i in scrots]) if scrots else 0
    while True:
        if scrotnum > 1:
            oneback_path = scrot_file_path(record_dir, scrotnum - 1)
            twoback_path = scrot_file_path(record_dir, scrotnum - 2)
            with open(oneback_path, 'r+b') as oneback, open(twoback_path, 'r+b') as twoback:
                if oneback.read() == twoback.read():
                    os.remove(oneback_path)
                    scrotnum -= 1

        scrot_path = scrot_file_path(record_dir, scrotnum)
        print(scrot_path)
        os.system(b"screencapture -Cmx " + scrot_path)
        time.sleep(speed / 30)
        scrotnum += 1


def export(record_dir="~/.autoscrot", output_file="output.mp4"):
    record_dir = expand_path(record_dir)
    output_file = expand_path(output_file)
    command = "ffmpeg -y -framerate 30 -i {}/{}.autoscrot.png -c:v libx264 -pix_fmt yuv420p {}"
    os.system(command.format(record_dir, '%d', output_file))


def status(record_dir="~/.autoscrot"):
    record_dir = expand_path(record_dir)
    scrots = glob(os.path.join(record_dir, "*.autoscrot.png"))
    print("{} autoscrot files in recording directory {}".format(len(scrots), record_dir))


def clear(record_dir="~/.autoscrot"):
    record_dir = expand_path(record_dir)
    scrots = glob(os.path.join(record_dir, b"*.autoscrot.png"))
    for f in tqdm(scrots):
        os.remove(f)
