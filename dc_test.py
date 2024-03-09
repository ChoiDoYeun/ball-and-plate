import RPi.GPIO as GPIO
import time

# GPIO 설정 초기화
GPIO.setwarnings(False)
GPIO.cleanup()  # 이전 실행의 설정을 정리
GPIO.setmode(GPIO.BCM)  # GPIO 모드를 BCM으로 설정

# 첫 번째 모터 핀 설정
Motor1A = 23
Motor1B = 24
Motor1E = 25

# 두 번째 모터 핀 설정
Motor2A = 17
Motor2B = 18
Motor2E = 27

# 모터 핀 설정
GPIO.setup(Motor1A, GPIO.OUT)
GPIO.setup(Motor1B, GPIO.OUT)
GPIO.setup(Motor1E, GPIO.OUT)

GPIO.setup(Motor2A, GPIO.OUT)
GPIO.setup(Motor2B, GPIO.OUT)
GPIO.setup(Motor2E, GPIO.OUT)

# 첫 번째 모터 앞으로 회전
def motor1_forward():
    GPIO.output(Motor1A, GPIO.HIGH)
    GPIO.output(Motor1B, GPIO.LOW)
    GPIO.output(Motor1E, GPIO.HIGH)
    print("Motor 1 Forward")

# 첫 번째 모터 정지
def motor1_stop():
    GPIO.output(Motor1E, GPIO.LOW)
    print("Motor 1 Stop")

# 첫 번째 모터 뒤로 회전
def motor1_backward():
    GPIO.output(Motor1A, GPIO.LOW)
    GPIO.output(Motor1B, GPIO.HIGH)
    GPIO.output(Motor1E, GPIO.HIGH)
    print("Motor 1 Backward")

# 두 번째 모터 앞으로 회전
def motor2_forward():
    GPIO.output(Motor2A, GPIO.HIGH)
    GPIO.output(Motor2B, GPIO.LOW)
    GPIO.output(Motor2E, GPIO.HIGH)
    print("Motor 2 Forward")

# 두 번째 모터 정지
def motor2_stop():
    GPIO.output(Motor2E, GPIO.LOW)
    print("Motor 2 Stop")

# 두 번째 모터 뒤로 회전
def motor2_backward():
    GPIO.output(Motor2A, GPIO.LOW)
    GPIO.output(Motor2B, GPIO.HIGH)
    GPIO.output(Motor2E, GPIO.HIGH)
    print("Motor 2 Backward")

try:
    print("Starting motor sequence...")
    motor1_forward()
    motor2_forward()
    time.sleep(5)  # 두 모터 모두 5초간 전진
    
    motor1_stop()
    motor2_stop()
    time.sleep(2)  # 두 모터 모두 2초간 정지
    
    motor1_backward()
    motor2_backward()
    time.sleep(5)  # 두 모터 모두 5초간 후진
    
    motor1_stop()
    motor2_stop()
    print("Motor sequence completed.")
    
except KeyboardInterrupt:
    print("Program stopped by user.")
finally:
    GPIO.cleanup()  # 프로그램 종료 시 GPIO 설정 정리
