#!/usr/bin/env python3
import pyaudio
import wave
from datetime import datetime, timedelta
import logging
import gc
import os
import glob
from pydub import AudioSegment
from multiprocessing import Process
import socket

logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

CHUNK = 1024 #CHUNK is frames in buffer
FORMAT = pyaudio.paInt24 #must save in format 24
CHANNELS = 2 #CHANNELS is stereo
RATE = 32000 #new setting at 32

PORT = 5001

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            frames_per_buffer=CHUNK)

def setup_logger(logger, log_file, level=logging.INFO):
    """To setup as many loggers as you want"""

    handler = logging.FileHandler(filename=log_file)
    handler.setLevel(level)
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    return handler

# Convert all of the .wav files in a given directory to .flac files

def wav_to_flac(dir):
    file_list = glob.glob(dir + '/*.wav')
    file_list.sort()
    for file in file_list: 
        dst = file[:-4] + '.flac'

        sound = AudioSegment.from_wav(file)
        sound.export(dst, format="flac")

        del sound
        gc.collect()
        os.remove(file)

# Initialize logging MEMS microphone data into a subdirectory called 'audio_log_data'
# Every day a new directory is created corresponding to the current date. Within that 
# directory, every hour a subdirectory is created corresponding to the hour. 
# Additionally, each hour a new process will spawn that converts/compresses all of
# the .wav files from past hour into .flac files. Every 5 minutes, a .log and .wav 
# file are created and stored in the innermost file. 

def start_logging():
    socket_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        while True:
            try:
                socket_obj.bind(('', PORT))
                socket_obj.listen(1) # Only allow one connection for now
                conn, addr = socket_obj.accept()
                conn.setblocking(False) # Don't block waiting for data from this connection
                print('Connected by: ', addr)
            except socket.error:
                pass
            dt_outer = datetime.now()

            while True:
                dt_mid = datetime.now()
                if dt_mid.date() != dt_outer.date(): # how often to make a main dir change to 1 day
                    break
                path = dt_mid.strftime('/media/pi/DDI_UCSC_LOGGING/audio_log_data/%Y_%m_%d')
                if not os.path.exists(path):
                    os.makedirs(path)

                path_inner = ''
                handler = None
                while True:
                    dt_inner = datetime.now()
                    if dt_inner.hour != dt_mid.hour: # how often to make a subdir change to 1 hour
                        logger.removeHandler(handler)
                        del handler
                        gc.collect()
                        break

                    old_path = path_inner
                    path_inner = path + '/' + dt_inner.strftime('%H')
                    if not os.path.exists(path_inner):
                        os.makedirs(path_inner)
                        log_string = path_inner + '/' + dt_inner.strftime('logfile_%H.log')
                        handler = setup_logger(logger, log_string)
                        logger.info('Log start')
                        proc = Process(target=wav_to_flac, args=(old_path,), daemon=True)
                        proc.start()

                    frames = []
                    wav_string = path_inner + '/' + dt_inner.strftime('soundfile_%H:%M:%S.wav')

                    wf = wave.open(wav_string, 'wb')
                    end_time = dt_inner + timedelta(minutes=5) # how long our sound files are, change to 5 minutes

                    while True:
                        curr_time = datetime.now()
                        if curr_time >= end_time:
                            break
                        data = stream.read(CHUNK, exception_on_overflow=False)
                        frames.append(data)
                        try:
                            data = conn.recv(1024)
                            if data:
                                logger.info(data.decode())
                        except Exception:
                            pass
                        # conn.send(data)

                    wf.setnchannels(CHANNELS)
                    wf.setsampwidth(p.get_sample_size(FORMAT))
                    wf.setframerate(RATE)
                    wf.writeframes(b''.join(frames))
                    wf.close()
                

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