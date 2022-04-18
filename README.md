# The Oracle
This repo tracks code related to the art installation "The Oracle" by Kelley Bell.

In a nutshell, and Arduino sends light intensity values from a photoresistor over serial bus to a Linux box. There, Python is used to control the playback of a series of related .mov clips based on the value sent.

If the Python code sees nominal light intensity, indicating no interference, it will loop the default 'sleep' film. Upon receiving a reading below nominal levels, indcating interference, the code will play a single pass of a randomly selected 'answer' .mov file. Once the 'answer' .mov has finished, the default loop begins again, awaiting interference. 

## Resources
This project requires programming both in Python and the Arduino programming language, which is basically C++.

### Python Docs:
https://docs.python.org/3.8/

### Arduino Language Ref:
https://www.arduino.cc/reference/en/
