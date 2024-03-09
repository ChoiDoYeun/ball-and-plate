import RPi.GPIO as GPIO
import time

# GPIO 설정 초기화
GPIO.setwarnings(False)
GPIO.cleanup()  # 이전 실행의 설정을 정리
GPIO.setmode(GPIO.BCM)

# 모터 핀 설정
Motor1A, Motor1B, Motor1E = 17, 18, 27  # 왼쪽 뒤 모터
Motor2A, Motor2B, Motor2E = 22, 23, 24  # 오른쪽 뒤 모터
Motor3A, Motor3B, Motor3E = 20, 21, 26  # 왼쪽 앞 모터
Motor4A, Motor4B, Motor4E = 8, 7, 11    # 오른쪽 앞 모터

# 모든 모터 핀 설정
motors = [Motor1A, Motor1B, Motor1E, Motor2A, Motor2B, Motor2E, Motor3A, Motor3B, Motor3E, Motor4A, Motor4B, Motor4E]
for pin in motors:
    GPIO.setup(pin, GPIO.OUT)

# 모터 제어 함수
def motor_control(MotorA, MotorB, MotorE, direction):
    if direction == "forward":
        GPIO.output(MotorA, GPIO.HIGH)
        GPIO.output(MotorB, GPIO.LOW)
    elif direction == "backward":
        GPIO.output(MotorA, GPIO.LOW)
        GPIO.output(MotorB, GPIO.HIGH)
    GPIO.output(MotorE, GPIO.HIGH) if direction != "stop" else GPIO.output(MotorE, GPIO.LOW)

def move_direction(direction):
    if direction == "12:00":  # 전진
        for motor in [(Motor1A, Motor1B, Motor1E), (Motor2A, Motor2B, Motor2E), (Motor3A, Motor3B, Motor3E), (Motor4A, Motor4B, Motor4E)]:
            motor_control(*motor, "forward")
    elif direction == "1:30":  # 1시 반 방향
        motor_control(Motor1A, Motor1B, Motor1E, "stop")
        motor_control(Motor2A, Motor2B, Motor2E, "forward")
        motor_control(Motor3A, Motor3B, Motor3E, "forward")
        motor_control(Motor4A, Motor4B, Motor4E, "forward")
    elif direction == "3:00":  # 오른쪽으로 이동
        motor_control(Motor1A, Motor1B, Motor1E, "forward")
        motor_control(Motor2A, Motor2B, Motor2E, "backward")
        motor_control(Motor3A, Motor3B, Motor3E, "backward")
        motor_control(Motor4A, Motor4B, Motor4E, "forward")
    elif direction == "4:30":  # 4시 반 방향
        motor_control(Motor1A, Motor1B, Motor1E, "forward")
        motor_control(Motor2A, Motor2B, Motor2E, "stop")
        motor_control(Motor3A, Motor3B, Motor3E, "forward")
        motor_control(Motor4A, Motor4B, Motor4E, "forward")
    elif direction == "6:00":  # 후진
        for motor in [(Motor1A, Motor1B, Motor1E), (Motor2A, Motor2B, Motor2E), (Motor3A, Motor3B, Motor3E), (Motor4A, Motor4B, Motor4E)]:
            motor_control(*motor, "backward")
    elif direction == "7:30":  # 7시 반 방향
        motor_control(Motor1A, Motor1B, Motor1E, "backward")
        motor_control(Motor2A, Motor2B, Motor2E, "backward")
        motor_control(Motor3A, Motor3B, Motor3E, "stop")
        motor_control(Motor4A, Motor4B, Motor4E, "backward")
    elif direction == "9:00":  # 왼쪽으로 이동
        motor_control(Motor1A, Motor1B, Motor1E, "backward")
        motor_control(Motor2A, Motor2B, Motor2E, "forward")
        motor_control(Motor3A, Motor3B, Motor3E, "forward")
        motor_control(Motor4A, Motor4B, Motor4E, "backward")
    elif direction == "10:30":  # 10시 반 방향
        motor_control(Motor1A, Motor1B, Motor1E, "backward")
        motor_control(Motor2A, Motor2B, Motor2E, "backward")
        motor_control(Motor3A, Motor3B, Motor3E, "backward")
        motor_control(Motor4A, Motor4B, Motor4E, "stop")

    time.sleep(2)  # 주어진 방향으로 2초간 이동
    # 모든 모터 정지
    for motorE in [Motor1E, Motor2E, Motor3E, Motor4E]:
        GPIO.output(motorE, GPIO.LOW)

try:
    print("Starting motor sequence...")

    # 여기에 원하는 방향을 넣어 이동 시키면 됩니다. 예: "3:00" 방향으로 이동
    directions = ["1:30", "3:00", "4:30", "6:00", "7:30", "9:00", "10:30", "12:00"]
    for direction in directions:
        print(f"Moving in {direction} direction")
        move_direction(direction)
        time.sleep(1)  # 다음 방향 전환을 위한 짧은 정지

    print("Motor sequence completed.")

except KeyboardInterrupt:
    print("Program stopped by user.")
finally:
    GPIO.cleanup()  # 프로그램 종료 시 GPIO 설정 정리
