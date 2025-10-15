import pendulum
import pyaudio
import random
import numpy as np
import struct
from copy import deepcopy
import time
import threading

MIDI_CONTROL = False

if MIDI_CONTROL:
    import mido

p = pyaudio.PyAudio()

def pt_to_sample(x,y,bits=16):
    x = x.astype(int)
    y = y.astype(int)
    if len(x) != len(y):
        raise Exception("x and y arrays must have the same length")
    l = len(x)
    combined = np.column_stack((x,y)).ravel()
    if bits == 8:
        return struct.pack(f"{2*l}b",*combined)
    elif bits == 16:
        return struct.pack(f"{2*l}h",*combined)
    elif bits == 32:
        return struct.pack(f"{2*l}i",*combined)
    else:
        raise Exception("Bitwidth must be 8, 16 or 32.")


running = True

SR = 192000
CHANNELS = 2
BITWIDTH = 16
FORMAT = p.get_format_from_width(BITWIDTH//8)
buf_queue = []
q_indices = []

def audio_thread():
    global running, p, SR, CHANNELS, FORMAT, buf_queue, q_indices

    device_index = None
    for ndev in range(p.get_device_count()):
        dev = p.get_device_info_by_index(ndev)
        if dev["maxOutputChannels"] > 0 and \
            dev["hostApi"] == 2 and \
            dev["name"] == "CABLE In 16ch (VB-Audio Virtual Cable)":
            device_index = ndev
            print(dev)
            print("Device Index:",device_index)
            break

    stream = p.open(SR, CHANNELS, FORMAT, output = True, output_device_index = device_index)
    start = time.time()
    i = 0
    while running:
        t = time.time() - start
        if len(buf_queue) > 0:
            i += 1
            stream.write(buf_queue.pop(0))
            

def note_to_freq(note):
    #A4 - 57, 440 Hz
    diffA4 = note - 57
    return 440*(2**(diffA4/12))

def main():
    global running, buf_queue, q_indices

    audioT = threading.Thread(target=audio_thread,daemon = True)
    audioT.start()

    dp = pendulum.DoublePend(1<<(BITWIDTH-4),1<<(BITWIDTH-3),1,2,0.01,0.01,1,0,10000)

    BUFFER_SIZE = 4096
    Q_SIZE = 40
    sim_acc = 2
    speed = 1
    freq = 440

    if MIDI_CONTROL:
        print(mido.get_input_names())
        port_name = "V_MIDI 0"
        inport = mido.open_input(port_name)
        freq = 5

    startTime = time.time()
    t = 0
    buffer = b""
    vol = 1
    print(SR//freq)
    i = 0
    lines = None
    while running:
        if MIDI_CONTROL:
            for msg in inport.iter_pending():
                print(msg)
                if msg.type == 'note_on':
                    
                    freq = note_to_freq(msg.note)
                    vol = 1
                    i = 0
                elif msg.type == 'note_off':
                    #freq = 50
                    vol = 0
                    i = 0
                #print(SR//freq)
        p0 = np.array([0,0])
        p1 = p0 + np.array([dp.l1*np.sin(dp.a1),dp.l1*np.cos(dp.a1)])
        p2 = p1 + np.array([dp.l2*np.sin(dp.a2), dp.l2*np.cos(dp.a2)])
        p3 = p1
        p4 = p0
        points = np.vstack([p0, p1, p2, p3, p4])  # shape (4,2)

        # --- Compute segment lengths ---
        diffs = np.diff(points, axis=0)         # shape (3,2)
        segment_lengths = np.linalg.norm(diffs, axis=1)
        total_length = segment_lengths.sum()
        
        
        cumdist = np.insert(np.cumsum(segment_lengths), 0, 0)
        x = points[:,0]
        y = points[:,1]

        target_distances = np.linspace(0, total_length, int(SR//freq))

        new_x = np.interp(target_distances, cumdist, x)
        new_y = np.interp(target_distances, cumdist, y)
        lines = np.stack([new_x, new_y], axis=1)*vol


        if len(buf_queue) < Q_SIZE:
            buffer += pt_to_sample(lines[:,0],lines[:,1],BITWIDTH)
            while len(buffer) >= BUFFER_SIZE:
                buf_queue.append(buffer[:BUFFER_SIZE])
                buffer = buffer[BUFFER_SIZE:]
                i += 1
        #print(len(buf_queue))
        #time.sleep(BUFFER_SIZE/SR)
        new_t = time.time() - startTime
        ms = round((new_t-t)*1000)
        t = new_t
        for m in range(sim_acc*speed*ms):
            dp.update(t=0.001/sim_acc)
    if MIDI_CONTROL:
        inport.close()
        
if __name__ == "__main__":
    main()
    quit()