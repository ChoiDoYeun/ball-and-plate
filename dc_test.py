import RPi.GPIO as GPIO
import time

# GPIO 모드 설정
GPIO.setmode(GPIO.BCM)

# 모터 핀 설정
Motor3A, Motor3B, Motor3E = 20, 21, 26 # 진행방향 (로봇팔쪽) 왼쪽
Motor4A, Motor4B, Motor4E = 8, 7, 11 # 진행방향 (로봇팔쪽) 오른쪽

# 모터 핀 출력 설정
GPIO.setup(Motor3A, GPIO.OUT)
GPIO.setup(Motor3B, GPIO.OUT)
GPIO.setup(Motor3E, GPIO.OUT)
GPIO.setup(Motor4A, GPIO.OUT)
GPIO.setup(Motor4B, GPIO.OUT)
GPIO.setup(Motor4E, GPIO.OUT)

# 모터 제어 함수
def motor_forward(motor):
    if motor == 3:
        GPIO.output(Motor3A, GPIO.HIGH)
        GPIO.output(Motor3B, GPIO.LOW)
        GPIO.output(Motor3E, GPIO.HIGH)
    elif motor == 4:
        GPIO.output(Motor4A, GPIO.HIGH)
        GPIO.output(Motor4B, GPIO.LOW)
        GPIO.output(Motor4E, GPIO.HIGH)

def motor_backward(motor):
    if motor == 3:
        GPIO.output(Motor3A, GPIO.LOW)
        GPIO.output(Motor3B, GPIO.HIGH)
        GPIO.output(Motor3E, GPIO.HIGH)
    elif motor == 4:
        GPIO.output(Motor4A, GPIO.LOW)
        GPIO.output(Motor4B, GPIO.HIGH)
        GPIO.output(Motor4E, GPIO.HIGH)

def motor_stop(motor):
    if motor == 3:
        GPIO.output(Motor3E, GPIO.LOW)
    elif motor == 4:
        GPIO.output(Motor4E, GPIO.LOW)

# 첫 번째 모터 테스트
motor_forward(3)
time.sleep(2)
motor_backward(3)
time.sleep(2)
motor_stop(3)

# 두 번째 모터 테스트
motor_forward(4)
time.sleep(2)
motor_backward(4)
time.sleep(2)
motor_stop(4)

# GPIO 정리
GPIO.cleanup()
