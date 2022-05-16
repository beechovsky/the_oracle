import subprocess

import serial
import time
import os
import random
import subprocess


# connect to Arduino
serial_path = '/dev/ttyUSB0'
serial_input = serial.Serial(serial_path, 9600)  # this auto-opens the port
time.sleep(2)  # wait for Arduino, which resets when serial conn opened

# answer .movs
answer_mov_root = '../the_oracle_mov/answers/'
# look up os.expandpath
answer_movs = os.listdir(answer_mov_root)

# playing .mov files from python is ... difficult
# so, letting bash do it via vlc, which has a robust and well-documented cli:
# https://wiki.videolan.org/VLC_command-line_help/

# DRY & comply with PEP8
# --no-qt-video-autoresize --fullscreen --no-autoscale --one-instance
# vlc_bash = ' cvlc --no-video-title-show --no-interact --one-instance --fullscreen '
# mov_process = subprocess.Popen(vlc_bash.split(), stdin=subprocess.PIPE)
mov_process = subprocess.run('/bin/bash', shell=True, universal_newlines=True, stdin=subprocess.PIPE)

vlc_bash = ' vlc --no-video-title-show --no-interact --one-instance --fullscreen'
# play_sleep_bash = vlc_bash + b'--repeat ../the_oracle_mov/Sleeping.mp4'
play_sleep_bash = vlc_bash + ' --repeat ../the_oracle_mov/Sleeping.mp4\n'
# start default sleep mov, non-blocking so interference can be caught
# sleep_process = subprocess.Popen(play_sleep_bash.split())
# mov_process.stdin.write(vlc_bash + play_sleep_bash)
mov_process.communicate(play_sleep_bash)
#mov_process.stdin.write(play_sleep_bash)
#mov_process.stdin.close()
#mov_process.stdout.read()

while True:
    # since we're jumping in mid-stream, the try/except will make sure we wait for good data
    mov_process.communicate(play_sleep_bash)
    try:
        # https://pyserial.readthedocs.io/en/latest/shortintro.html#readline
        value = serial_input.readline().strip().decode("utf-8")  # format for easy digestion - '3XX'
        # debug
        print(value)
        # print(len(value))

        if len(value) is 3 and int(value) < 300:  # interference

            # terminate sleep process
            # sleep_process.terminate()  # non-blocking process only requires terminate() to stop
            # mov_process.terminate()

            # get a random idx for selecting random answer .mov
            # answer_index = random.randint(0, len(answer_movs) - 1)

            # may need  --one-instance --play-and-exit; doesn't need --playlist-enqueue as that's default behavior
            # play_answer_bash = vlc_bash + '--play-and-exit ' + answer_mov_root + answer_movs[answer_index]

            # alternate: use vlc random arg an pass the whole answer dir
            play_answer_bash = vlc_bash + '--play-and-exit --random ' + answer_mov_root

            # queue the answer .mov
            # answer_process = subprocess.Popen(play_answer_bash.split())
            # answer_process = subprocess.Popen(play_answer_bash.split(), stdout=subprocess.PIPE)
            # mov_process.stdin.write(play_answer_bash)
            # mov_process.stdin.flush()
            mov_process.communicate(play_answer_bash)

            # calling wait() on the object returned from Popen will block until it completes.
            # answer_process.wait()
            # mov_process.wait()

            # fire up sleep mov when answer vid finishes
            # sleep_process = subprocess.Popen(play_sleep_bash.split())
            # mov_process.stdin.write(play_answer_bash)
            # mov_process.stdin.flush()
            mov_process.communicate(play_sleep_bash)

            # flush buffer
            serial_input.reset_input_buffer()

    # ignore errors caused by grabbing values mid-byte and try again until we get the beginning
    except UnicodeDecodeError:
        pass
    except ValueError:
        pass
