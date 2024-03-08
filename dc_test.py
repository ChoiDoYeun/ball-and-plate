import RPi.GPIO as GPIO
from time import sleep

# GPIO 모드 설정
GPIO.setmode(GPIO.BCM)

# 모터 제어 핀 설정
motor1_pins = {'in1': 17, 'in2': 18, 'en': 27}
motor2_pins = {'in1': 22, 'in2': 23, 'en': 24}

for pin in motor1_pins.values():
    GPIO.setup(pin, GPIO.OUT)
for pin in motor2_pins.values():
    GPIO.setup(pin, GPIO.OUT)

# PWM 설정
motor1_pwm = GPIO.PWM(motor1_pins['en'], 1000)  # 1000Hz로 설정
motor2_pwm = GPIO.PWM(motor2_pins['en'], 1000)  # 1000Hz로 설정
motor1_pwm.start(0)  # 듀티 사이클 0%로 시작
motor2_pwm.start(0)  # 듀티 사이클 0%로 시작

# 모터 제어 함수 정의
def control_motor(pins, pwm, speed=100, forward=True):
    """모터 제어 함수: 속도와 방향을 인자로 받음"""
    pwm.ChangeDutyCycle(speed)
    GPIO.output(pins['in1'], GPIO.HIGH if forward else GPIO.LOW)
    GPIO.output(pins['in2'], GPIO.LOW if forward else GPIO.HIGH)

def stop_motor(pins, pwm):
    """모터 정지 함수"""
    pwm.ChangeDutyCycle(0)
    GPIO.output(pins['in1'], GPIO.LOW)
    GPIO.output(pins['in2'], GPIO.LOW)

# 테스트 시퀀스
try:
    print("모터1 전진")
    control_motor(motor1_pins, motor1_pwm, speed=100, forward=True)
    sleep(5)
    stop_motor(motor1_pins, motor1_pwm)
    sleep(2)

    print("모터2 전진")
    control_motor(motor2_pins, motor2_pwm, speed=100, forward=True)
    sleep(5)
    stop_motor(motor2_pins, motor2_pwm)

finally:
    # 정리
    motor1_pwm.stop()
    motor2_pwm.stop()
    GPIO.cleanup()
