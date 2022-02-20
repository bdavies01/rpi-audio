import glob, os
from pydub import AudioSegment
import sys

os.chdir("/home/bert/audio_log_data")
for file in glob.glob("*.flac"):
    dst = file[:-5] + '.wav'

    print(file)
    print(dst)

    cmd_string = 'ffmpeg -i ' + file + ' ' + dst
    print(cmd_string)
    os.system(cmd_string)
    os.remove(file)