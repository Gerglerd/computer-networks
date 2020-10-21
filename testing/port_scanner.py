from socket import *
import time

startTime = time.time()

if __name__ == '__main__':
    target = input('Enter the host to be scanned: ')
    target_IP = gethostbyname(
        target)  # given a host name the gethostbyname() function returns the IP address of the host
    print('Sterting scan on host: ', target_IP)

    for i in range(50, 500):
        s = socket(AF_INET, SOCK_STREAM)

        conn = s.connect_ex((target_IP, i))  # connect(address) with execution
        if (conn == 0):  # 0 succeeded
            print('Port %d: OPEN' % (i,))
        s.close()
print('Time taken: ', time.time() - startTime)
