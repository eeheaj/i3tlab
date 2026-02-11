# PupilLab real time tutorial

for my computer usage --> setup anaconda library as pupil

in the environment 
pip install pupil-labs-realtime-api
pip install zmq msgpack==0.5.6

## running pupil core and setting up
sudo /Applications/Pupil\ Capture.app/Contents/MacOS/pupil_capture

# progress update
2/11
- so the current realtime.py has a dictionary of both rgb formatted world frame and eye gaze data (converted to 2d pos in frame)
- question is how I'm going to send it into yolo. 