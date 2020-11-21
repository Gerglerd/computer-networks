import sys
from scapy.all import sniff
import threading
from matplotlib import pyplot
from matplotlib import animation

data_count = [0]
time_points = [0]

time_interval = 0.5
time_width = 15

if len(sys.argv) > 2:
    print('Usage:', sys.argv[0], '[filter]')
    exit()
if len(sys.argv) == 2:
    filt = sys.argv[1]
else:
    print('Enter valid pcap filter:')
    filt = input()


def handlePacket(packet):
    global data_count
    data_count[-1] += len((bytes(packet)))


def plot_cont():
    fig = pyplot.figure()
    plot = fig.add_subplot(111)
    fig.canvas.set_window_title("Network indicator")

    def update(i):
        while len(data_count) * time_interval > time_width:
            time_points.pop(0)
            data_count.pop(0)
        plot.clear()
        plot.set_title('Network activity')
        plot.set_xlabel('Seconds, s')
        plot.set_ylabel('Data, bytes')
        plot.plot(time_points, data_count)

        data_count.append(0)
        time_points.append(time_points[-1] + time_interval)

    a = animation.FuncAnimation(fig, update, repeat=False)
    pyplot.show()


capture_thread = threading.Thread(target=sniff, kwargs={'prn': handlePacket, 'filter': filt})
capture_thread.start()
plot_cont()
