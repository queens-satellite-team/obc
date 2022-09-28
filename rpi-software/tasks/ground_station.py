"""
QSAT Communications Team 
Implementation of a Ground Station Control Panel for the QSAT Moc-Sat

The main objective of this module includes: 
    1. To have a GUI to choose from a list of commands 
    2. Easy communication to a connected Transmitting Radio (Arduino and RF24, or STM32 and CC1120)
    3. See progress of incoming data and have a log of previously sent commands and received data. 
"""
####################################################################
########################### USER CONFIG ############################
####################################################################

outfile = "/moc-sat/src/comms_msat/imgs/received.png"
infile = "/moc-sat/src/comms_msat/imgs/sent.png"
portname = "/dev/cu.usbserial-1410"  # for arduino nano on mac
# portname = "/dev/cu.usbmodem14101"    # for arduino uno on mac

####################################################################
############################# IMPORTS ##############################
####################################################################

from tkinter import Menu, HORIZONTAL
from tkinter import scrolledtext
from tkinter.ttk import Progressbar
import tkinter as tk
from datetime import datetime
import serial
import sys
import time
import base64

####################################################################
############################# GLOBALS ##############################
####################################################################
startMarker = "<"
endMarker = ">"
dataStarted = False
newCMD = False
dataBuf = ""
img_string = ""
messageComplete = False
pack_size = 32
start = 0
stop = pack_size

####################################################################
####################### CONTROL SUBROUTINES ########################
####################################################################
def setupSerial(baudRate, serialPortName):

    global serialPort

    serialPort = serial.Serial(
        port=serialPortName, baudrate=baudRate, timeout=0, rtscts=True
    )

    print("Serial port " + serialPortName + " opened  Baudrate " + str(baudRate))

    waitForArduino()


def arduinoACK():
    msg = ""
    while msg.find("XXX") == 0:
        msg = recvLikeArduino()
        if msg == "success":
            print(msg)
            return True
        elif msg == "failed":
            print(msg)
            return False


def waitForArduino():

    # wait until the Arduino sends 'Arduino is ready' - allows time for Arduino reset
    # it also ensures that any bytes left over from a previous message are discarded

    print("Waiting for Arduino to Reset...")

    msg = ""
    while msg.find("Arduino is ready") == -1:
        msg = recvLikeArduino()
        if not (msg == "XXX"):
            print(msg)


def recvLikeArduino():

    global startMarker, endMarker, serialPort, dataStarted, dataBuf, messageComplete

    if serialPort.inWaiting() > 0 and messageComplete == False:
        x = serialPort.read().decode("utf-8")  # decode needed for Python3
        x = x.rstrip("\r\n")

        if dataStarted == True:
            if x != endMarker:
                dataBuf = dataBuf + x
            else:
                dataStarted = False
                messageComplete = True
        elif x == startMarker:
            dataBuf = ""
            dataStarted = True

    if messageComplete == True:
        messageComplete = False
        return dataBuf
    else:
        return "XXX"


def sendToArduino(stringToSend):

    # this adds the start- and end-markers before sending
    global startMarker, endMarker, serialPort

    stringWithMarkers = startMarker
    stringWithMarkers += stringToSend
    stringWithMarkers += endMarker

    if serialPort.write(stringWithMarkers.encode("utf-8")):  # encode needed for Python3
        print("Success: Sent a packet to Arduino.")
    else:
        print("Error: Could not write to Arduino.")


def imageToCharacters(file):

    # encode bytes in file to base64 characters
    global img_chars, nchars

    with open(file, mode="rb") as image:
        img_encoded = base64.b64encode(image.read())
        if img_encoded:
            print("Image file successfully encoded.")
        else:
            print("Error: image file did not encode.")

        img_chars = img_encoded.decode("utf-8")
        if img_chars:
            print("Encoded image succefullly converted to utf-8 string.")
        else:
            print("Error: Encoded image did not convert to utf-8 string.")

        nchars = len(img_chars)
        print("Encoded Image is " + str(nchars) + " characters long.")


def createPack():

    global img_chars, start, stop, pack_size

    pack = img_chars[start:stop]

    if pack:
        print("Success: Pack succesfully created.")
        start += pack_size
        stop += pack_size
    else:
        print("Error: pack not created.")
        return

    return pack


####################################################################
############################## GUI #################################
####################################################################
class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("MOC SAT Ground Station")
        self.master.geometry("1024x564")  # width x height
        self.create_widgets()

    def enter_cmd(self):
        self.log_text_box.configure(state="normal")
        self.log_text_box.insert("end", "\n")
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        self.log_text_box.insert("end", current_time + "\n")

        self.log_text_box.insert(
            "end", "Implenting Command: " + self.cmd_variable.get() + "\n"
        )
        if self.cmd_variable.get() == cmd_List[0]:
            self.log_text_box.insert(
                "end", "Angle Sent: " + self.angle_entry.get() + "\n"
            )
            print(self.angle_entry.get())
        self.log_text_box.configure(state="disabled")

        if self.cmd_variable.get() == cmd_List[0]:
            self.cmd_one()
        elif self.cmd_variable.get() == cmd_List[1]:
            self.cmd_two()
        elif self.cmd_variable.get() == cmd_List[2]:
            self.cmd_three()

    def clear_text_cmd(self):
        self.log_text_box.configure(state="normal")
        self.log_text_box.delete("1.0", tk.END)
        self.log_text_box.configure(state="disabled")

    def update_add_frame(self, cmd):
        if self.cmd_variable.get() == cmd_List[0]:

            self.add_data_frame.config(text="Send Data")

            for widget in self.add_data_frame.winfo_children():
                widget.destroy()

            ### ADDITIONAL DATA FRAME -- ANGLE LABEL ###
            self.angle_label = tk.Label(self.add_data_frame, text="Angle: ")
            self.angle_label.config(font=("Courier", 12))
            self.angle_label.grid(row=0, column=0, sticky="W", padx=8, pady=4)

            ### ADDITIONAL DATA FRAME -- ANGLE ENTRY ###
            self.angle_entry = tk.Entry(self.add_data_frame, width=20)
            self.angle_entry.grid(row=0, column=1, sticky="W", padx=8, pady=4)

            ### ADDITIONAL DATA FRAME -- ENTER BUTTON ###
            self.enter = tk.Button(
                self.add_data_frame, text="Enter", fg="green", command=self.enter_cmd
            )
            self.enter.grid(row=2, column=0, sticky="W", padx=8, pady=4)

        elif self.cmd_variable.get() == cmd_List[1]:

            self.add_data_frame.config(text="Current Health Status")

            for widget in self.add_data_frame.winfo_children():
                widget.destroy()

            ### ADDITIONAL DATA FRAME -- VOLTAGE LEVEL LABEL ###
            self.voltage_label = tk.Label(self.add_data_frame, text="Battery Voltage: ")
            self.voltage_label.config(font=("Courier", 12))
            self.voltage_label.grid(row=0, column=0, sticky="W", padx=8, pady=4)

            ### ADDITIONAL DATA FRAME -- VOLTAGE LEVEL ENTRY ###
            self.voltage_text_box = tk.Text(self.add_data_frame)
            self.voltage_text_box.config(
                font=("Courier", 12), width=10, height=1, state="disabled"
            )
            self.voltage_text_box.grid(row=0, column=1, sticky="W", padx=8, pady=4)

            ### ADDITIONAL DATA FRAME -- CURRENT LEVEL LABEL ###
            self.current_label = tk.Label(self.add_data_frame, text="Battery Current: ")
            self.current_label.config(font=("Courier", 12))
            self.current_label.grid(row=1, column=0, sticky="W", padx=8, pady=4)

            ### ADDITIONAL DATA FRAME -- CURRENT LEVEL ENTRY ###
            self.current_text_box = tk.Text(self.add_data_frame)
            self.current_text_box.config(
                font=("Courier", 12), width=10, height=1, state="disabled"
            )
            self.current_text_box.grid(row=1, column=1, sticky="W", padx=8, pady=4)

            ### ADDITIONAL DATA FRAME -- INTERNAL HEAT LABEL ###
            self.temp_label = tk.Label(self.add_data_frame, text="Satellite Temp: ")
            self.temp_label.config(font=("Courier", 12))
            self.temp_label.grid(row=2, column=0, sticky="W", padx=8, pady=4)

            ### ADDITIONAL DATA FRAME -- INTERNAL HEAT ENTRY ###
            self.temp_text_box = tk.Text(self.add_data_frame)
            self.temp_text_box.config(
                font=("Courier", 12), width=10, height=1, state="disabled"
            )
            self.temp_text_box.grid(row=2, column=1, sticky="W", padx=8, pady=4)

            ### ADDITIONAL DATA FRAME -- UPDATE HEALTH VALUES BUTTON ###
            self.enter = tk.Button(
                self.add_data_frame, text="Update", fg="green", command=self.enter_cmd
            )
            self.enter.grid(row=3, column=0, sticky="W", padx=8, pady=4)

        elif self.cmd_variable.get() == cmd_List[2]:

            self.add_data_frame.config(text="Confirm Reboot")

            for widget in self.add_data_frame.winfo_children():
                widget.destroy()

            ### ADDITIONAL DATA FRAME -- CONFIRM BUTTON ###
            self.enter = tk.Button(
                self.add_data_frame, text="CONFIRM", fg="green", command=self.enter_cmd
            )
            self.enter.grid(row=0, column=0, sticky="N", padx=8, pady=4)

    def create_widgets(self):
        ### TITLE ###
        self.title = tk.Label(text="MOC-SAT Control Panel")
        self.title.config(font=("Courier", 32))
        self.title.grid(row=0, sticky="N", padx=8, pady=4)

        ### COMMAND OPTION FRAME ###
        self.cmd_frame = tk.LabelFrame(self.master, text="Command Options")
        self.cmd_frame.config(font=("Courier", 22))
        self.cmd_frame.grid(row=1, column=0, padx=8, pady=4, sticky="nw")

        ### RECEIVED DATA FRAME ###
        self.recv_frame = tk.LabelFrame(self.master, text="Received Data")
        self.recv_frame.config(font=("Courier", 22))
        self.recv_frame.grid(row=1, column=1, rowspan=2, padx=8, pady=4, sticky="ne")

        ### ADDITIONAL DATA FRAME ###
        self.add_data_frame = tk.LabelFrame(self.master)
        self.add_data_frame.config(font=("Courier", 22))
        self.add_data_frame.grid(row=2, column=0, padx=8, pady=4, sticky="nw")

        ### PROGRESS BAR FRAME ###
        self.progress_bar_frame = tk.LabelFrame(
            self.master, text="Received Data Progress"
        )
        self.progress_bar_frame.config(font=("Courier", 22))
        self.progress_bar_frame.grid(row=3, columnspan=2, padx=8, pady=4, sticky="nw")

        ### COMMAND OPTION FRAME -- HEADER ###
        self.cmd_heading = tk.Label(self.cmd_frame, text="Choose a Command:")
        self.cmd_heading.config(font=("Courier", 16))
        self.cmd_heading.grid(row=0, column=0, sticky="W", padx=8, pady=4)

        ### COMMAND OPTION FRAME -- OPTION MENU ###
        global cmd_List
        cmd_List = ("Retrieve Image", "Retrieve System Health", "Reboot Satellite")
        self.cmd_variable = tk.StringVar()
        self.cmd_variable.set(cmd_List[0])
        self.cmd_option_menu = tk.OptionMenu(
            self.cmd_frame, self.cmd_variable, *cmd_List, command=self.update_add_frame
        )
        self.cmd_option_menu.grid(row=1, column=0, sticky="W", padx=8, pady=4)

        ### RECEIVED DATA FRAME -- HEADER ###
        self.recv_header = tk.Label(self.recv_frame, text="Data Log")
        self.recv_header.config(font=("Courier", 16))
        self.recv_header.grid(row=0, column=0, sticky="W", padx=8, pady=4)

        ### RECEIVED DATA FRAME -- TEXTBOX ###
        self.log_text_box = tk.Text(self.recv_frame)
        self.log_text_box.config(font=("Courier", 14), width=50, height=20)
        self.log_text_box.grid(row=1, column=0, sticky="W", padx=8, pady=4)

        ### RECEIVED DATA FRAME -- CLEAR BUTTON ###
        self.clear_text_button = tk.Button(
            self.recv_frame, text="Clear", command=self.clear_text_cmd
        )
        self.clear_text_button.grid(row=2, column=0, sticky="W", padx=8, pady=4)

        ### PROGRRESS BAR FRAME ###
        self.progress = Progressbar(
            self.progress_bar_frame, orient=HORIZONTAL, length=900, mode="determinate"
        )
        self.progress.grid(row=0, column=0, sticky="N", padx=8, pady=4)

        ### MASTER FRAME -- QUIT BUTTON ###
        self.quit = tk.Button(
            self.master, text="Quit", fg="red", command=self.master.destroy
        )
        self.quit.grid(row=4, column=0, sticky="sw", padx=8, pady=4)

    def console_print(self, msg):
        self.log_text_box.configure(state="normal")
        self.log_text_box.insert("end", msg + "\n")
        self.log_text_box.configure(state="disabled")

    def receiveImage(self):
        # img_string starts off empty and gets appended to by the received data
        global img_string

        # receive the first packet
        arduinoReply = recvLikeArduino()

        # loop until we get the STOP message
        while arduinoReply.find("STOP") == -1:
            time.sleep(0.01)

            if arduinoReply.find("XXX") == 0:
                arduinoReply = recvLikeArduino()
                continue
            elif arduinoReply.find("failed") == 0:
                # if we receive an error, print the error, and try to get a new response
                self.console_print(
                    "Returned Message: {} at time {}.".format(arduinoReply, time.time())
                )
                arduinoReply = recvLikeArduino()
                continue
            elif arduinoReply.find("success") == 0:
                # if we read success in the received packet, append it to the img_string
                img_string = img_string + arduinoReply
                self.console_print(
                    "Returned Message: {} at time {}.".format(arduinoReply, time.time())
                )
                arduinoReply = recvLikeArduino()
                continue
            else:
                # if we receive anything else, just try again.
                arduinoReply = recvLikeArduino()
            # end_if
        # end_while

        # after receiving all the data packets encode string back into img file)
        img_bytes = img_string.encode("utf-8")
        if img_bytes:
            self.console_print(
                "Success: ASCII character string encoded to byte string."
            )
            img_64_decoded = base64.b64decode(img_bytes)

            if img_64_decoded:
                self.console_print(
                    "Success: stringToImage: Byte string decoded with base 64."
                )

                with open(outfile, mode="wb") as output:
                    output.write(img_64_decoded)
                    self.console_print("Ouput file: {} created.".format(outfile))
            else:
                self.console_print(
                    "Error: stringToImage: Byte string unable to decode with base 64."
                )
        else:
            self.console_print(
                "Error: stringToImage: Character string not converted to bytes string."
            )

    def receiveHealthData(self):
        pass

    def receiveRebootConfirmation(self):
        pass

    def cmd_one(self):
        """
        This command receives an image from the satellite's memory.
        The OP_code sent to the satellite is 1 and the angle given is attached to the command packet
        """
        # pad the provided angle
        angle = self.angle_entry.get()
        if len(angle) < 3:
            while len(angle) < 3:
                angle = "0" + angle
        else:
            angle = angle[0:2]

        # send the command to the arduino
        sendToArduino("cmd_1_" + angle)

        # update the user
        self.console_print("Waiting for Arduino...")

        # receive acknowledgement
        if arduinoACK():
            self.console_print("Sent Data Successfully.")
            # receive the image
            self.receiveImage()

            # terminate transeivers and return to idle state
            sendToArduino("cmd_0_000")

        else:
            self.console_print("Failed to Send Data.")

    def cmd_two(self):
        """
        This command gets the health values from a text file on the satellite
        The OP_code being sent is 2 and no other information is required to be sent along. 
        """

        # send the command to the arduino
        sendToArduino("cmd_2_000")

        # update the user
        self.console_print("Waiting for Arduino...")

        # receive acknowledgement
        if arduinoACK():
            self.console_print("Sent Data Successfully.")
            # begin receiving the data
            self.receiveHealthData()

            # terminate transeivers and return to idle state
            sendToArduino("cmd_0_000")

        else:
            self.console_print("Failed to Send Data.")

    def cmd_three(self):
        """
        This command reboots the satellite in case of a required update or to reestablish a connection. 
        For now, we are blinking LEDs on the satellite to confirm recognition. 
        The OP_code being sent is 3 and no other information is required to be sent along. 
        """

        # send the command to the arduino
        sendToArduino("cmd_3_000")

        # update the user
        self.console_print("Waiting for Arduino...")

        # receive acknowledgement
        if arduinoACK():
            self.console_print("Sent Data Successfully.")
            self.receiveRebootConfirmation()

            # terminate transeivers and return to idle state
            sendToArduino("cmd_0_000")
        else:
            self.console_print("Failed to Send Data.")


####################################################################
########################## MAIN WINDOW #############################
####################################################################
def main():
    setupSerial(9600, portname)
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()


if __name__ == "__main__":
    main()
