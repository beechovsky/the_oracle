import serial
import time
import os
import random
import vlc
# import subprocess # may be handy for blocking during answer playback

# playing .mov files from python is ... difficult
# using python vlc bindings
# https://www.olivieraubert.net/vlc/python-ctypes/doc/
# https://wiki.videolan.org/VLC_command-line_help/

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
vlc_instance = vlc.Instance() # passing options here doesn't seem to actually work

# Standard player can play vids, but doesn't seem to respond to any commands like looping. Trying a list player below.
# player = vlc_instance.media_player_new()
list_player = vlc_instance.media_list_player_new()
media_list = vlc_instance.media_list_new()
# player.set_fullscreen(True) # TODO: turn on only when certain you can esc/minimize it
# need to be able to get out of mov
# TODO: Get interference via input working so you don't have to nuke the pi when in fullscreen
#player.video_set_key_input(True)
#player.video_set_mouse_input(True)

print('Playing sleep .mov ...')
sleep_media = vlc_instance.media_new_path(sleep_mov_path)
# sleep_media.add_option() # TODO: solve repeating/loooping sleep .mov
# vlc_instance.vlm_set_loop(sleep_media, True) # need a string of file name apparently
# sleep_media.add_option_flag('--repeat',1)
# player.set_media(sleep_media)
#vlc_instance.vlm_set_loop(sleep_mov_path, True) # Sigh. Nope.
# vlc.libvlc_vlm_set_loop(vlc_instance, sleep_media.get_meta(0), True) # get_meta(0) = Title
# player.play()
media_list.add_media(sleep_media)
list_player.set_media_list(media_list)
list_player.play()

threshold = 300 # nominal value from sensor; below indicates interference

while True:
    # since we're jumping in mid-stream, the try/except will make sure we wait for good data
    try:
        # https://pyserial.readthedocs.io/en/latest/shortintro.html#readline
        value = serial_input.readline().strip().decode("utf-8")  # format for easy digestion - '3XX'
        # debug
        # print(value)
        # print(len(value))
        if len(value) == 3 and int(value) < threshold:  # interference

            # prepare answer mov
            # get a random idx for selecting random answer .mov
            # TODO: sort out how to block during answer playback; do not want to reposnd to subseqent quyestions until back to sleep movie
            answer_index = random.randint(0, len(answer_movs) - 1)
            answer_path = answer_mov_root + answer_movs[answer_index]
            answer_media = vlc_instance.media_new_path(answer_path)
            #player.set_media(answer_media)
            #player.play()
            media_list.remove_index(0) # trim the list; remove sleep .mov
            media_list.add_media(answer_media)
            list_player.set_media_list(media_list)
            print('playing answer .mov ...') 
            list_player.play() # next()?
            # TODO: determine how to block during answer playback and how to start sleep .mov when it's done
            
            print('cleaning up answer .mov ...')
            media_list.remove_index(0) # remove answer .mov to keep list from blowing up
            media_list.add_media(sleep_media)
            list_player.set_media_list(media_list)
            print('replaying sleep .mov ...')
            list_player.play()
            
            # flush buffer
            serial_input.reset_input_buffer()

    # ignore errors caused by grabbing values mid-byte and try again until we get the beginning
    # TODO: If we were simply getting/sending start/stop signals between the components, this hack wouldn;t be necessary.
    except UnicodeDecodeError:
        pass
    except ValueError:
        pass
