import glob, os
from pydub import AudioSegment
import sys

os.chdir("/home/bert/audio_log_data")
for file in glob.glob("*.wav"):
    print(file)
    dst = file[:-4] + '.flac'

    sound = AudioSegment.from_wav(file)
    sound.export(dst, format="flac")