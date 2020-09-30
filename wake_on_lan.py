# This module provides access to the BSD socket interface, low-level network interface
import socket  # API for data exchange between processes

# this module performs conversions between Python values and C structs represented as Python bytes objects
import struct


def WakeOnLan(ethernet_address):
    # construct six-byte hw address

    addr_byte = ethernet_address.split(':')

    if len(addr_byte) != 6:
        print("\n Illegal MAC address\n")
        print("Format MAC address => 00:11:22:33:44:55\n")
        return

    # struct.pack(format,v1,v2,...) - return a bytes object containing the values v1, v2, … packed according to the format string format
    hw_addr = struct.pack('BBBBBB', int(addr_byte[0], 16),
                          int(addr_byte[1], 16),
                          int(addr_byte[2], 16),
                          int(addr_byte[3], 16),
                          int(addr_byte[4], 16),
                          int(addr_byte[5], 16))

    # build WOL MagicPocket
    # the leading \x escape sequence means the next two characters are interpreted as hex digits for the character code
    msg = '\xff' * 6 + str(hw_addr * 16)

    # send pocket to the broadcast address using UDP

    # AF_INET (host, port) (-> host -string, port - integer) - is an address family that is used to designate the type of addresses that your socket can communicate with
    # SOCK-DGRAM - UDP is datagram-based protocol
    soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # setcockopt - o manipulate the socket-level options described in this section
    # SOL_SOCKET is the socket layer itself. It is used for options that are protocol independent
    # set the SO_BROADCAST option on before attempting to send a datagram to a base or broadcast address. This protects the application from accidentally sending a datagram to many systems
    soc.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    # special host address: string '<broadcast>' represents INADDR_BROADCAST (only for IPv4)
    soc.sendto(msg.encode(), ('<broadcast>', 9))
    soc.close()


WakeOnLan('64:6e:69:d7:f2:41')

