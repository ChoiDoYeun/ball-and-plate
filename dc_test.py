import RPi.GPIO as GPIO
import time

# GPIO 모드 설정
GPIO.setmode(GPIO.BCM)

# 모터 드라이버 핀 설정
Motor1A = 24
Motor1B = 23
Motor1E = 25

# 모터 핀 설정
GPIO.setup(Motor1A, GPIO.OUT)
GPIO.setup(Motor1B, GPIO.OUT)
GPIO.setup(Motor1E, GPIO.OUT)

# 모터 앞으로 회전
def motor_forward():
    GPIO.output(Motor1A, GPIO.HIGH)
    GPIO.output(Motor1B, GPIO.LOW)
    GPIO.output(Motor1E, GPIO.HIGH)
    print("Motor Forward")

# 모터 정지
def motor_stop():
    GPIO.output(Motor1E, GPIO.LOW)
    print("Motor Stop")

# 모터 뒤로 회전
def motor_backward():
    GPIO.output(Motor1A, GPIO.LOW)
    GPIO.output(Motor1B, GPIO.HIGH)
    GPIO.output(Motor1E, GPIO.HIGH)
    print("Motor Backward")

try:
    motor_forward()
    time.sleep(5)  # 5초간 전진
    motor_stop()
    time.sleep(2)  # 2초간 정지
    motor_backward()
    time.sleep(5)  # 5초간 후진
    motor_stop()
except KeyboardInterrupt:
    GPIO.cleanup()

GPIO.cleanup()
