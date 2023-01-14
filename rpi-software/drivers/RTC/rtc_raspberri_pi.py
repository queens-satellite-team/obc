#Maintainer Harrison Gordon
import time
from   smbus import SMBus

class RTC:
    '''
    RTC class for MCP79410
    Data Sheet: http://ww1.microchip.com/downloads/en/devicedoc/20002266h.pdf
    
    Functionality:
    -Enable/Disable Internal Oscillator (Start and Stop Clock)
    -Get Date and Time from Clock
    -Enable/Disable Backup Battery
    -Reset Clock 
    '''
    i2c_bus = SMBus(1)
    registers = {
        'slave' : 0x6F,
        'second': 0x00,
        'minute': 0x01,
        'hour' : 0x02,
        'wkday' : 0x3,
        'day' : 0x04,
        'month': 0x05,
        'year' : 0x06,
    }

    def __check_tick(self,clock_state):
        '''
        Args: clock_state: can either be 0, meaning off, or 1 meaning on
        Return: -2 if unable to check tick, -1 if clock is in an undesirable state, 0 if clock is in desired state
        '''
        try:
            tmp_second = self.second 
            time.sleep(5)
            time_diff = self.second - tmp_second
            if clock_state == 1:
                if time_diff > 0:
                    print("Success: Clock is Ticking")
                    return 0
                else:
                    print("Fail: Clock is not ticking")
                    return -1
            elif clock_state == 0:
                if time_diff == 0:
                    print("Success: Clock is not Ticking")
                    return 0
                else:
                    print("Fail: Clock is still ticking")
                    return -1
        except:
            raise Exception("Unable to Check clock tick")

    def __init__(self, battery_state, clock_state):
        '''
        Initialization of RTC class
        
        Args:
            battery_state: 0 = backup battery off, 1 = backup battery on
            clock_state: 0 = clock off, 1 = clock on
        '''
        self.battery = battery_state 
        self.clock = clock_state 

    def reset(self):
        '''
        Reset the clock's time to zero, and battery to zero 

        Returns:
            -1: The RTC was unable to be reset
            0: The RTC was able to be reset
        '''
        for self.rtc_register in self.registers:
            try:
                self.current_time = 0
                self.battery = 0
            except:
               print("Unable to reset RTC") 
               return -1
        return 0   
    
    def __encode(self,value):
        '''
        Encodes integer values into binary for the RTC's registers 
        
        Returns:
            Bit encoding for RTC registers       
        '''
        ones = value % 10
        tens = int(value / 10)
        return (tens<<4 | ones)

    @property
    def clock(self):
        '''
        Get state of the internal oscillator of the RTC. This will control if the clock is ticking or not

        Return:
            0: Clock = OFF
            1: Clock = ON
        '''
        try:# if check_device_status is bad 
            second_data = self.i2c_bus.read_byte_data(self.registers['slave'],self.registers['second'])
        except:
            raise Exception("Could not get clock state")
        return second_data >> 7 #Should return a 1 or a 0 (on or off)

    @clock.setter
    def clock(self,state):
        '''
        Set state of the internal oscillator of the RTC. This will control if the clock is ticking or not

        Args:
            State: 0 = Clock is OFF, 1 = Clock is ON
        '''
        second_data = self.i2c_bus.read_byte_data(self.registers['slave'],self.registers['second'])
        if state == 1:
            second_data = 0b10000000 | second_data
        elif state == 0:
            second_data = 0b01111111 & second_data
        else:
            raise Exception(f"Unable to set Clock. State entered must be 0 or 1, not {state}")
        self.i2c_bus.write_byte_data(self.registers['slave'],self.registers['second'],second_data)
        self.__check_tick(state)

    @property
    def battery(self):
        '''
        Get state of the backup battery of the RTC. This will control if the backup battery or not

        Return:
            0: Battery = OFF
            1: Battery = ON
        '''
        try:
            tmp_battery = self.i2c_bus.read_byte_data(self.registers['slave'],self.registers['wkday'])
            return  (tmp_battery & 0b1000)>>3
        except:
            raise Exception("Unable to get Battery State")

    @battery.setter
    def battery(self,state):
        '''
        Set state of the backup battery of the RTC. This will control if the backup battery or not

        Args:
            state: 0 = Battery is OFF, 1 = Battery is ON
        '''
        try:
            if not (state == 0 or state == 1):
                raise Exception("Not valid value for battery, must be 0 (OFF) or 1 (ON)") 
            tmp_battery = self.i2c_bus.read_byte_data(self.registers['slave'],self.registers['wkday'])
            if state == 0:
                tmp_battery = tmp_battery & 0b11110111
            else:
                tmp_battery = tmp_battery | 0b1000
            self.i2c_bus.write_byte_data(self.registers['slave'],self.registers['wkday'],tmp_battery)
        except:
            raise Exception("Unable to Set Battery")

    @property
    def second(self):
        '''
        Get seconds value from RTC register

        Return:
            Integer representing seconds data
        '''
        try:
            tmp_second = self.i2c_bus.read_byte_data(self.registers['slave'],self.registers['second'])
            tmp_second = tmp_second & 0b01111111 #Remove the start oscillation bit
            return (tmp_second>>4)*10 + (tmp_second & 0b00001111) 
        except:
            print("Unable to Get Second")

    @second.setter
    def second(self,value):
        '''
        Set seconds value from RTC register

        Args:
            Value: Integer value to set the seconds register to
        '''
        try:
            self.__verify_date("second",value)
            tmp_second = self.i2c_bus.read_byte_data(self.registers['slave'],self.registers['second']) & 0b10000000
            #^^^ could be replaced by clock_status()
            tmp_second = tmp_second | self.__encode(value)
            self.i2c_bus.write_byte_data(self.registers['slave'],self.registers['second'],tmp_second)
        except:
            print("Unable to Set second")

    @property
    def minute(self):

        '''
        Get minute value from RTC register

        Return:
            Integer representing minute data
        '''
        try:
            tmp_minute =  self.i2c_bus.read_byte_data(self.registers['slave'],self.registers['minute'])
            tmp_minute = tmp_minute & 0b01111111 #Remove uninitialized bit 
            return (tmp_minute >>4)*10 + (tmp_minute & 0b00001111) 
        except:
            print("Unable to Get minute")

    @minute.setter
    def minute(self,value):
        '''
        Set minutes value from RTC register

        Args:
            Value: Integer value to set the minutes register to, must be eligible minute value (1-60)
        '''
        try:
            self.__verify_date("minute",value)
            self.i2c_bus.write_byte_data(self.registers['slave'],self.registers['minute'],self.__encode(value) )
        except:
            print("Unable to set minute")

    @property
    def hour(self): # AM/PM untested stick to 24hr time
        '''
        Get hour value from RTC register

        Return:
            Integer representing hour data
        '''
        try:
            tmp_hour =  self.i2c_bus.read_byte_data(self.registers['slave'],self.registers['hour'])
            hour_format = tmp_hour >> 6 & 0x1
            if hour_format == 0:
                tmp_hour = ((tmp_hour>>4) & 0x03)*10 + (tmp_hour & 0x0F)
            else:
                tmp_hour = ((tmp_hour>>4) & 0x01)*10 + (tmp_hour & 0x0F)
                am_pm = (tmp_hour>>4) & 0x02
                if am_pm == 1:
                    am_pm = 'PM'
                else:
                    am_pm = 'AM'
                tmp_hour = str(tmp_hour) + am_pm 
            return(tmp_hour)
        except:
            print("Unable to get current hour")

    @hour.setter
    def hour(self,value):
        '''
        Set hour value from RTC register

        Args:
            Value: Integer value to set the hour register to, must be an eligible hour (1-60)
        '''
        try:
            self.__verify_date("hour",value)
            tmp_hour =  (self.i2c_bus.read_byte_data(self.registers['slave'],self.registers['hour']) & 0b11000000) | self.__encode(value)
            self.i2c_bus.write_byte_data(self.registers['slave'],self.registers['hour'],tmp_hour)
        except:
            print("Unable to Set Hours")

    @property
    def day(self):
        '''
        Get day value from RTC register

        Return:
            Integer representing day data
        '''
        try:
            tmp_days = self.i2c_bus.read_byte_data(self.registers['slave'],self.registers['day'])
            tmp_days = tmp_days & 0b00111111 #Remove unused bits 
            return (tmp_days >>4)*10 + (tmp_days & 0b00001111) 
        except:
            print("Unable to Get Days")

    @day.setter
    def day(self,value):
        '''
        Set day value from RTC register

        Args:
            Value: Integer value to set the day register to, must be an eligible amount for days in month
        '''
        try:
            self.__verify_date("day",value)
            self.i2c_bus.write_byte_data(self.registers['slave'],self.registers['day'],self.__encode(value))
        except:
            print("Unable to Set Days")

    @property
    def month(self):
        '''
        Get month value from RTC register
        1 -> January
        2 -> February
        3 -> March
        4 -> April
        5 -> May
        6 -> June
        7 -> July
        8 -> August
        9 -> September
        10 -> October
        11 -> November
        12 -> December

        Return:
            Integer representing month data
        '''
        try:
            tmp_months = self.i2c_bus.read_byte_data(self.registers['slave'],self.registers['month'])
            tmp_months = tmp_months & 0b00011111 #Remove unused bits 
            return (tmp_months >>4)*10 + (tmp_months & 0b00001111) 
        except:
            print("Unable to Get Days")

    @month.setter
    def month(self,value):
        '''
        Set month value from RTC register
        1 -> January
        2 -> February
        3 -> March
        4 -> April
        5 -> May
        6 -> June
        7 -> July
        8 -> August
        9 -> September
        10 -> October
        11 -> November
        12 -> December

        Args:
            Value: Integer value to set the month register to, must be an eligible month (1-12)
        '''
        try:
            self.__verify_date("month",value)
            tmp_month= self.__encode(value) | (self.i2c_bus.read_byte_data(self.registers['slave'],self.registers['month']) & 0b11100000)  
            self.i2c_bus.write_byte_data(self.registers['slave'],self.registers['month'],tmp_month)
        except:
            print("Unable to Set Month")

    @property
    def year(self):
        '''
        Get year value from RTC register

        Args:
            Value: Integer value to set the year register to, must be eligible value (0-99 which maps to 2000-2099) 
        '''
        try:
            tmp_years = self.i2c_bus.read_byte_data(self.registers['slave'],self.registers['year'])
            return (tmp_years >>4)*10 + (tmp_years & 0b00001111) + 2000 
        except:
            print("Unable to Get Year")

    @year.setter
    def year(self,value):
        '''
        Set year value from RTC register

        Args:
            Value: Integer value to set the year register to, must be eligible value (0-99 which maps to 2000-2099) 
        '''
        try:
            self.i2c_bus.write_byte_data(self.registers['slave'],self.registers['year'],self.__encode(value))
        except:
            print("Unable to Get Year")

    @property
    def current_time(self): #returns array in format [Second,Minute,Hour,Day,Month,Year]
        '''
        Get second,minute,hour,day,month and year values from RTC register

        Returns:
            Array of 6 integers in the form of [Second,Minute,Hour,Day,Month,Year]
        '''
        return  [self.second,self.minute,self.hour, self.day, self.month,self.year]

    @current_time.setter
    def current_time(self,value):
        '''
        Set second,minute,hour,day,month and year values from RTC register

        Args:
            Value: Array of 6 integers in the form of [Second,Minute,Hour,Day,Month,Year]
        
        Raises:
            Please enter a valid array in the format of [Second,Minute,Hour,Day,Month,Year]
        '''
        try:
            if len(value) != 6: raise Exception("Please enter a valid array in the format of [Second,Minute,Hour,Day,Month,Year]")
            self.second = value[0]
            self.minute = value[1]
            self.hour = value[2]
            self.day = value[3]
            self.month = value[4]
            self.year = value[5]
        except:
            print("Unable to Set Current Time")

    def __verify_date(self, time_unit, value):
        '''
        Verify that the value inputted is acceptable for that unit of time
        Second: 0-60
        Minute: 0-60
        Hour: 0-24 
        Day: 1-28/29/30/31 (month and leap year dependent)
        Month: 1-12
        Year: 0-99

        Args:
            time_type: String that can take on 1 of 6 values, 'second','minute','hour','day','month','year'
            value: Integer that must be valid 
        Raises:
            -{value}, is an invalid second value
            -{value}, is an invalid minute value
            -{value}, is an invalid hour value
            -{value}, is an invalid day value
            -{value}, is an invalid month value
            -{value}, is an invalid year value
            -Time Unit: {time_unit} not valid
        '''
        if (time_unit == "second"):
            if (value<0 or value>60 ): raise Exception (f"{value}, is an invalid second value") 
        elif (time_unit == "minute"):
            if (value<0 or value>60 ): raise Exception (f"{value}, is an invalid minute value") 
        elif (time_unit == "hour"):
            if (value<0 or value>24): raise Exception (f"{value}, is an invalid hour value") 
        elif (time_unit == "day"): # NEED TO FIX FOR ALL DAYS
            if (value<1 or value>31): raise Exception (f"{value}, is an invalid day value") 
        elif (time_unit == "month"):
            if (value<1 or value>12): raise Exception (f"{value}, is an invalid month value") 
        elif (time_unit == "year"):
            if (value<0 or value>99): raise Exception (f"{value}, is an invalid year value") 
        else:
            raise Exception (f"Time Unit: {time_unit} not valid")