import RPi.GPIO as GPIO
import time

# GPIO 설정 초기화
GPIO.setwarnings(False)
GPIO.cleanup()  # 이전 실행의 설정을 정리
GPIO.setmode(GPIO.BCM)  # GPIO 모드를 BCM으로 설정

# 모터 핀 설정
Motor1A, Motor1B, Motor1E = 24, 23, 25
Motor2A, Motor2B, Motor2E = 17, 18, 27
Motor3A, Motor3B, Motor3E = 10, 9, 25
Motor4A, Motor4B, Motor4E = 8, 7, 11

# 모든 모터 핀 설정
motors = [Motor1A, Motor1B, Motor1E, Motor2A, Motor2B, Motor2E, Motor3A, Motor3B, Motor3E, Motor4A, Motor4B, Motor4E]
for pin in motors:
    GPIO.setup(pin, GPIO.OUT)

# 모터 제어 함수 정의 (앞으로, 정지, 뒤로 각각 모터별로 정의)
def motor_forward(MotorA, MotorB, MotorE):
    GPIO.output(MotorA, GPIO.HIGH)
    GPIO.output(MotorB, GPIO.LOW)
    GPIO.output(MotorE, GPIO.HIGH)

def motor_stop(MotorE):
    GPIO.output(MotorE, GPIO.LOW)

def motor_backward(MotorA, MotorB, MotorE):
    GPIO.output(MotorA, GPIO.LOW)
    GPIO.output(MotorB, GPIO.HIGH)
    GPIO.output(MotorE, GPIO.HIGH)

try:
    # 모터 순차적으로 제어
    print("Starting motor sequence...")
    motor_forward(Motor1A, Motor1B, Motor1E)
    motor_forward(Motor2A, Motor2B, Motor2E)
    motor_forward(Motor3A, Motor3B, Motor3E)
    motor_forward(Motor4A, Motor4B, Motor4E)
    time.sleep(5)  # 모든 모터 5초간 전진
    
    motor_stop(Motor1E)
    motor_stop(Motor2E)
    motor_stop(Motor3E)
    motor_stop(Motor4E)
    time.sleep(2)  # 모든 모터 2초간 정지
    
    motor_backward(Motor1A, Motor1B, Motor1E)
    motor_backward(Motor2A, Motor2B, Motor2E)
    motor_backward(Motor3A, Motor3B, Motor3E)
    motor_backward(Motor4A, Motor4B, Motor4E)
    time.sleep(5)  # 모든 모터 5초간 후진
    
    motor_stop(Motor1E)
    motor_stop(Motor2E)
    motor_stop(Motor3E)
    motor_stop(Motor4E)
    print("Motor sequence completed.")
    
except KeyboardInterrupt:
    print("Program stopped by user.")
finally:
    GPIO.cleanup()  # 프로그램 종료 시 GPIO 설정 정리
