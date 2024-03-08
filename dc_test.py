import RPi.GPIO as GPIO
from time import sleep

# GPIO 모드 설정
GPIO.setmode(GPIO.BCM)

# 모터 제어 핀 설정
motor_pins = {
    "motor1": {"in1": 17, "in2": 18, "en": 27},
    "motor2": {"in3": 22, "in4": 23, "en": 24},
}

# 모터 제어 핀 초기화
for motor, pins in motor_pins.items():
    for pin in pins.values():
        GPIO.setup(pin, GPIO.OUT)

# PWM 초기화 및 시작
pwm = {
    "motor1": GPIO.PWM(motor_pins["motor1"]["en"], 1000),
    "motor2": GPIO.PWM(motor_pins["motor2"]["en"], 1000),
}
for p in pwm.values():
    p.start(0)

# 모터 제어 함수 정의
def control_motor(motor, action):
    pins = motor_pins[motor]
    if action == "forward":
        GPIO.output(pins["in1" if "1" in motor else "in3"], GPIO.HIGH)
        GPIO.output(pins["in2" if "1" in motor else "in4"], GPIO.LOW)
        pwm[motor].ChangeDutyCycle(100)
    elif action == "stop":
        GPIO.output(pins["in1" if "1" in motor else "in3"], GPIO.LOW)
        GPIO.output(pins["in2" if "1" in motor else "in4"], GPIO.LOW)
        pwm[motor].ChangeDutyCycle(0)

try:
    # 모터1 전진 및 정지
    control_motor("motor1", "forward")
    sleep(5)
    control_motor("motor1", "stop")
    sleep(2)

    # 모터2 전진 및 정지
    control_motor("motor2", "forward")
    sleep(5)
    control_motor("motor2", "stop")

finally:
    # 정리
    for p in pwm.values():
        p.stop()
    GPIO.cleanup()
