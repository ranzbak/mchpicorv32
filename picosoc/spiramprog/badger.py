#!/usr/bin/env python3

import serial
import sys
import time
import select
import tty
import termios
import binascii


def getChar(block=True):
    if block or select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
        return sys.stdin.read(1)


class Badger:
    def __init__(self, portname):
        self.portname = portname
        self.port = serial.Serial(self.portname, 115200, timeout=0)

    def attempt_reset(self):
        self.port.write(bytes([3]))
        prev_time = time.time()
        shell_counter = 0
        timeout_counter = 10000
        while timeout_counter > 0:
            c = self.port.read(1)
            if c == b'>':
                shell_counter += 1
            else:
                shell_counter = 0

            if shell_counter >= 3:
                return True

            curr_time = time.time()
            if curr_time - prev_time > 2:
                prev_time = curr_time
                self.port.write(bytes([3]))

            timeout_counter -= 1
            if c == b'':
                time.sleep(0.001)
        return False

    def connect(self):
        print("Connecting to {}...".format(self.portname))
        self.port.reset_input_buffer()
        if not self.attempt_reset():
            print("Failed to connect")
            return False
        return True

    def shell(self):
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        tty.setraw(fd)
        # self.port.write(bytes([3]))
        print("Badge python shell, press ctrl+\\ to exit.")
        try:
            while True:
                c = self.port.read(1)
                print(c.decode("ascii"), end="", flush=True)
                k = getChar(False)
                if k:
                    if ord(k) == 28:
                        break
                    else:
                        self.port.write(bytes(k, "utf-8"))
                if c == b'' and not k:
                    time.sleep(0.001)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    def fpga(self, bitstream):
        self.port.write(b'import ice40, stm32, binascii\r\n')
        time.sleep(0.01)
        self.port.write(b'stm32.lcd_fpga(True)\r\n')
        time.sleep(0.01)
        bitstream_str = binascii.hexlify(bitstream)
        self.port.write(bytes([1]))  # CTRL+A
        self.port.write(b'bitstream="')
        counter = 0
        print("Sending bitstream...", end="", flush=True)
        self.port.write(bytes(bitstream_str))
        self.port.write(b'"\r\n')
        print(" Done.", flush=True)
        self.port.write(
            b'bitstream=binascii.unhexlify(bitstream);ice40.load(bitstream)\r\n')
        self.port.write(bytes([4, 2]))  # CRTL-D, CTRL+B
        print("Waiting while the ESP32 programs the FPGA...")
        time.sleep(4)
        print("Done, dropping to python shell...")
        self.port.reset_input_buffer()
        self.shell()


def main():
    if len(sys.argv) < 3:
        print("Usage: {} <port> <command>".format(sys.argv[0]))
        sys.exit(1)
    portname = sys.argv[1]
    command = sys.argv[2]
    badger = Badger(portname)
    if not badger.connect():
        sys.exit(1)
    if command == "shell":
        badger.shell()
    elif command == "fpga":
        if len(sys.argv) < 4:
            print("Usage: {} <port> fpga <bitstream file>".format(sys.argv[0]))
            sys.exit(1)
        with open(sys.argv[3], "rb") as f:
            bitstream = f.read()
        badger.fpga(bitstream)


if __name__ == "__main__":
    main()
