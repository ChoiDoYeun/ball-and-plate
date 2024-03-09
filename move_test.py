import RPi.GPIO as GPIO
import time

# GPIO 설정 초기화
GPIO.setwarnings(False)
GPIO.cleanup()  # 이전 실행의 설정을 정리
GPIO.setmode(GPIO.BCM)

# 모터 핀 설정
Motor1A, Motor1B, Motor1E = 17, 18, 27
Motor2A, Motor2B, Motor2E = 22, 23, 24
Motor3A, Motor3B, Motor3E = 10, 9, 25
Motor4A, Motor4B, Motor4E = 8, 7, 11

# 모터 PWM 객체 초기화
motor_pwm = {}

def setup_motor_pins():
    global motor_pwm
    motors = [Motor1A, Motor1B, Motor2A, Motor2B, Motor3A, Motor3B, Motor4A, Motor4B]
    enables = [Motor1E, Motor2E, Motor3E, Motor4E]
    for pin in motors:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)
    for en in enables:
        GPIO.setup(en, GPIO.OUT)
        pwm = GPIO.PWM(en, 1000)  # PWM 객체 생성
        pwm.start(0)
        motor_pwm[en] = pwm  # PWM 객체를 딕셔너리에 추가

def motor_control(MotorA, MotorB, speed):
    if speed >= 0:
        GPIO.output(MotorA, GPIO.HIGH)
        GPIO.output(MotorB, GPIO.LOW)
    else:
        GPIO.output(MotorA, GPIO.LOW)
        GPIO.output(MotorB, GPIO.HIGH)
        speed = -speed
    return speed

def move_direction(direction):
    if direction == "1:30":
        motor_pwm[Motor1E].ChangeDutyCycle(motor_control(Motor1A, Motor1B, 50))
        motor_pwm[Motor2E].ChangeDutyCycle(motor_control(Motor2A, Motor2B, 100))
        motor_pwm[Motor3E].ChangeDutyCycle(motor_control(Motor3A, Motor3B, 50))
        motor_pwm[Motor4E].ChangeDutyCycle(motor_control(Motor4A, Motor4B, 100))
    elif direction == "3:00":
        motor_pwm[Motor1E].ChangeDutyCycle(motor_control(Motor1A, Motor1B, 0))
        motor_pwm[Motor2E].ChangeDutyCycle(motor_control(Motor2A, Motor2B, 0))
        motor_pwm[Motor3E].ChangeDutyCycle(motor_control(Motor3A, Motor3B, 100))
        motor_pwm[Motor4E].ChangeDutyCycle(motor_control(Motor4A, Motor4B, 100))
    elif direction == "4:30":
        motor_pwm[Motor1E].ChangeDutyCycle(motor_control(Motor1A, Motor1B, -50))
        motor_pwm[Motor2E].ChangeDutyCycle(motor_control(Motor2A, Motor2B, -100))
        motor_pwm[Motor3E].ChangeDutyCycle(motor_control(Motor3A, Motor3B, -50))
        motor_pwm[Motor4E].ChangeDutyCycle(motor_control(Motor4A, Motor4B, -100))
    elif direction == "6:00":
        motor_pwm[Motor1E].ChangeDutyCycle(motor_control(Motor1A, Motor1B, -100))
        motor_pwm[Motor2E].ChangeDutyCycle(motor_control(Motor2A, Motor2B, -100))
        motor_pwm[Motor3E].ChangeDutyCycle(motor_control(Motor3A, Motor3B, -100))
        motor_pwm[Motor4E].ChangeDutyCycle(motor_control(Motor4A, Motor4B, -100))
    elif direction == "7:30":
        motor_pwm[Motor1E].ChangeDutyCycle(motor_control(Motor1A, Motor1B, -100))
        motor_pwm[Motor2E].ChangeDutyCycle(motor_control(Motor2A, Motor2B, -50))
        motor_pwm[Motor3E].ChangeDutyCycle(motor_control(Motor3A, Motor3B, -100))
        motor_pwm[Motor4E].ChangeDutyCycle(motor_control(Motor4A, Motor4B, -50))
    elif direction == "9:00":
        motor_pwm[Motor1E].ChangeDutyCycle(motor_control(Motor1A, Motor1B, 100))
        motor_pwm[Motor2E].ChangeDutyCycle(motor_control(Motor2A, Motor2B, 100))
        motor_pwm[Motor3E].ChangeDutyCycle(motor_control(Motor3A, Motor3B, 0))
        motor_pwm[Motor4E].ChangeDutyCycle(motor_control(Motor4A, Motor4B, 0))
    elif direction == "10:30":
        motor_pwm[Motor1E].ChangeDutyCycle(motor_control(Motor1A, Motor1B, 100))
        motor_pwm[Motor2E].ChangeDutyCycle(motor_control(Motor2A, Motor2B, 50))
        motor_pwm[Motor3E].ChangeDutyCycle(motor_control(Motor3A, Motor3B, 100))
        motor_pwm[Motor4E].ChangeDutyCycle(motor_control(Motor4A, Motor4B, 50))
    elif direction == "12:00":
        motor_pwm[Motor1E].ChangeDutyCycle(motor_control(Motor1A, Motor1B, 100))
        motor_pwm[Motor2E].ChangeDutyCycle(motor_control(Motor2A, Motor2B, 100))
        motor_pwm[Motor3E].ChangeDutyCycle(motor_control(Motor3A, Motor3B, 100))
        motor_pwm[Motor4E].ChangeDutyCycle(motor_control(Motor4A, Motor4B, 100))

try:
    # 방향별로 움직이도록 시퀀스 설정
    directions = ["1:30", "3:00", "4:30", "6:00", "7:30", "9:00", "10:30", "12:00"]
    for direction in directions:
        print(f"Moving in {direction} direction")
        move_direction(direction)
        time.sleep(2)  # 각 방향으로 2초간 이동

except KeyError as e:
    print(f"KeyError encountered: {e}")
    # 모터 PWM 인스턴스가 정의되지 않았을 경우의 처리
finally:
    # 모터 정지 및 GPIO 설정 정리
    for en in [Motor1E, Motor2E, Motor3E, Motor4E]:
        if en in motor_pwm:  # motor_pwm 딕셔너리에 핀이 존재하는지 확인
            motor_pwm[en].ChangeDutyCycle(0)
            motor_pwm[en].stop()  # PWM 정지
    GPIO.cleanup()
