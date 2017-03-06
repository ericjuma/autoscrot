import os
import tqdm


def record(record_dir='~/.autoscrot', speed=1.0):
    print(locals())


def export(record_dir='~/.autoscrot', output_file='output.mp4'):
    print(locals())


def status(record_dir='~/.autoscrot'):
    print(locals())


def clear(record_dir='~/.autoscrot'):
    for filename in tqdm(os.listdir(record_dir)):
        if filename[:10] == 'autoscrot.' and filename[-4:] == '.png':
            os.remove(filename)
