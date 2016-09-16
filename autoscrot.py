#! /usr/bin/env python
import os, time, datetime, sys

script, task_choice, timing_rate = sys.argv
timing_rate = float(timing_rate)
inv_fps = 1.0 / timing_rate
autoscrot_dir = os.path.expanduser('~') + '/.autoscrot'

def record_screen():
    os.system('clear')
    print "starting screenshots"
    while True:
        scrot_filename = str(datetime.datetime.now()).replace(" ", "...")
        record_command = "scrot -q 75 -e 'mv $f {}/scrots' '{}'.jpg".format(autoscrot_dir, scrot_filename)
        os.system(record_command)
        os.system('clear')
        print record_command
        print str(len([name for name in os.listdir(autoscrot_dir + '/scrots')])) + " files in directory"
        time.sleep(inv_fps)

def compile_scrots():
    os.system('clear')
    print "compiling screenshots..."
    compile_file_name = str(datetime.datetime.now().strftime("%Y-%m-%d...%H:%M")) + ".avi"
    command_base = "mencoder 'mf://{}/scrots/*.jpg' -ovc x264 -mf fps={} -o {}/vids/{}"
    compile_command = command_base.format(autoscrot_dir, timing_rate, autoscrot_dir, compile_file_name)
    print compile_command
    os.system(compile_command)
    clear_dir()
    open_ranger_cmd = "ranger --selectfile={}/vids/{}".format(autoscrot_dir, compile_file_name)
    os.system(open_ranger_cmd)
    print "old scrots cleared"

def clear_dir():
    clear_dir_cmd = "rm -f {}/scrots/*.jpg".format(autoscrot_dir)
    os.system(clear_dir_cmd)
    print "{} cleared".format(autoscrot_dir + "/scrots")

print 'Welcome to autoscrot by Eric Juma\n'
if task_choice == 'r':
    record_screen()
elif task_choice == 'e':
    compile_scrots()
elif task_choice == 'c':
    clear_dir()
else:
    print "argument {} not accepted".format(task_choice)
