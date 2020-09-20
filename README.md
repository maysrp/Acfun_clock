# Acfun_clock
ESP32 Micropython ESP32 Clock acfun fans clock


你的ESP32首先要刷好了Micropython固件


按照下图连线：  

|esp32 |    max7219  |
|----|----|
|5v（或者3v3）| vcc|  
|GND   |GND|  
|G27   |DIN|  
|G26  |CS|  
|G25| CLK|  


修改main.py的还有你的ACFUN的idWiFi名称和密码,  
上传到你的ESP32上
max7219.py这个库文件也上传到你的esp32上
你的acfun的时钟就完成了

## 存在的问腿
因为ACFUN没有固定的API,micropython不支持utf8的中文所以在无法显示粉丝大于10000的acer。
