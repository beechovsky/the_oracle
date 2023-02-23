import serial
import time
import os
import random
import subprocess
import vlc

# playing .mov files from python is ... difficult
# using python vlc bindings

# connect to Arduino
serial_path = '/dev/ttyUSB0' # for ttyUSBN, N is assigned randomly at startup. May want to determine dynamically.
serial_input = serial.Serial(serial_path, 9600)  # this auto-opens the port
time.sleep(2)  # wait for Arduino, which resets when serial conn opened

# default .mov
sleep_mov_path = '../the_oracle_mov/sleep.mov'

# answer .movs
answer_mov_root = '../the_oracle_mov/answers/'
answer_movs = os.listdir(answer_mov_root)

# create vlc instance and player.
vlc_instance = vlc.Instance('--fullscreen --no-video-title-show --no-interact'.split())
player = vlc_instance.media_player_new()

# kept for args
# play_sleep_bash = 'cvlc -f --no-video-title-show --no-interact -R ' + sleep_mov_path

print('Playing sleep mov ...')
media = vlc_instance.media_new_path(sleep_mov_path)
player.set_media(media)
player.play()

threshold = 300

while True:
    # since we're jumping in mid-stream, the try/except will make sure we wait for good data
    try:
        # https://pyserial.readthedocs.io/en/latest/shortintro.html#readline
        value = serial_input.readline().strip().decode("utf-8")  # format for easy digestion - '3XX'
        # debug
        # print(value)
        # print(len(value))
        if len(value) is 3 and int(value) < threshold:  # interference

            # prepare answer mov
            # get a random idx for selecting random answer .mov
            answer_index = random.randint(0, len(answer_movs) - 1)

            # may need  --one-instance, --play-and-exit, or --playlist-enqueue
            play_answer_bash = 'cvlc -f --no-video-title-show --no-interact --play-and-exit ' + answer_mov_root + answer_movs[answer_index]

            # TODO: don't clobber the process; use communicate instead
            # terminate sleep process
            sleep_process.terminate()  # non-blocking process only requires terminate() to stop
            
            # queue the answer .mov
            print('Playing answer mov ...')
            answer_process = subprocess.Popen(play_answer_bash.split())
            # answer_process = subprocess.Popen(play_answer_bash.split(), stdout=subprocess.PIPE)
        
            # calling wait() on the object returned from Popen will block until it completes.
            answer_process.wait()

            # fire up sleep mov when answer vid finishes
            print('Replaying sleep mov ...')
            sleep_process = subprocess.Popen(play_sleep_bash.split())

            # flush buffer
            serial_input.reset_input_buffer()

    # ignore errors caused by grabbing values mid-byte and try again until we get the beginning
    # TODO: If we were simply getting/sending start/stop signals between the components, this hack wouldn;t be necessary.
    except UnicodeDecodeError:
        pass
    except ValueError:
        pass
