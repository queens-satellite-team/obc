import rtc_raspberri_pi as rtc
import time

my_rtc = rtc.RTC(1,1)

my_rtc.year = 22
#my_rtc.current_time = [12,12,12,12,12,12] 

while 1:
    time.sleep(1)
    print(f"{my_rtc.current_time}  |  [Second,Minute,Hour,Day,Month,Year]")