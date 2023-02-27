import serial
import time
import os
import random
import vlc
import keyboard # requires root/sudo
# import subprocess # may be handy for blocking during answer playback, or looping sleep mov wiuthout two instances below

# playing .mov files from python is ... difficult
# using python vlc bindings
# https://www.olivieraubert.net/vlc/python-ctypes/doc/
# https://wiki.videolan.org/VLC_command-line_help/

################
# ARDUINO BITS #
################
# connect to Arduino
serial_path = '/dev/ttyUSB0' # for ttyUSBN, N is assigned randomly at startup. May want to determine dynamically.
serial_input = serial.Serial(serial_path, 9600)  # this auto-opens the port
time.sleep(2)  # wait for Arduino, which resets when serial conn opened
threshold = 300 # nominal value from sensor; below indicates interference

###############
# .MOVS & VLC #
###############
# default .mov
sleep_mov_path = '../the_oracle_mov/sleep.mov'

# answer .movs
answer_mov_root = '../the_oracle_mov/answers/'
answer_movs = os.listdir(answer_mov_root)

# Using '--input-repeat=999999' made my soul hurt but this API is rubbish and this is the only thing that works.
vlc_instance = vlc.Instance('--input-repeat=999999')

# TWO OPTIONS: MediaPlayer, and MediaListPlayer. The former has more built-in methods.
player = vlc_instance.media_player_new()
#list_player = vlc_instance.media_list_player_new()
#media_list = vlc_instance.media_list_new()
player.set_fullscreen(True)

sleep_media = vlc_instance.media_new(sleep_mov_path) # or media_new_path? there are, of course, multiple ways to do this
# media_list.add_media(sleep_media)
# list_player.set_media_list(media_list)
# list_player.play()

def play_sleep_mov():
    player.set_media(sleep_media) # forces starting at beginning, or should; otherwise it doesn't need to be in here
    player.play()
    # media_list.add_media(sleep_media)
    # list_player.set_media_list(media_list)
    # list_player.play()

print('Starting sleep .mov ...')
play_sleep_mov()

###########
# CONTROL #
###########
keyboard.add_hotkey("Esc", lambda: player.set_fullscreen(False))

while True:
    # TODO: need a way to exit gracefully when in fullscreen
    
    # since we're jumping in mid-stream, the try/except will make sure we wait for good data
    try:
        # https://pyserial.readthedocs.io/en/latest/shortintro.html#readline
        value = serial_input.readline().strip().decode("utf-8")  # format for easy digestion - '3XX'
        # print(value)
        if len(value) == 3 and int(value) < threshold:  # interference

            # prepare answer mov - get a random idx for selecting random answer .mov
            answer_index = random.randint(0, len(answer_movs) - 1)
            answer_path = answer_mov_root + answer_movs[answer_index]
            answer_media = vlc_instance.media_new_path(answer_path)
            print('Playing answer .mov ...')
            player.set_media(answer_media) # adding to a playlist would be smoother
            player.play()
            #media_list.remove_index(0) # trim the list; remove sleep .mov
            #media_list.add_media(answer_media)
            #list_player.set_media_list(media_list)
            #print('playing answer .mov ...') 
            #list_player.play() # next() if we leave the sleep movie in
    
            # block interference during answer playback
            time.sleep(1) # dunno if this is necessary
            duration = player.get_length() / 1000
            time.sleep(duration - 1)
            
            # transition is a little rough. try two instances of vlc?
            print('Replaying answer .mov ...')
            play_sleep_mov()
            
            # flush buffer
            serial_input.reset_input_buffer()

    # ignore errors caused by grabbing values mid-byte and try again until we get the beginning
    # TODO: If we were simply getting/sending start/stop signals between the components, this hack wouldn;t be necessary.
    except UnicodeDecodeError:
        pass
    except ValueError:
        pass
