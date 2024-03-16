from adafruit_servokit import ServoKit
import time

# PCA9685 모듈 설정 (16채널 PWM 드라이버)
kit = ServoKit(channels=16)

# 각 서보 모터의 최소 및 최대 펄스 길이를 설정합니다 (서보 모터에 따라 조정할 수 있음)
min_pulse = 500
max_pulse = 2500

# 서보 모터를 점진적으로 움직이는 함수
def move_servo_smoothly(motor_number, target_angle, step=1, delay=0.05):
    kit.servo[motor_number].set_pulse_width_range(min_pulse, max_pulse)
    
    current_angle = kit.servo[motor_number].angle if kit.servo[motor_number].angle is not None else 0
    
    if current_angle < target_angle:
        for angle in range(int(current_angle), int(target_angle)+1, step):
            kit.servo[motor_number].angle = angle
            time.sleep(delay)
    else:
        for angle in range(int(current_angle), int(target_angle)-1, -step):
            kit.servo[motor_number].angle = angle
            time.sleep(delay)

# 모든 서보 모터를 0도로 초기화하는 함수
def initialize_servos():
    for i in range(16):  # 16채널 모든 서보 모터 초기화
        kit.servo[i].set_pulse_width_range(min_pulse, max_pulse)
        kit.servo[i].angle = 0
        time.sleep(0.05)  # 초기화 간에 약간의 지연을 줍니다.

if __name__ == '__main__':
    initialize_servos()  # 프로그램 시작 시 모든 서보 모터를 0도로 초기화합니다.
    print("모든 서보 모터가 0도로 초기화되었습니다.")

    while True:
        # 사용자 입력 받기
        motor_number = int(input("제어할 서보 모터 번호를 입력하세요 (0-15): "))
        target_angle = int(input("목표 각도를 입력하세요 (0-180): "))
        
        # 입력 검증
        if motor_number < 0 or motor_number > 15 or target_angle < 0 or target_angle > 180:
            print("잘못된 입력입니다. 서보 모터 번호는 0-15, 각도는 0-180 사이여야 합니다.")
        else:
            # 서보 모터 움직이기
            move_servo_smoothly(motor_number, target_angle, step=1, delay=0.05)
            print(f"{motor_number}번 서보 모터를 {target_angle}도로 이동했습니다.")

        # 반복 제어
        continue_prompt = input("다른 서보 모터를 제어하시겠습니까? (y/n): ")
        if continue_prompt.lower() != 'y':
            break
