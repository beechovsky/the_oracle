import serial
import os
import cv2
# I should be able to simply decode the byte string coming over serial,
# but the strings I get change sometimes.
# So, I'm ripping out non-numeric chars.
import re

# TODO: investigate other args
# read serial input
serial_input = serial.Serial('/dev/ttyUSB0', 9600)

# paths need updating every time this program moves to a different computer
answer_path = '/home/arctangent/the_oracle/video/answers/'
answer_dir = os.fsencode(answer_path)

sleeping_path = '/home/arctangent/the_oracle/video/sleeping.mov'

no_signal_path = '/home/arctangent/the_oracle/video/no_signal.mov'

# TODO: Is this necessary?
# serial_input.flushInput()

# While there's input, keep going.
while (serial_input.readline()):
    # # open default mov file
    # sleeping_cap = cv2.VideoCapture(sleeping_path)
    #
    # # debug
    # if (sleeping_cap.isOpened() == False):
    #   print("Error opening video file")
    #
    # # Read until video is completed
    # while (sleeping_cap.isOpened()):
    #   # Capture frame-by-frame
    #   ret, frame = sleeping_cap.read()
    #   if ret == True:
    #     # Display the resulting frame
    #     cv2.imshow('Frame', frame)
    #
    #     # Press Q on keyboard to exit
    #     if cv2.waitKey(25) & 0xFF == ord('q'):
    #       # Closes all the frames
    #       cv2.destroyAllWindows()
    #       break
    #
    #   # Break the loop
    #   else:
    #     break
    #
    # # When everything done, release the video capture object
    # #sleeping_cap.release()

    # debug
    value = serial_input.readline().strip().decode("utf-8") # decode() to return str for regex
    class_name = value.__class__.__name__
    print(value)
    print(class_name)
    ### NOTE: This was a byte string, e.g. b'358' after stripping. Something changed ...
    # Method 1: regex
    #value = re.sub("[^0-9]", "", serial_input.readline())
    # Method 2: filter and lambda
    #value = "".join(filter(lambda x: x.isdigit(), serial_input.readline()))
    #value = serial_input.readline().strip()
    #print(value)