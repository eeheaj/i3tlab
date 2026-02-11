import zmq
import msgpack #this is the serializer

ctx = zmq.Context()
# The REQ talks to Pupil remote and receives the session unique IPC SUB PORT
pupil_remote = ctx.socket(zmq.REQ)

ip = 'localhost'  # If you talk to a different machine use its IP.
port = 50020  # The port defaults to 50020. Set in Pupil Capture GUI.

pupil_remote.connect(f'tcp://{ip}:{port}')

# Request 'SUB_PORT' for reading data
pupil_remote.send_string('SUB_PORT')
sub_port = pupil_remote.recv_string()

# Request 'PUB_PORT' for writing data
pupil_remote.send_string('PUB_PORT')
pub_port = pupil_remote.recv_string()

# Assumes `sub_port` to be set to the current subscription port
subscriber = ctx.socket(zmq.SUB)
subscriber.connect(f'tcp://{ip}:{sub_port}')
subscriber.subscribe('gaze.')  # receive all gaze messages


# while True:
#     topic, payload = subscriber.recv_multipart()
#     message = msgpack.loads(payload)
#     print(f"{topic}: {message}")

#store data in an array [time stamp, x, y, conf]
data = []

while True:
    topic, payload = sub.recv_multipart()
    gaze = msgpack.loads(payload, raw=False)

    # Example fields
    ts = gaze["timestamp"]
    conf = gaze["confidence"]

    if "norm_pos" in gaze:
        x, y = gaze["norm_pos"]
        print(f"2D gaze | x={x:.3f}, y={y:.3f}, conf={conf:.2f}")

        dat = [ts,x,y,conf]
        data.append(dat)