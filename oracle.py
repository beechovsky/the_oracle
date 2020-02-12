import serial
import time
import os
import random
import subprocess
import signal

# connect to Arduino
serial_path = '/dev/ttyUSB0'
serial_input = serial.Serial(serial_path, 9600)  # this auto-opens the port
time.sleep(2)  # wait for Arduino, which resets when serial conn opened

# default .mov
sleep_mov_path = '../the_oracle_mov/sleep.mov'

# answer .movs
answer_mov_root = '../the_oracle_mov/answers/'
answer_movs = os.listdir(answer_mov_root)

# playing .mov files from python is ... difficult
# so, letting bash do it via vlc, which has a robust and well-documented cli:
# https://wiki.videolan.org/VLC_command-line_help/
play_sleep_bash = "cvlc -f -L --no-video-title-show --one-instance --no-interact ../the_oracle_mov/sleep.mov"

# start default sleep mov
sleep_process = subprocess.Popen(play_sleep_bash.split())

while True:
    # since we're jumping in mid-stream, the try/except will make sure we wait for good data
    try:
        # https://pyserial.readthedocs.io/en/latest/shortintro.html#readline
        value = serial_input.readline().strip().decode("utf-8")  # format for easy digestion - '3XX'
        print(value)

        if int(value) < 300:  # interference
            # terminate sleep process
            sleep_process.terminate()
            # os.kill(process.pid, signal.SIGINT)

            # don't cue the sleep mov while the answer plays
            # sleeping = False

            # get a random idx for selecting random answer .mov
            answer_index = random.randint(0, len(answer_movs) - 1)

            # may need --play-and-exit
            play_answer_bash = 'cvlc -f --no-video-title-show --playlist-enqueue --play-and-exit --no-interact ' + answer_mov_root + answer_movs[answer_index]

            # queue the answer .mov
            # run bash script
            answer_process = subprocess.Popen(play_answer_bash.split())
            # calling communicate() on the object returned from Popen will block until it completes.
            output, error = answer_process.communicate()
            # upon completion, terminate and kill the answer mov process and restart the sleep mov process
            answer_process.terminate()
            # answer_process.kill()
            # os.kill(answer_process.pid, signal.SIGKILL)

            # fire up the sleep loop again
            sleep_process = subprocess.Popen(play_sleep_bash.split())
    # ignore errors caused by grabbing values mid-byte and try again until we get the beginning
    except UnicodeDecodeError:
        pass
    except ValueError:
        pass



