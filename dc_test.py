import RPi.GPIO as GPIO
from time import sleep

# GPIO 모드 설정
GPIO.setmode(GPIO.BCM)

# 모터1 제어 핀 설정
in1 = 17
in2 = 18
en = 27
GPIO.setup(in1, GPIO.OUT)
GPIO.setup(in2, GPIO.OUT)
GPIO.setup(en, GPIO.OUT)

# 모터2 제어 핀 설정
in3 = 10
in4 = 9
en2 = 25 
GPIO.setup(in3, GPIO.OUT)
GPIO.setup(in4, GPIO.OUT)
GPIO.setup(en2, GPIO.OUT)

# PWM 설정
p1 = GPIO.PWM(en, 1000)  # 모터1 PWM 신호를 1000Hz로 설정
p2 = GPIO.PWM(en2, 1000)  # 모터2 PWM 신호를 1000Hz로 설정
p1.start(100)  # 모터1 PWM 신호의 듀티 사이클을 100%로 시작
p2.start(100)  # 모터2 PWM 신호의 듀티 사이클을 100%로 시작

# 모터1 제어 함수
def motor1_forward():
    GPIO.output(in1, GPIO.HIGH)
    GPIO.output(in2, GPIO.LOW)
    print("모터1 전진")

def motor1_backward():
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.HIGH)
    print("모터1 후진")

def motor1_stop():
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.LOW)
    print("모터1 정지")

# 모터2 제어 함수
def motor2_forward():
    GPIO.output(in3, GPIO.HIGH)
    GPIO.output(in4, GPIO.LOW)
    print("모터2 전진")

def motor2_backward():
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in4, GPIO.HIGH)
    print("모터2 후진")

def motor2_stop():
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in4, GPIO.LOW)
    print("모터2 정지")

try:
    motor1_forward()
    motor2_forward()
    sleep(5)  # 5초 동안 모터1과 모터2 전진
    motor1_backward()
    motor2_backward()
    sleep(5)  # 5초 동안 모터1과 모터2 후진
    motor1_stop()
    motor2_stop()

finally:
    p1.stop()
    p2.stop()
    GPIO.cleanup()  # GPIO 설정 초기화
