#!/usr/bin/env python3
import subprocess
import time
import sys

# screen to dim
screen = sys.argv[1]
# read arguments from the run command: idel time (in seconds)
dimtime = int(sys.argv[2])*1000
# brightness when dimmed (between 0 and 255)
dimmed = sys.argv[3]
# brighness else
undimmed = sys.argv[4]

def get_cmd(cmd):
    return subprocess.Popen(["/bin/bash", "-c", cmd], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)

def set_cmd(cmd):
    subprocess.Popen(["/bin/bash", "-c", cmd], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)

get_idleTime = "dbus-send --print-reply --dest=org.gnome.Mutter.IdleMonitor /org/gnome/Mutter/IdleMonitor/Core org.gnome.Mutter.IdleMonitor.GetIdletime"
get_brightness = "brightnessctl -d " + screen + " g"
set_brightness = "brightnessctl -d " + screen + " s "

# initial state (idle time > set time)
check1 = False
oldBrightness = undimmed
set_cmd(set_brightness + oldBrightness)

while True:
    time.sleep(2)
    # get the current idle time (millisecond)
    idleTime = int((get_cmd(get_idleTime)).communicate()[0].rsplit(None,1)[-1])

    # see if idle time exceeds set time (True/False)
    check2 = idleTime > dimtime
    # compare with last state
    if check2 != check1:
        # if state chenges, define new brightness...
        newBrightness = dimmed if check2 else oldBrightness
        oldBrightness = get_cmd(get_brightness).communicate()[0].rsplit(None,1)[0]
        # ...and set it
        set_cmd(set_brightness + newBrightness)
        # set current state as initial one for the next loop cycle
        check1 = check2
