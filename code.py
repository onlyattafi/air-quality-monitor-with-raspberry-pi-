import time as t
import board as b
import busio as bu
import adafruit_ccs811 as cc
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306 as ssd
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from gpiozero import Buzzer,Button,TrafficLights
import Adafruit_DHT as dht
import matplotlib.pyplot as plt
DHT_SENSOR = dht.DHT22
DHT_PIN = 4
buzzer = Buzzer(17)
i2c = b.I2C()
ccs811 = cc.CCS811(i2c)
while not ccs811.data_ready:
    pass
RST = None
DC = 23
SPI.PORT = 0
SPI.DEVICE = 0
disp = ssd.SSD1306_128_64(rst=RST)
disp.begin()
disp.clear()
disp.display()
width = disp.width
height = disp.height
image = Image.new('1', (width, height))
draw = ImageDraw.Draw(image)
draw.rectangle((0, 0, width, height), outline=0, fill=0)
padding = -2
top = padding
bottom = height - padding
x = 0
font = ImageFont.truetype('Minecraftia-Regular.ttf', 13)
eco=[]
voc=[]
temp=[]
hum=[]
fich=open('project.txt','w')
fich.close()
while True:
    i=0
    while(i<=3600):
         humidity,temperature = adah.read_retry(DHT_SENSOR, DHT_PIN)
        eco2 = ccs811.eco2
        if(eco2==None):
            print("Failed getting CO2 value")
        eco.append(eco2)
        tvoc = ccs811.tvoc
        if (tvoc == None):
            print("Failed getting TVOC value")
        voc.append(tvoc)
        if ((int(eco2)>1000)and (int(eco2)<2000)):
            di=eco2*10
            di=int(di%10)
            draw.text((x, top + 20), "co2: " + str(eco2) + "." + str(di) + "ppm", font=font, fill=255)
            draw.text((x, top + 5), " The co2 is high, try opening the windows or leave the room.Or You will suffer from drowsiness!", font=font, fill=255)
            TrafficLights.lights.green.on()
            t.sleep(5)
        elif ((int(eco2)>2000)and (int(eco2)<5000)):
            di = eco2 * 10
            di = int(di % 10)
            draw.text((x, top + 20), "co2: " + str(eco2) + "." + str(di) + "ppm", font=font, fill=255)
            draw.text((x, top + 5), " Warning ! the co2 value is too much high, try opening the windows or leave the room.Or you will suffer from headaches, sleepiness, and stagnant, stale, stuffy air,Poor concentration, loss of attention, increased heart rate and slight nausea may also be present!", font=font, fill=255)
            TrafficLights.lights.amber.on()
            t.sleep(10)
        elif ((int(eco2) > 5000) and (int(eco2) <40000)):
            di = eco2 * 10
            di = int(di % 10)
            draw.text((x, top + 20), "co2: " + str(eco2) + "." + str(di) + "ppm", font=font, fill=255)
            draw.text((x, top + 5), " Warning ! the co2 value is too much high and unusual, try opening the windows or leave the room.An unusual air conditions,Toxicity or oxygen deprivation could occur! ", font=font, fill=255)
            TrafficLights.lights.amber.on()
            t.sleep(20)
            buzzer.on()
        elif (int(eco2) >40000):
            di = eco2 * 10
            di = int(di % 10)
            draw.text((x, top + 20), "co2: " + str(eco2) + "." + str(di) + "ppm", font=font, fill=255)
            draw.text((x, top + 5), " Danger !!! the co2 value is Dangerous and may harm you, so leave the room immediately!", font=font, fill=255)
            TrafficLights.lights.red.on()
            buzzer.on()
        if((int(tvoc)>500)and (int(tvoc)>1000)):
            di = eco2 * 10
            di = int(di % 10)
            draw.text((x, top + 20), "TVOC: " + str(eco2) + "." + str(di) + "ug/m3", font=font, fill=255)
            draw.text((x, top + 5), " the TVOC is Marginal.Complaints about irritation and discomfort are possible in sensitive individuals", font=font, fill=255)
        elif((int(tvoc>1000))and(int(tvoc>3000))):
            di = eco2 * 10
            di = int(di % 10)
            draw.text((x, top + 20), "TVOC: " + str(eco2) + "." + str(di) + "ug/m3", font=font, fill=255)
            draw.text((x, top + 5)," the TVOC is High.Irritation and discomfort are very likely", font=font, fill=255)
        elif (int(tvoc) >3000):
            di = eco2 * 10
            di = int(di % 10)
            draw.text((x, top + 20), "TVOC: " + str(eco2) + "." + str(di) + "ug/m3", font=font, fill=255)
            draw.text((x, top + 5), " the TVOC is Very High.Irritation and discomfort are very possible.", font=font, fill=255)
            TrafficLights.lights.red.on()
            buzzer.on()
        if humidity is not None and temperature is not None:
            temp.append(temperature)
            hum.append(humidity)
            draw.rectangle((0, 0, width, height), outline=0, fill=0)
            digit = temperature * 10
            digit = int(digit)% 10
            humidity = int(humidity)
            temperature = int(temperature)
            if(temperature<35):
                draw.text((x, top + 20), "T: " + str(temperature) + "." + str(digit) + "C", font=font, fill=255)
                TrafficLights.lights.green.on()
                t.sleep(5)
            elif (temperature>50):
                draw.text((x, top + 20), "T: " + str(temperature) + "." + str(digit) + "C", font=font, fill=255)
                TrafficLights.lights.red.on()
                buzzer.on()
            draw.text((x, top + 5), "Environment", font=font, fill=255)
            draw.text((x, top + 20), "T: " + str(temperature) + "." + str(digit) + "C", font=font, fill=255)
            draw.text((x + 64, top + 20), "H: " + str(humidity) + "%", font=font, fill=255)
            draw.text((x, top + 35), "CO2: " + str(eco2) + " PPM", font=font, fill=255)
            draw.text((x, top + 50), "TVOC: " + str(tvoc) + " PPB", font=font, fill=255)
            disp.image(image)
            disp.display()
        t.sleep(5)
        i+=5
    plt.plot(eco,i,color='#955500',marker='o',linestyle='dashed',linewidth=2,markersize=12)
    s=0
    k=0
    for j in voc:
        k+=1
        s+=j
    s/=k
    if (s<50):
        plt.plot(voc,i,color='8AC847',marker=',',linestyle='dashed',linewidth=2,markersize=12)
    elif((s>51)and(s<100)):
        plt.plot(voc,i,color='y',marker=',',linestyle='dashed',linewidth=2,markersize=12)
    elif ((s >101) and (s < 150)):
        plt.plot(voc,i,color='#FF6600',marker=',',linestyle='dashed',linewidth=2,markersize=12)
    elif ((s > 151) and (s < 200)):
        plt.plot(voc,i,color='r',marker=',',linestyle='dashed',linewidth=2,markersize=12)
    elif((s>201)and(s<300)):
        plt.plot(voc,i,color='m',marker=',',linestyle='dashed',linewidth=2,markersize=12)
    elif ((s >301) and (s < 500)):
        plt.plot(voc,i,color='k',marker=',',linestyle='dashed',linewidth=2,markersize=12)
    plt.plot(temp,i,color='b',marker='.',linestyle='dashed',linewidth=2,markersize=12)
    plt.plot(hum,i, color='#52A736', marker='*', linestyle='dashed', linewidth=2, markersize=12)
    fich=open('project.txt','a')
    fich.write('the Co2 values:'+str(eco)+'\n the TVOC values:'+str(voc)+'\n the Temperature values:'+str(temp)+'\n the humidity value:'+str(hum))
    fich.close()
