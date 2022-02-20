import glob, os
from pydub import AudioSegment
import gc

os.chdir("/home/bert/audio_log_data")
file_list = glob.glob("*.wav")
file_list.sort()
for file in file_list[:-1]: #want to convert all the files except the one currently being used
    print(file)
    dst = file[:-4] + '.flac'

    sound = AudioSegment.from_wav(file)
    sound.export(dst, format="flac")

    del sound
    gc.collect()
    os.remove(file)