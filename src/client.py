import socket
import struct
import time
import signal
import random
from tminterface.structs import SimStateData, CheckpointData

HOST = "127.0.0.1"
PORT = 8477

SC_RUN_STEP_SYNC = 0
C_SET_SPEED = 1
C_REWIND_TO_STATE = 2
C_SET_INPUT_STATE = 3
C_SHUTDOWN = 4
C_RECOVER_INPUT = 5

sock = None

def signal_handler(sig, frame):
    global sock

    print('Shutting down...')
    sock.sendall(struct.pack('i', C_SHUTDOWN))
    sock.close()


def rewind_to_state(sock, state):
    sock.sendall(struct.pack('i', C_REWIND_TO_STATE))
    sock.sendall(struct.pack('i', len(state.data)))
    sock.sendall(state.data)

def set_input_state(sock, up=-1, down=-1, steer=0x7FFFFFFF):
    sock.sendall(struct.pack('i', C_SET_INPUT_STATE))
    sock.sendall(struct.pack('b', up))
    sock.sendall(struct.pack('b', down))
    sock.sendall(struct.pack('i', steer))

def respond(sock, type):
    sock.sendall(struct.pack('i', type))

def main():
    global sock

    first_state = 0

    ticks_per_second = 0
    now = time.time()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    signal.signal(signal.SIGINT, signal_handler)

    sock.connect((HOST, PORT))
    print('Connected')
    while True:
        message_type = struct.unpack('i', sock.recv(4))[0]
        if message_type == SC_RUN_STEP_SYNC:
            state_length = struct.unpack('i', sock.recv(4))[0]
            state = SimStateData(sock.recv(state_length))
            state.cp_data.resize(CheckpointData.cp_states_field, state.cp_data.cp_states_length)
            state.cp_data.resize(CheckpointData.cp_times_field, state.cp_data.cp_times_length)

            if time.time() - now > 1:
                velocity = state.velocity
                position = state.position
                # Now 'velocity' contains the velocity as a list [vx, vy, vz]
                print("Velocity:", velocity)
                print("Position:", position)
                print(f'Effective speed: {ticks_per_second / 100}x')
                now = time.time()
                ticks_per_second = 0

            race_time = state.player_info.race_time

            if race_time == 0:
                first_state = state

            if race_time > 0 and race_time % 1000 == 0:
                set_input_state(sock, up=True, down=False, steer=random.randint(-65536,65536))
            if (race_time > 2000 and all(int(v) == 0 for v in state.velocity)):
                respond(sock, C_RECOVER_INPUT)
                respond(sock, SC_RUN_STEP_SYNC)
                rewind_to_state(sock, first_state)

            respond(sock, SC_RUN_STEP_SYNC)

            ticks_per_second += 1

if __name__ == "__main__":
    main()