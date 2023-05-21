import time
from rtc import RTC

my_rtc = RTC(1,1,0,"2021-2-5-0-15-34") # Initalize RTC

while 1:
    time.sleep(1)
    print(f"{my_rtc.datetime}  |  [Year,Month,Day,Hour,Minute,Second]")
