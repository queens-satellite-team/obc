#Maintainer Harrison Gordon
import time
from   smbus import SMBus
import datetime

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
        'wkday' : 0x3, #Register only utilized by battery
        'day' : 0x04,
        'month': 0x05,
        'year' : 0x06
    }

    @staticmethod
    def status_verbose():
        if self.status_code:
            return "Unable to Communicate with Device"
        else:
            return "System is OK"

    @staticmethod
    def _encode(value):
        """Encodes integer values into binary for the RTC's registers

        Args:
            value (int): value to be encoded

        Returns:
            int: Encoded value to be used by RTC registers
        """
        ones = value % 10
        tens = int(value / 10)
        return (tens<<4 | ones)

    def _check_tick(self,clock_state):
        """Verify that the clock is acting im accordance to it's desired state

        Args:
            clock_state (bool): State of clock (0=OFF,1=ON)

        Returns:
            int : -1 if clock is in an undesirable state, 0 if clock is in desired state
        """
        second_start = self._second
        time.sleep(3)
        time_diff = self._second - second_start
        if clock_state == 1:
            if time_diff > 0:
                return 0
            else:
                return -1
        elif clock_state == 0:
            if time_diff == 0:
                return 0
            else:
                return -1

    def __init__(self, battery_state, clock_state,i2c_status):
        """Initialization of RTC class

        Args:
            battery_state (boolean): 0 = backup battery off, 1 = backup battery on
            clock_state (boolean): clock off, 1 = clock on

        Raises:
            RuntimeError: Initial communication failed, please verify setup.
        """
        try:
            self._second
        except:
            raise RuntimeError("Initial communication failed, please verify setup.")
        self.battery = battery_state
        self.clock = clock_state
        self.i2c_status = i2c_status

    def reset(self):
        """Reset the clock's time to 0:0:0 January 1 2000, battery to zero, and stop clock"""
        self.datetime = "0-1-1-0-0-0"
        self.battery = 0
        self.clock = 0
        self.i2c_status = 0

    @property
    def clock(self):
        """Get state of the internal oscillator of the RTC. This will control if the clock is ticking or not

        Returns:
            boolean :State of clock 0 = OFF , 1 = ON
        """
        second_raw = self.i2c_bus.read_byte_data(self.registers['slave'],self.registers['second'])
        return second_raw >> 7 #Should return a 1 or a 0 (on or off)

    @clock.setter
    def clock(self,state):
        """Set state of the internal oscillator of the RTC. This will control if the clock is ticking or not

        Args:
            state (boolean): 0 = Turn clock off, 1 = Turn clock on

        Raises:
            ValueError: f"Unable to set Clock. Invalid state:{state}"
            RuntimeError: "Clock unable to stop"
            RuntimeError: "Clock unable to start"
        """
        second_raw = self.i2c_bus.read_byte_data(self.registers['slave'],self.registers['second'])
        if state == 1:
            clock_state = 0b10000000 | second_raw
        elif state == 0:
            clock_state = 0b01111111 & second_raw
        else:
            raise ValueError(f"Unable to set Clock. Invalid state:{state}")
        self.i2c_bus.write_byte_data(self.registers['slave'],self.registers['second'],clock_state)
        if (self._check_tick(state) == -1):
            if state == 0:
                raise RuntimeError("Clock unable to Stop")
            if state == 1:
                raise RuntimeError("Clock unable to Start")

    @property
    def battery(self):
        """Get state of the backup battery of the RTC. This will control if the backup battery or not

        Raises:
            RuntimeError: "Unable to get Battery State"

        Returns:
            int : State of backup battery, 0=OFF, 1=ON
        """
        try:
            weekday_raw = self.i2c_bus.read_byte_data(self.registers['slave'],self.registers['wkday'])
            return  (weekday_raw & 0b1000)>>3
        except:
            raise RuntimeError("Unable to get Battery State")

    @battery.setter
    def battery(self,state):
        """Set state of the backup battery of the RTC. This will control if the backup battery or not

        Args:
            state (bool): 0 = Turn off backup battery, 1 = Turn on backup battery

        Raises:
            RuntimeError: Invalid state: {state}
            RuntimeError: Unable to Set Battery
        """
        if not (state == 0 or state == 1):
            raise RuntimeError(f"Invalid state: {state}")
        try:
            weekday_raw = self.i2c_bus.read_byte_data(self.registers['slave'],self.registers['wkday'])
            if state == 0:
                battery_state = weekday_raw& 0b11110111
            else:
                battery_state = weekday_raw | 0b1000
            self.i2c_bus.write_byte_data(self.registers['slave'],self.registers['wkday'],battery_state)
        except:
            raise RuntimeError("Unable to Set Battery")

    @property
    def _second(self):
        """Get seconds value from RTC register

        Raises:
            RuntimeError: Unable to Get Second

        Returns:
            int : "Unable to Get Second"
        """
        try:
            second_raw = self.i2c_bus.read_byte_data(self.registers['slave'],self.registers['second'])
            second_raw = second_raw & 0b01111111 #Remove the start oscillation bit
            return (second_raw>>4)*10 + (second_raw & 0b00001111)
        except:
            raise RuntimeError("Unable to Get Second")

    @_second.setter
    def _second(self,value):
        """Set value of second RTC register

        Args:
            value (int): set to valid second (0-60)

        Raises:
            RuntimeError: _description_
        """
        try:
            second_encoded = self.clock << 7 | RTC._encode(value)
            self.i2c_bus.write_byte_data(self.registers['slave'],self.registers['second'],second_encoded)
        except:
            raise RuntimeError("Unable to Set Second")

    @property
    def _minute(self):
        """Get value from minute RTC register

        Raises:
            RuntimeError: "Unable to Get Minute"

        Returns:
            int : decoded minute value
        """
        try:
            minute_raw =  self.i2c_bus.read_byte_data(self.registers['slave'],self.registers['minute'])
            minute_raw &=  0b01111111 #Remove uninitialized bit
            return (minute_raw >>4)*10 + (minute_raw & 0b00001111)
        except:
            raise RuntimeError("Unable to Get Minute")

    @_minute.setter
    def _minute(self,value):
        """Set minute RTC register

        Args:
            value (int): set a valid minute (0-60)

        Raises:
            RuntimeError: "Unable to Set Minute"
        """
        try:
            minute_encoded = RTC._encode(value)
            self.i2c_bus.write_byte_data(self.registers['slave'],self.registers['minute'], minute_encoded)
        except:
            raise RuntimeError("Unable to Set Minute")

    @property
    def _hour(self):
        """Get value from hour RTC register

        Raises:
            RuntimeError: "Unable to Get Hour"

        Returns:
            int : decoded hour value
        """
        try:
            hour_raw =  self.i2c_bus.read_byte_data(self.registers['slave'],self.registers['hour'])
            hour = ((hour_raw>>4) & 0x03)*10 + (hour_raw & 0x0F)
            return(hour)
        except:
            raise RuntimeError("Unable to Get Hour")

    @_hour.setter
    def _hour(self,value):
        """Set hour value from RTC register

        Args:
            value (int): set a valid hour value (0-24)

        Raises:
            RuntimeError: "Unable to Set Hours"
        """
        try:
            hour_encoded =  (self.i2c_bus.read_byte_data(self.registers['slave'],self.registers['hour']) & 0b1 << 7 ) | RTC._encode(value)
            self.i2c_bus.write_byte_data(self.registers['slave'],self.registers['hour'],hour_encoded)
        except:
            raise RuntimeError("Unable to Set Hours")

    @property
    def _day(self):
        """Get value from day RTC register

        Raises:
            RuntimeError: "Unable to Get Days"

        Returns:
            int : decoded day value
        """
        try:
            day_raw = self.i2c_bus.read_byte_data(self.registers['slave'],self.registers['day'])
            day_raw &= 0b00111111 #Remove unused bits
            return (day_raw>>4)*10 + (day_raw & 0b00001111)
        except:
            raise RuntimeError("Unable to Get Days")

    @_day.setter
    def _day(self,value):
        """Set value in day RTC register

        Args:
            value (int): set the month register to an eligible day

        Raises:
            RuntimeError: "Unable to Set Days"
        """
        try:
            day_encoded = RTC._encode(value)
            self.i2c_bus.write_byte_data(self.registers['slave'],self.registers['day'],day_encoded)
        except:
            raise RuntimeError("Unable to Set Days")

    @property
    def _month(self):
        """Get month value from RTC register
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

        Raises:
            RuntimeError: "Unable to Get Month"

        Returns:
            int : Decoded month value
        """
        try:
            month_raw = self.i2c_bus.read_byte_data(self.registers['slave'],self.registers['month'])
            month_raw &= 0b00011111 #Remove unused bits
            return (month_raw >> 4)*10 + (month_raw & 0b00001111)
        except:
            raise RuntimeError("Unable to Get Month")

    @_month.setter
    def _month(self,value):
        """Set value of month RTC register
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
            value (int): set the month register to an eligible month (1-12)

        Raises:
            RuntimeError: "Unable to Set Month"
        """
        try:
            month_encoded = RTC._encode(value) | (self.i2c_bus.read_byte_data(self.registers['slave'],self.registers['month']) & 0b11100000)
            self.i2c_bus.write_byte_data(self.registers['slave'],self.registers['month'],month_encoded)
        except:
            raise RuntimeError("Unable to Set Month")

    @property
    def _year(self):
        """Get value from year RTC register

        Raises:
            RuntimeError:  "Unable to Get Year"

        Returns:
            _type_: The decoded year value
        """
        try:
            year_raw = self.i2c_bus.read_byte_data(self.registers['slave'],self.registers['year'])
            return (year_raw >> 4)*10 + (year_raw & 0b00001111) + 2000
        except:
            raise RuntimeError("Unable to Get Year")

    @_year.setter
    def _year(self,value):
        """Set year RTC register

        Args:
            value (_type_): Integer value to set the year register to, must be eligible value (0-99 which maps to 2000-2099)

        Raises:
            RuntimeError: "Unable to Get Year"
        """
        try:
            value -= 2000
            self.i2c_bus.write_byte_data(self.registers['slave'],self.registers['year'],RTC._encode(value))
        except:
            raise RuntimeError("Unable to Get Year")

    @property
    def datetime(self):
        """Get Current datetime from RTC

        Returns:
            string: datetime in format year-month-day-hour-minute-second
        """
        return f"{self._year}-{self._month}-{self._day}-{self._hour}-{self._minute}-{self._second}"

    @datetime.setter
    def datetime(self,datetime_raw):
        """Checks if datetime_raw entered is valid datetime. Sets the datetime of the RTC in terms of years, months, days, hours, minutes, and seconds

        Args:
            datetime_raw (string): datetime in format "%Y-%m-%d %H:%M:%S"

        Raises:
            RuntimeError: f"Invalid datetime: {datetime_raw}"
        """
        try:
            datetime_split = datetime_raw.split('-')
            datetime_split = [int(i) for i in datetime_split]
            datetime.datetime(datetime_split[0],datetime_split[1],datetime_split[2],datetime_split[3],datetime_split[4],datetime_split[5],0)
        except:
            raise RuntimeError(f"Invalid datetime: {datetime_raw}")
        try:
            self._second = datetime_split[5]
            self._minute = datetime_split[4]
            self._hour = datetime_split[3]
            self._day = datetime_split[2]
            self._month = datetime_split[1]
            self._year = datetime_split[0]
            self.i2c_status = 0
        except:
            self.i2c_status = 1
