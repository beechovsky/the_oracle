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
# play_sleep_bash = "cvlc -R --no-video-title-show --one-instance --no-interact -f ../the_oracle_mov/sleep.mov"
play_sleep_bash = "cvlc -R --no-video-title-show --no-interact -f ../the_oracle_mov/sleep.mov"

# start default sleep mov, non-blocking so interference can be caught
sleep_process = subprocess.Popen(play_sleep_bash.split())

# state
# sleeping = True

while True:
    # since we're jumping in mid-stream, the try/except will make sure we wait for good data
    try:
        # https://pyserial.readthedocs.io/en/latest/shortintro.html#readline
        value = serial_input.readline().strip().decode("utf-8")  # format for easy digestion - '3XX'
        print(value)
        # serial_input.reset_input_buffer()

        if int(value) < 300:  # interference
            # interference isn't instantaneous; need to flush the buffer so multiple values under 300 don't get caught
            # could slow down the stream from the Arduino, but trying to time paper drops is silly
            # https://pythonhosted.org/pyserial/pyserial_api.html#serial.Serial.reset_input_buffer
            # Close and flush input buffer, discarding all its contents.
            # serial_input.reset_input_buffer()
            # serial_input.flush()

            # terminate sleep process
            sleep_process.terminate()  # non-blocking process only requires terminate() to stop

            # get a random idx for selecting random answer .mov
            answer_index = random.randint(0, len(answer_movs) - 1)

            # may need  --one-instance --play-and-exit; doesn't need --playlist-enqueue as that's default behavior
            play_answer_bash = 'cvlc --no-video-title-show --no-interact --play-and-exit -f ' + answer_mov_root + answer_movs[answer_index]

            # queue the answer .mov
            answer_process = subprocess.Popen(play_answer_bash.split())
            # answer_process = subprocess.Popen(play_answer_bash.split(), stdout=subprocess.PIPE)

            # update state
            # sleeping = False

            # calling wait() on the object returned from Popen will block until it completes.
            answer_process.wait()
            # blocking processes are harder to kill
            # close, terminate, and kill the answer mov process and restart the sleep mov process
            # answer_process.stdout.close()

            # fire up sleep mov when answer vid finishes
            sleep_process = subprocess.Popen(play_sleep_bash.split())

            # flush buffer
            serial_input.reset_input_buffer()
            # sleep_process = subprocess.Popen(play_sleep_bash.split())
            # sleeping = True
            # blocking processes are harder to kill
            # close, terminate, and kill the answer mov process and restart the sleep mov process
            # answer_process.stdout.close()
            # answer_process.terminate()
            # answer_process.kill()

            # open the buffer again, before starting the sleep again because it takes a moment to start reading
            # serial_input.open()
            # fire up the sleep loop again
            # sleep_process = subprocess.Popen(play_sleep_bash.split())
            # serial_input.reset_input_buffer()

    # ignore errors caused by grabbing values mid-byte and try again until we get the beginning
    except UnicodeDecodeError:
        pass
    except ValueError:
        pass



