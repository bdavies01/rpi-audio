import time
import datetime
dt = datetime.datetime.now()
dtLog = dt.strftime("audio_log_data/logfile_%Y_%m_%d_%H.log")
f = open(dtLog,"a")
while True:
    dt = datetime.datetime.now()
    print('{:%Y-%m-%d %H:%M:%S}'.format(dt))
    f.write('{:%Y-%m-%d %H:%M:%S}'.format(dt))
    f.write('\n')
    time.sleep(5)
f.close()
