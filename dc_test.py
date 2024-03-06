import RPi.GPIO as GPIO
from time import sleep

# GPIO 모드 설정
GPIO.setmode(GPIO.BCM)

# 모터 제어 핀 설정
in1 = 24
in2 = 23
en = 25
GPIO.setup(in1, GPIO.OUT)
GPIO.setup(in2, GPIO.OUT)
GPIO.setup(en, GPIO.OUT)

GPIO.output(in1, GPIO.LOW)
GPIO.output(in2, GPIO.LOW)
p=GPIO.PWM(en, 1000) # PWM 신호를 1000Hz로 설정
p.start(25) # PWM 신호의 듀티 사이클을 25%로 시작 (속도 조절)

# 모터 제어 함수
def motor_forward():
    GPIO.output(in1, GPIO.HIGH)
    GPIO.output(in2, GPIO.LOW)
    print("모터 전진")

def motor_backward():
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.HIGH)
    print("모터 후진")

def motor_stop():
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.LOW)
    print("모터 정지")

try:
    motor_forward()
    sleep(5) # 5초 동안 전진
    motor_backward()
    sleep(5) # 5초 동안 후진
    motor_stop()

finally:
    p.stop()
    GPIO.cleanup() # GPIO 설정 초기화
