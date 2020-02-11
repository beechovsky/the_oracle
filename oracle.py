import serial
import time
import os
import random
import subprocess

# opening and closing this in the loop is messy; causes reading mid-string
# could alleviate that by waiting for a certain amount of info,
# but we'd still be closing and reopening the stream which will cause pauses and stutters
# so, the stream is always on
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
# may need -L to loop
play_sleep_bash = "cvlc -f --no-video-title-show --one-instance --no-interact ../the_oracle_mov/sleep.mov"


# generic method to play mov files
def play_mov_cv2(bash, is_answer):
    # run bash script
    process = subprocess.Popen(bash.split())

    # calling communicate() on the object returned from Popen will block until it completes.
    # if is_answer:
    #    output, error = process.communicate()
    output, error = process.communicate()


while True:
    try:
        # https://pyserial.readthedocs.io/en/latest/shortintro.html#readline
        value = serial_input.readline().strip().decode("utf-8")  # format for easy digestion - '3XX'
        print(value)

        if int(value) > 300:  # nominal
            # play default .mov
            play_mov_cv2(play_sleep_bash, False)

            # problem 1 - catch 22
            # The call to communicate() in play_mov_cv2 blocks serial read.
            # This means the system isn't looking for serial input while the mov plays.
            # That would be okay with answer movs, but not the default sleep mov.
            # However, without that blocking, the system will attempt to spin up sleep movie every time it reads.

            # play_mov_cv2.is_answer can determine whether or not to block,
            # but that is only useful if I can stop the default sleep mov from playing anew at every readline()

            # This doesn't work because there's still no serial input while sleep mov is playing.
            # sleep for the length of the clip before reading input again
            # time.sleep(3)

        else:  # interference
            # get a random idx for selecting random answer .mov
            answer_index = random.randint(0, len(answer_movs) - 1)

            play_answer_bash = 'cvlc -f --no-video-title-show --one-instance --no-interact --play-and-exit ' + answer_mov_root + \
                               answer_movs[answer_index]

            # queue the answer .mov
            play_mov_cv2(play_answer_bash, True)
    # ignore errors caused by grabbing values mid-byte and try again until we get the beginning
    except UnicodeDecodeError:
        pass
    except ValueError:
        pass


