from bluepy.btle import Peripheral, UUID
from bluepy.btle import Scanner, DefaultDelegate
import globalv as gl
from pynput.mouse import Button, Controller
import threading

class MyDelegate(DefaultDelegate):

    def __init__(self):
        DefaultDelegate.__init__(self)
        self.state =0
        self.button1_handle =0
        self.button2_handle =0
    def handleNotification(self, cHandle, data):
        
        if (cHandle== self.button2_handle ):
            #print("button1")
            if self.state ==0:
                mouse = gl.get_value('mouse')
                mouse.press(Button.left)
                self.state =1
            elif self.state ==1 :
                self.state =0
                mouse = gl.get_value('mouse')
                mouse.release(Button.left)
        '''
        elif (cHandle== self.button1_handle ):
            continue
        '''    


## ble button setup

class ble_7697:
    def __init__(self):
        self.my_not = MyDelegate() 
        success = False
        while( not success):
            try:
                self.dev_button = Peripheral("31:ba:00:2b:88:8c", 'public')
                self.service_button = self.dev_button.getServiceByUUID("19B10010-E8F2-537E-4F6C-D104768A1214")
                self.button1 = self.service_button.getCharacteristics()[0]
                self.button2 = self.service_button.getCharacteristics()[1]
                self.my_not.button1_handle = self.button1.getHandle() 
                self.my_not.button2_handle = self.button2.getHandle()
                self.dev_button.setDelegate(self.my_not)
            except:
                success = False
            else:
                success = True
    def waitNot(self):
        while True:
            if self.dev_button.waitForNotifications(0.1):
                print("not")
            
