import RPi.GPIO as GPIO
from time import sleep

# GPIO 모드 설정
GPIO.setmode(GPIO.BCM)

# 모터1 제어 핀 설정
in1 = 17
in2 = 18
en1 = 27
GPIO.setup(in1, GPIO.OUT)
GPIO.setup(in2, GPIO.OUT)
GPIO.setup(en1, GPIO.OUT)

# 모터2 제어 핀 설정
in3 = 22
in4 = 23
en2 = 24
GPIO.setup(in3, GPIO.OUT)
GPIO.setup(in4, GPIO.OUT)
GPIO.setup(en2, GPIO.OUT)

# PWM 설정
p1 = GPIO.PWM(en1, 1000)  # 모터1 PWM 신호를 1000Hz로 설정
p2 = GPIO.PWM(en2, 1000)  # 모터2 PWM 신호를 1000Hz로 설정
p1.start(0)  # 모터1 PWM 신호의 듀티 사이클을 0%로 시작하여 모터1이 초기에는 동작하지 않도록 설정
p2.start(0)  # 모터2 PWM 신호의 듀티 사이클을 0%로 시작하여 모터2가 초기에는 동작하지 않도록 설정

# 모터1 제어 함수
def motor1_forward():
    p1.ChangeDutyCycle(100)  # 모터1 동작 시, 듀티 사이클을 100%로 설정
    GPIO.output(in1, GPIO.HIGH)
    GPIO.output(in2, GPIO.LOW)
    print("모터1 전진")

def motor1_stop():
    p1.ChangeDutyCycle(0)  # 모터1 정지 시, 듀티 사이클을 0%로 설정하여 모터 정지
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.LOW)
    print("모터1 정지")

# 모터2 제어 함수
def motor2_forward():
    p2.ChangeDutyCycle(100)  # 모터2 동작 시, 듀티 사이클을 100%로 설정
    GPIO.output(in3, GPIO.HIGH)
    GPIO.output(in4, GPIO.LOW)
    print("모터2 전진")

def motor2_stop():
    p2.ChangeDutyCycle(0)  # 모터2 정지 시, 듀티 사이클을 0%로 설정하여 모터 정지
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in4, GPIO.LOW)
    print("모터2 정지")

try:
    # 모터1 동작 테스트
    motor1_forward()
    sleep(5)  # 5초간 모터1 전진
    motor1_stop()
    sleep(2)  # 2초간 정지 상태 유지

    # 모터2 동작 테스트
    motor2_forward()
    sleep(5)  # 5초간 모터2 전진
    motor2_stop()

finally:
    p1.stop()
    p2.stop()
    GPIO.cleanup()  # GPIO 설정 초기화
