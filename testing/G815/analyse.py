#! /usr/bin/env python3

import sys
from scapy.all import (
    rdpcap
)
from scapy.compat import raw
from scapy.data import EtherDA
from scapy.packet import Raw
from scapy.utils import hexdump

packets = rdpcap("ghub starten_mapping ist aus2.pcapng")

#test = Raw()
#print(raw(packets[550])[:3])
#print(len(raw(packets[143])))

num = 0
for i, p in enumerate(packets):
    if len(raw(p)) == 56:
        #print(num, raw(p)[-20:].hex(), raw(p)[-20:], i+1)
        print( f"{raw(p)[-20:]}," )
        num += 1
