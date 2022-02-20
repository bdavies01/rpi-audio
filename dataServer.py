#!/usr/bin/env python3
import sys
import pyaudio
import wave
import re #regular expression
#server
import socket

pi_etherNet_server = '169.254.100.53'

TCP_IP = pi_etherNet_server #always use server IP
TCP_PORT = 5005
# BUFFER_SIZE = 1024 #?? NOT USED HERE...

# thisSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# # https://stackoverflow.com/questions/6380057/python-binding-socket-address-already-in-use
# thisSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # attempt to reduce TIME_WAIT after socket close, ask Matt its kinda weird but helpful
# thisSocket.bind((TCP_IP, TCP_PORT))
# thisSocket.listen(1) # I think this holts program until one connection is made
# conn, addr = thisSocket.accept() #blocks and waits for connection, conn is connection object, addr is
# print ('Connection address:', addr)


#CHUNK is frames in buffer
CHUNK = 1024
FORMAT = pyaudio.paInt32
#CHANNELS is stereo
CHANNELS = 2
# Sample Rate
# RATE = 16000
RATE = 44100
RECORD_SECONDS = 60 #For Testing

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            frames_per_buffer=CHUNK)



frames = []
for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
     data = stream.read(CHUNK)
     frames.append(data) #each "data" is 8209 bytes
     # print(sys.getsizeof(data))
    #  conn.send(data)
# container = list(frames[0])
# for n in range(0, len(container), 4):
#     print(container[n:n+4])
# thisSocket.close()
stream.stop_stream()
stream.close()
p.terminate()


wf = wave.open("60sec.wav", 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))

# joined = b''.join(frames)
# for i in range(0, len(data), 4):
#     for j in range(3, -1, -1):
#         print(f"{joined[i+j]} ",end="")
#     print("")
wf.close()
