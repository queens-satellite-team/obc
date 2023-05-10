import rtc
import time


# def test_date_time(raw,expected):
#     pass
# def test_check_tick(raw,expected):
#     pass
# def test_encode(raw,expected):
#     pass

my_rtc = RTC(1,1,0)
my_rtc.datetime = "2021-2-5-0-15-34"
while 1:
    time.sleep(1)
    print(f"{my_rtc.datetime}  |  [Year,Month,Day,Hour,Minute,Second]")
