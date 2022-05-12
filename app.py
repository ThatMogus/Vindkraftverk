from pyfirmata2 import Arduino
from termcolor import colored
from threading import Thread
from os import system, name
from time import sleep

def clear(): system("cls" if name == "nt" else "clear")

clear()

open("prev.txt", "w").write("red")

def greenCallback(value):
    if not value:
        if open("prev.txt", "r").read() == "green":
            print(colored("[DEBUG] [INFO] Green button pressed, but was previously pressed, ignoring input.", "blue"))
            return
        l1.write(0)
        l2.write(1)
        print(colored("[DEBUG] [SUCCESS] Green button pressed, motor turned on.", "green"))
        open("prev.txt", "w").write("green")

def redCallback(value):
    if not value:
        if open("prev.txt", "r").read() == "red":
            print(colored("[DEBUG] [INFO] Red button pressed, but was previously pressed, ignoring input.", "blue"))
            return
        l1.write(1)
        l2.write(0)
        print(colored("[DEBUG] [SUCCESS] Red button pressed, motor turned off.", "green"))
        open("prev.txt", "w").write("red")

print(colored("[DEBUG] [INFO] Establishing connection to board...", "blue"))

port = Arduino.AUTODETECT
board = Arduino(port)

print(colored("[DEBUG] [SUCCESS] Connection to board established.", "green"))

print(colored("[DEBUG] [INFO] Retrieving data from board and setting up communication...", "blue"))

board.samplingOn()

b1 = board.get_pin("d:2:u")
b2 = board.get_pin("d:3:u")
l1 = board.get_pin("d:4:o")
l2 = board.get_pin("d:5:o")
l3 = board.get_pin("d:6:o")

l1.write(1)
l2.write(0)
l3.write(0)

sleep(0.1)

b1.register_callback(greenCallback)
b2.register_callback(redCallback)

b1.enable_reporting()
b2.enable_reporting()

print(colored("[DEBUG] [SUCCESS] Communication set up.", "green"))

print(colored("[DEBUG] [INFO] Starting up warningLightHandler thread...", "blue"))

class Threads:
    class warningLightHandler(Thread):
        def __init__(self):
            Thread.__init__(self)
            self.daemon = True
            self.start()
        def run(self):
            while True:
                if open("prev.txt", "r").read() == "green":
                    l3.write(1)
                    sleep(1)
                    l3.write(0)
                    sleep(1)

Threads.warningLightHandler()

print(colored("[DEBUG] [SUCCESS] Successfully started warningLightHandler thread.", "green"))

print(colored("[DEBUG] [INFO] Waiting for inputs...", "blue"))

input()
