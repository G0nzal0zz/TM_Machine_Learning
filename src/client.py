"""
This is an empty template showing basic interactions with a TMI2 interface with Python.
"""
import argparse
import time

from tminterface2 import MessageType, TMInterface

PORT = 8477

def main():
    # parser = argparse.ArgumentParser()
    # parser.add_argument("--tmi_port", "-p", type=int, default=8477)
    #  args = parser.parse_args()
    iface = TMInterface(8477)
    now = time.time()

    if not iface.registered:
        while True:
            try:
                iface.register(2)
                break
            except ConnectionRefusedError as e:
                print(e)

    while True:

        msgtype = iface._read_int32()
        # =============================================
        #        READ INCOMING MESSAGES
        # =============================================
        if msgtype == int(MessageType.SC_RUN_STEP_SYNC):
            _time = iface._read_int32()
            if time.time() - now > 1:
                now = time.time()
                print(iface.get_simulation_state().velocity)
                if (iface.get_simulation_state().velocity[0] < 0.1 and iface.get_simulation_state().velocity[1] < 0.1 and iface.get_simulation_state().velocity[2] < 0.1):
                    iface.recover_inputs()

            # ============================
            # BEGIN ON RUN STEP
            # ============================

            # ============================
            # END ON RUN STEP
            # ============================
            iface._respond_to_call(msgtype) 
        elif msgtype == int(MessageType.SC_CHECKPOINT_COUNT_CHANGED_SYNC):
            current = iface._read_int32()
            target = iface._read_int32()
            # ============================
            # BEGIN ON CP COUNT
            # ============================
            # ============================
            # END ON CP COUNT
            # ============================
            iface._respond_to_call(msgtype)
        elif msgtype == int(MessageType.SC_LAP_COUNT_CHANGED_SYNC):
            iface._read_int32()
            iface._respond_to_call(msgtype)
        elif msgtype == int(MessageType.SC_REQUESTED_FRAME_SYNC):
            iface._respond_to_call(msgtype)
        elif msgtype == int(MessageType.C_SHUTDOWN):
            iface.close()
        elif msgtype == int(MessageType.SC_ON_CONNECT_SYNC):
            iface._respond_to_call(msgtype)
        else:
            pass


if __name__ == "__main__":
    main()