#!/usr/bin/env python3
import sys
import pyaudio
import wave
import re #regular expression
from datetime import datetime, timedelta
#server
import socket
import logging
import gc
from pydub import AudioSegment
import os

formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

# pi_etherNet_server = '169.254.100.53'

# TCP_IP = pi_etherNet_server #always use server IP
# TCP_PORT = 5005
# # BUFFER_SIZE = 1024 #?? NOT USED HERE...

# thisSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# # https://stackoverflow.com/questions/6380057/python-binding-socket-address-already-in-use
# thisSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # attempt to reduce TIME_WAIT after socket close, ask Matt its kinda weird but helpful
# thisSocket.bind((TCP_IP, TCP_PORT))
# thisSocket.listen(1) # I think this holts program until one connection is made
# conn, addr = thisSocket.accept() #blocks and waits for connection, conn is connection object, addr is
# print ('Connection address:', addr)


#CHUNK is frames in buffer
CHUNK = 1024
FORMAT = pyaudio.paInt24 #must save in format 24
#CHANNELS is stereo
CHANNELS = 2
# Sample Rate
RATE = 32000 #new setting at 32
# RATE = 44100
RECORD_SECONDS = 60 #For Testing

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            frames_per_buffer=CHUNK)

def setup_logger(name, log_file, level=logging.INFO):
    """To setup as many loggers as you want"""

    handler = logging.FileHandler(log_file)        
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger

def start_logging():
    try:
        while True:

            frames = []
            dt = datetime.now()
            log_string = dt.strftime("audio_log_data/logfile_%Y_%m_%d_%H:%M:%S.log")
            wav_string = dt.strftime("audio_log_data/soundfile_%Y_%m_%d_%H:%M:%S.wav")
            flac_string = dt.strftime("audio_log_data/soundfile_%Y_%m_%d_%H:%M:%S.flac")

            wf = wave.open(wav_string, 'wb')
            logger = setup_logger("audio_logger", log_string)
            logger.info('Example of logging with ISO-8601 timestamp')
            end_time = dt + timedelta(seconds = 10) #how long our sound files are
            while True:
                curr_time = datetime.now()
                if curr_time >= end_time:
                    break
                data = stream.read(CHUNK)
                frames.append(data)
                # conn.send(data)
            del logger
            gc.collect()

            wf.setnchannels(CHANNELS)
            wf.setsampwidth(p.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))
            wf.close()

            # convert to flac/delete wav file for storage
            # sound = AudioSegment.from_wav(wav_string)
            # sound.export(flac_string, format="flac")
            # os.remove(wav_string)

    except KeyboardInterrupt:
        # thisSocket.close()
        print("\nstopping...")
        stream.stop_stream()
        stream.close()
        p.terminate()

        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()

start_logging()