#usr/bin/env
"""
The code for ANT Python is actually cloned from "OpenAnt" Library 
available at: https://github.com/Tigge/openant
"""

from ant.easy.node import Node
from ant.easy.channel import Channel
from ant.base.message import Message

import logging
import struct
import threading
import sys

NETWORK_KEY = [0xB9, 0xA5, 0x21, 0xFB, 0xBD, 0x72, 0xC3, 0x45]

sys.stdout = open("basic_test.csv",'w')

def on_data(data):
    heartrate = data[7]
    # string = "Heartrate: " + str(heartrate) + " [BPM]"
    string = str(heartrate) 
    sys.stdout.write(string)
    sys.stdout.write("\n")
    # The value is directly in BPM 

def main():
    # logging.basicConfig()

    node = Node()
    node.set_network_key(0x00, NETWORK_KEY)

    channel = node.new_channel(Channel.Type.BIDIRECTIONAL_RECEIVE)

    channel.on_broadcast_data = on_data
    channel.on_burst_data = on_data

    channel.set_period(8070)
    # Can set different message period for different receiving frequency
    # default 8070 counts = 4.06 hz Approximately, but can be lower too
    # Reference for the message period: 
    # https://err.no/tmp/ANT_Device_Profile_Heart_Rate_Monitor.pdf
    # Need not change any other value
    channel.set_search_timeout(12)
    channel.set_rf_freq(57)
    channel.set_id(0, 120, 0)

    try:
        channel.open()
        node.start()
    finally:
        node.stop()


if __name__ == "__main__":
    main()

#To stop the program you can just press Cntrl +  C