"""
here will be receiving video data

in pupil capture dont forget to change the format to bgr
"""

import zmq
from msgpack import unpackb, packb
import numpy as np

context = zmq.Context()
# open a req port to talk to pupil
addr = '127.0.0.1'  # remote ip or localhost
req_port = "50020"  # same as in the pupil remote gui
req = context.socket(zmq.REQ)
req.connect("tcp://{}:{}".format(addr, req_port))
# ask for the sub port
req.send_string('SUB_PORT')
sub_port = req.recv_string()


# send notification:
def notify(notification):
    """Sends ``notification`` to Pupil Remote"""
    topic = 'notify.' + notification['subject']
    payload = packb(notification, use_bin_type=True)
    req.send_string(topic, flags=zmq.SNDMORE)
    req.send(payload)
    return req.recv_string()

# Start frame publisher with format BGR
notify({'subject': 'start_plugin', 'name': 'Frame_Publisher', 'args': {'format': 'bgr', 'fps': 1}})

#i would be able to chaneg the fps here so that it doesn't really need to be that frequently updating the information

# open a sub port to listen to pupil
sub = context.socket(zmq.SUB)
sub.connect("tcp://{}:{}".format(addr, sub_port))

# set subscriptions to topics
# recv just pupil/gaze/notifications
sub.setsockopt_string(zmq.SUBSCRIBE, 'frame.')
# this is getting the gaze data
sub.setsockopt_string(zmq.SUBSCRIBE, 'gaze.')

def recv_from_sub():
    '''Recv a message with topic, payload.

    Topic is a utf-8 encoded string. Returned as unicode object.
    Payload is a msgpack serialized dict. Returned as a python dict.

    Any addional message frames will be added as a list
    in the payload dict with key: '__raw_data__' .
    '''
    topic = sub.recv_string()
    payload = unpackb(sub.recv(), encoding='utf-8')
    extra_frames = []
    while sub.get(zmq.RCVMORE):
        extra_frames.append(sub.recv())
    if extra_frames:
        payload['__raw_data__'] = extra_frames
    return topic, payload


recent_world = None
recent_world_meta = None
recent_gaze = None


while True:
    topic, msg = recv_from_sub()

    
    # world frame
    if topic == 'frame.world':
        recent_world = {"timestamp": msg.get("timestamp"),
            "bgr": np.frombuffer(msg['__raw_data__'][0], dtype=np.uint8).reshape(msg['height'], msg['width'], 3),
            }
    # gaze
    elif topic.startswith("gaze"):
        # gaze is in the dict itself
        if "norm_pos" in msg:
            recent_gaze = {
                "timestamp": msg.get("timestamp"),
                "confidence": msg.get("confidence", 0.0),
                "norm_pos": msg["norm_pos"],  # [x_norm, y_norm]
            }
    

    # print(recent_world)
    # print(recent_gaze)
    # print()

    # ---- USE THEM TOGETHER ----
    if recent_world is not None and recent_gaze is not None:
        x_norm, y_norm = recent_gaze["norm_pos"]
        conf = recent_gaze["confidence"]

        h, w = recent_world["bgr"].shape[:2] #this is the height and width of the frame
        px = int(x_norm * w)
        py = int((1.0 - y_norm) * h)  # flip Y if needed, this is converting the norm 2d pose of the eyegaze interms of pixel data

        print(recent_world["timestamp"])
        print(recent_gaze["timestamp"])
        print()
        
        # print(f"world+gaze | px={px}, py={py}, conf={conf:.2f}, latest={topic}")
