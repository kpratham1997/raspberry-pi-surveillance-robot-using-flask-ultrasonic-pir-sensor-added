from flask import Flask, request, render_template, redirect, url_for, jsonify
import RPi.GPIO as GPIO
from time import sleep
import time


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

in1 = 27
in2 =6 
en = 22
temp1=1

in3 = 26
in4 = 13
enb = 19

global sensor
sensor=23

triggerPin = 4
echoPin = 17

GPIO.setup(triggerPin,GPIO.OUT)
GPIO.setup(echoPin,GPIO.IN)

GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(en,GPIO.OUT)

GPIO.setup(in3,GPIO.OUT)
GPIO.setup(in4,GPIO.OUT)
GPIO.setup(enb,GPIO.OUT)


GPIO.setup(sensor,GPIO.IN)

GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)

global p1
p1=GPIO.PWM(en,1000)
GPIO.output(in3,GPIO.LOW	)
GPIO.output(in4,GPIO.LOW)
global p2
p2=GPIO.PWM(enb,1000)


p1.start(25)
p2.start(25)
print("Initializing sensors")
time.sleep(12)
print("Waitng For Sensors To be ready")
	

app = Flask(__name__)

@app.route("/")
def index():
     return render_template('robo.html')

@app.route('/pirlistening', methods = ['GET','POST'])
def pirlistening():
    global distance 
    distance = 0
    while True:
	GPIO.output(triggerPin, False)
        time.sleep(2)                
	GPIO.output(triggerPin, True)
        time.sleep(0.00001)
        GPIO.output(triggerPin, False)  

	while GPIO.input(echoPin)==0:
            pulseStart = time.time()
   
        while GPIO.input(echoPin)==1:
            pulseEnd = time.time()
	            
        pulseDuration = pulseEnd - pulseStart
        
        distance = round(pulseDuration * 17150 , 2)
	       
	print(distance)
  	
    	if GPIO.input(sensor):
        	time.sleep(0.2)
		return jsonify({'mstatus':1,'distance':distance})
    	else:		
        	time.sleep(0.2)
		return jsonify({'mstatus':0,'distance':distance})                           #Delay of 2 seconds


@app.route('/left_side')
def left_side(): 
    p1.ChangeDutyCycle(90)
    p2.ChangeDutyCycle(90)
    GPIO.output(in3,GPIO.HIGH)
    GPIO.output(in4,GPIO.LOW) 
    return 'true'


@app.route('/right_side')
def right_side():
    p1.ChangeDutyCycle(90)
    p2.ChangeDutyCycle(90)
    GPIO.output(in1,GPIO.HIGH)
    GPIO.output(in2,GPIO.LOW)
    return 'true'

   
@app.route('/up_side')
def up_side():
   print("forward")
   p1.ChangeDutyCycle(90)
   p2.ChangeDutyCycle(90)
   GPIO.output(in1,GPIO.HIGH)
   GPIO.output(in2,GPIO.LOW)
   GPIO.output(in3,GPIO.HIGH)
   GPIO.output(in4,GPIO.LOW)        
   return 'true'

@app.route('/down_side')
def down_side():
   p1.ChangeDutyCycle(90)
   p2.ChangeDutyCycle(90)
   GPIO.output(in1,GPIO.LOW)
   GPIO.output(in2,GPIO.HIGH)
   GPIO.output(in3,GPIO.LOW)
   GPIO.output(in4,GPIO.HIGH) 
   return 'true'



@app.route('/stop')
def stop():
   p1.ChangeDutyCycle(0)
   p2.ChangeDutyCycle(0)
   GPIO.output(in1,GPIO.LOW)
   GPIO.output(in2,GPIO.LOW)
   GPIO.output(in3,GPIO.LOW)
   GPIO.output(in4,GPIO.LOW)        
   return 'true'

if __name__ == "__main__":
 print("Start")
 app.run(host='0.0.0.0',port=5000)