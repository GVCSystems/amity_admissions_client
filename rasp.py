
"""

Try7 - Display both waiting and attending
Try6 - working - display only waiting 

SetSerialPort - Choose first port with USB in it
Set variable SerialPortFound


ConnectDevice - send +++ and look for OK
if found set DeviceConnected to 1

ReadID
Send ATID <CR> and reply is put in ID

SaveID - send ATWR

Write ID -send ATID ID<CR>


def DisplayData ():
    x=serdev.read()
    print (format(ord(x),'02x')),
    

# Beginning of program
# first sense serial port
# and then capture data


while (True):
    CaptureData()

                     


"""


import Tkinter

import sys
 
import serial
import serial.tools.list_ports
import sys
import time

import os

global serdev,SerialPortFound,DeviceConnected,Debug,ID,TokenValue,Mode
global HeaderFound,TargetFound,RxBytes,Token,UnitNumber,Waiting,PreviousWaiting
global T1,T2,T3,T4,T5,T6,T7    


global tokens


root = Tkinter.Tk()

#root.state('zoomed')
PreviousWaiting=0

CABIN="#"
TOKEN="Token"

FT=90
FH=50
WID=5

#uncomment when running on RPi 
#FT=120;FH=100;WID=6;root.attributes('-fullscreen',True)

def SetSerialPort ():
    ###First part for initializing serial port
    global serdev,SerialPortFound,DeviceConnected
    global tokens
    portsList=list(serial.tools.list_ports.comports())
    totalPorts = len(portsList)
    if (Debug == 1):
        print ("Total Ports - ",totalPorts)
        print ("OS - ",sys.platform)
    #find port with USB in that
    USBPort="NULL"
    for x in range (0, totalPorts):
        if (Debug == 1):
            print  (portsList[x])
        if sys.platform.startswith('linux'):
            if (Debug == 1):
                print "linux"
            if ('USB' in portsList[x][0]):
                USBPort=portsList[x][0]
        elif sys.platform == "win32":
            if (Debug == 1):
                print "windows"
            if ('USB' in portsList[x][1]):
                USBPort=portsList[x][0]
                
    #USBPort has first usb serial ports
    #open that port
    if (USBPort == "NULL"):
        print ("NO serial Port")
        serdev = None
    else:
        print (USBPort)
        serdev = serial.Serial(USBPort,1200,timeout=0)
        if (Debug == 1):
            print serdev
        SerialPortFound = 1


def CaptureData ():
    global HeaderFound,TargetFound,RxBytes,Token,UnitNumber,Waiting,PreviousWaiting
    global T1,T2,T3,T4,T5,T6,T7,TokenValue,Mode
    AttendingColor="GREEN"
    WaitingColor="RED"
    #HeaderFound = 0
    #TargetFound = 0
    #RxBytes = 0;
    while (1):
        x=serdev.read()
        if len(x) == 0:
            break
        if RxBytes == 0 and ord(x) == 0x55:
            HeaderFound = 1
            TargetFound = 0
            RxBytes = 1;
        elif RxBytes == 1 and HeaderFound == 1:
            if ord(x) == 0x55:
                TargetFound = 1
                HeaderFound = 0
                RxBytes = 2
            else:
                TargetFound = 0
                HeaderFound = 0
                RxBytes = 0
        elif RxBytes == 2:
            RxBytes = 3
            print
            UnitNumber=ord(x)
            print(format(ord(x),'02x')),
        elif RxBytes == 3:
            if ord(x) >= 0x80:
                Mode = 1
                print ('B'),
            else:
                Mode = 0
                print (' '),
            RxBytes = 4    
        elif RxBytes == 4:
            if ord(x) == 0x00:
                print ("DISP"),
            elif ord(x) == 0x03:
                print ("SETM"),
            elif ord(x) == 0x06:
                print ("BUZZ"),
            else:
                print ("    "),
            RxBytes = 5
        elif RxBytes == 5:
            print (format(ord(x))),
            RxBytes = 6
            Waiting = ord(x)
        elif RxBytes == 6:
            Token = ord(x)
            RxBytes = 7
        elif RxBytes == 7:
            Token = Token * 256 + ord(x)
            print (Token),
            if (Token == 0): #or (Mode == 0):
                TokenValue = ''
            else:
                TokenValue = str(Token)
            RxBytes = 8
        elif RxBytes == 8:
            if UnitNumber == 1:
                T1Text.set(TokenValue)
                if (Mode == 0):
                    T1.config(foreground=AttendingColor)
                if (Mode == 1):
                    T1.config(foreground=WaitingColor)
            if UnitNumber == 2:
                T2Text.set(TokenValue)
                if (Mode == 0):
                    T2.config(foreground=AttendingColor)
                if (Mode == 1):
                    T2.config(foreground=WaitingColor)
            if UnitNumber == 3:
                T3Text.set(TokenValue)
                if (Mode == 0):
                    T3.config(foreground=AttendingColor)
                if (Mode == 1):
                    T3.config(foreground=WaitingColor)
            if UnitNumber == 4:
                T4Text.set(TokenValue)
                if (Mode == 0):
                    T4.config(foreground=AttendingColor)
                if (Mode == 1):
                    T4.config(foreground=WaitingColor)
            if UnitNumber == 5:
                T5Text.set(TokenValue)
                if (Mode == 0):
                    T5.config(foreground=AttendingColor)
                if (Mode == 1):
                    T5.config(foreground=WaitingColor)
            if UnitNumber == 6:
                T6Text.set(TokenValue)
                if (Mode == 0):
                    T6.config(foreground=AttendingColor)
                if (Mode == 1):
                    T6.config(foreground=WaitingColor)
            if UnitNumber == 7:
                T7Text.set(TokenValue)
                if (Mode == 0):
                    T7.config(foreground=AttendingColor)
                if (Mode == 1):
                    T7.config(foreground=WaitingColor)
                
            RxBytes=0    
            if Waiting > PreviousWaiting:
                PreviousWaiting=Waiting
                print(Waiting)
                WaitingText.set(str(Waiting))
                
        else:
            RxBytes = 0
    root.after(5,CaptureData)


print ("Start Program")
SerialPortFound = 0
DeviceConnected = 0
Debug = 0
SetSerialPort()
RxBytes = 0
TokenValue = ''

WaitingText = Tkinter.StringVar()

T1Text = Tkinter.StringVar()
T2Text = Tkinter.StringVar()
T3Text = Tkinter.StringVar()
T4Text = Tkinter.StringVar()
T5Text = Tkinter.StringVar()
T6Text = Tkinter.StringVar()
T7Text = Tkinter.StringVar()

T1Text.set

Tkinter.Label(root, text=CABIN, font=("Helvetica", FH+20),borderwidth=2, 
            width=2,height=1).grid(row=0,column=0)
Tkinter.Label(root, text=TOKEN, font=("Helvetica", FH),borderwidth=2, 
            width=6,height=1).grid(row=0,column=1)
Tkinter.Label(root, text=CABIN, font=("Helvetica", FH+20),borderwidth=2, 
            width=2,height=1).grid(row=0,column=2)
Tkinter.Label(root, text=TOKEN, font=("Helvetica", FH),borderwidth=2, 
            width=6,height=1).grid(row=0,column=3)

for r in range(4):
        Tkinter.Label(root, text=str(r+1), font=("Helvetica", FT),borderwidth=2, relief="groove",
            width=2,height=1).grid(row=r+1,column=0)
        if r < 3:
            Tkinter.Label(root, text=str(r+5), font=("Helvetica", FT),borderwidth=2, relief="groove",
            width=2,height=1).grid(row=r+1,column=2)
        else:
            Tkinter.Label(root, text=' ', font=("Helvetica", FT),borderwidth=2, relief="groove",
            width=2,height=1).grid(row=r+1,column=2)
             
T1 = Tkinter.Label(root, textvariable=T1Text, font=("Helvetica", FT),borderwidth=2, relief="groove",
            width=WID,height=1)
T1.grid(row=1,column=1)

T5 = Tkinter.Label(root, textvariable=T5Text, font=("Helvetica", FT),borderwidth=2, relief="groove",
            width=WID,height=1)
T5.grid(row=1,column=3)

T2 = Tkinter.Label(root, textvariable=T2Text, font=("Helvetica", FT),borderwidth=2, relief="groove",
            width=WID,height=1)
T2.grid(row=2,column=1)

T6 = Tkinter.Label(root, textvariable=T6Text, font=("Helvetica", FT),borderwidth=2, relief="groove",width=WID,height=1)
T6.grid(row=2,column=3)

T3 = Tkinter.Label(root, textvariable=T3Text, font=("Helvetica", FT),borderwidth=2, relief="groove",
            width=WID,height=1)
T3.grid(row=3,column=1)

T7 = Tkinter.Label(root, textvariable=T7Text, font=("Helvetica", FT),borderwidth=2, relief="groove",
            width=WID,height=1)
T7.grid(row=3,column=3)

T4 = Tkinter.Label(root, textvariable=T4Text, font=("Helvetica", FT),borderwidth=2, relief="groove",
            width=WID,height=1)
T4.grid(row=4,column=1)

CountWaiting = Tkinter.Label(root, text='', font=("Helvetica", FT),borderwidth=2, relief="groove",
            width=WID,height=1).grid(row=4,column=3)


root.after(20,CaptureData)        
root.mainloop()

 

