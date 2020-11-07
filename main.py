import time
import ntptime
import network
import max7219
import urequests
import gc,ure,ujson
from machine import Pin,SPI,RTC
class clock:
    def __init__(self):
        self.id="701353" #你的ACFUN的ID,目前只能在10000粉丝以下时候才能正常显示
        self.wifi="pangxh" #你的WiFi名，只支持2.4GHZ的wifi
        self.password="a12345678" #你的WiFi密码
        self.ntp()
        self.dp()
        self.se=0
        self.rtc=RTC()
        self.fans()
        self.acfun=[[4, 1], [12, 1], [13, 1], [14, 1], [4, 2], [12, 2], [3, 3], [5, 3], [9, 3], [10, 3], [12, 3], [16, 3], [19, 3], [21, 3], [22, 3], [23, 3], [24, 3], [3, 4], [5, 4], [8, 4], [12, 4], [13, 4], [14, 4], [16, 4], [19, 4], [21, 4], [24, 4], [3, 5], [4, 5], [5, 5], [8, 5], [12, 5], [16, 5], [19, 5], [21, 5], [24, 5], [2, 6], [6, 6], [8, 6], [12, 6], [16, 6], [19, 6], [21, 6], [24, 6], [2, 7], [6, 7], [9, 7], [10, 7], [12, 7], [16, 7], [17, 7], [18, 7], [19, 7], [21, 7], [24, 7]]
    def net(self):
        wlan = network.WLAN(network.STA_IF) 
        wlan.active(True) 
        if not wlan.isconnected(): 
            wlan.connect(self.wifi,self.password) 
    def dp(self):
        spi = SPI(baudrate=100000, polarity=1, phase=0, mosi=Pin(27),sck=Pin(25), miso=Pin(33))
        self.display = max7219.Matrix8x8(spi,Pin(26),4)
    def ntp(self):
        self.net()
        time.sleep(5)
        ntptime.host="ntp1.aliyun.com"
        ntptime.NTP_DELTA = 3155644800
        try:
            ntptime.settime()
        except Exception as e:
            pass
    def show_time(self):
        date=self.rtc.datetime()
        self.m=date[5]
        self.h=date[4]
        self.display.fill(0)
        self.display.text(str(self.h) if len(str(self.h))==2 else ' '+str(self.h) ,0,1,1)
        self.display.pixel(16,2,self.se)        
        self.display.pixel(16,4,self.se)        
        self.display.text(str(self.m) if len(str(self.m))==2 else '0'+str(self.m) ,17,1,1)
        self.se=0 if self.se==1 else 1
        self.display.show()
    def fans(self):
        gc.collect()    
        url="https://www.acfun.cn/rest/pc-direct/user/userInfo?userId="+str(self.id)
        headers = {'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Mobile Safari/537.36' }
        re=urequests.get(url,headers=headers)
        ca=re.text
        cc=ujson.loads(ca)
        if cc['result']==0:
            self.fan=cc['profile']['followed']
        else:
            self.fan='0'
    def show_myfans(self):
        for j in range(4):
            self.display.fill(0)
            for i in self.acfun:
                self.display.pixel(i[0]-8*j,i[1],1)
            self.display.text(str(self.fan),25-8*j,1,1)
            self.display.show()
            time.sleep(0.5)


Clock=clock()

oldM=0
while 1:
    Clock.show_time()
    time.sleep(1)
    Clock.show_myfans()
    if Clock.m!=oldM and Clock.m%5!=0:
        Clock.ntp()
        oldM=Clock.m
        Clock.fans()
