# This module provides access to the BSD socket interface, low-level network interface
import socket  # API for data exchange between processes

# this module performs conversions between Python values and C structs represented as Python bytes objects
import struct


def WakeOnLan(ethernet_address):
    # construct six-byte hw address


    # build WOL MagicPocket
    # the leading \x escape sequence means the next two characters are interpreted as hex digits for the character code
    msg = bytes.fromhex('FF')*6+bytes.fromhex(ethernet_address)*16
    # send pocket to the broadcast address using UDP

    # AF_INET (host, port) (-> host -string, port - integer) - is an address family that is used to designate the type of addresses that your socket can communicate with
    # SOCK-DGRAM - UDP is datagram-based protocol
    soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # setcockopt - o manipulate the socket-level options described in this section
    # SOL_SOCKET is the socket layer itself. It is used for options that are protocol independent
    # set the SO_BROADCAST option on before attempting to send a datagram to a base or broadcast address. This protects the application from accidentally sending a datagram to many systems
    soc.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    # special host address: string '<broadcast>' represents INADDR_BROADCAST (only for IPv4)
    soc.sendto(msg, ('<broadcast>', 9))
    soc.close()


WakeOnLan('64 6e 69 d7 f2 41 ')
