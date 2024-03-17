from adafruit_servokit import ServoKit
import time

# PCA9685 모듈 설정 (16채널 PWM 드라이버)
kit = ServoKit(channels=16)

# 각 서보 모터의 최소 및 최대 펄스 길이를 전역 변수로 설정
min_pulse = 500
max_pulse = 2500

# 서보 모터를 점진적으로 움직이는 함수
def move_servo_smoothly(motor_number, target_angle, step=1, delay=0.01):
    global min_pulse, max_pulse  # 전역 변수 사용 선언
    kit.servo[motor_number].set_pulse_width_range(min_pulse, max_pulse)
    
    current_angle = kit.servo[motor_number].angle if kit.servo[motor_number].angle is not None else 0
    
    # 각도 조정 로직
    if current_angle < target_angle:
        for angle in range(int(current_angle), min(int(target_angle), 180)+1, step):  # 최대 각도를 180으로 제한
            kit.servo[motor_number].angle = angle
            time.sleep(delay)
    else:
        for angle in range(int(current_angle), max(int(target_angle), 0)-1, -step):  # 최소 각도를 0으로 제한
            kit.servo[motor_number].angle = angle
            time.sleep(delay)

# 모든 서보 모터를 0도로 초기화하는 함수
def initialize_servos():
    global min_pulse, max_pulse  # 전역 변수 사용 선언
    # 초기 설정 값 지정
    initial_positions = [0, 60, 60, 150, 0, 0]  # 0~3번 서보 모터 각도 설정, 4, 5번 서보 모터는 0도
    for i in range(len(initial_positions)):
        kit.servo[i].set_pulse_width_range(min_pulse, max_pulse)
        kit.servo[i].angle = initial_positions[i]
        time.sleep(0.05)

if __name__ == '__main__':
    initialize_servos()
    print("모든 서보 모터가 0도로 초기화되었습니다.")

    while True:
        motor_number = int(input("제어할 서보 모터 번호를 입력하세요 (0-15): "))
        target_angle = int(input("목표 각도를 입력하세요 (0-180): "))  # 연속 회전 서보 모터가 아닌 경우
        
        # 입력 검증 (연속 회전 서보 모터의 경우, 이 부분은 무시)
        if motor_number < 0 or motor_number > 15:
            print("잘못된 서보 모터 번호입니다. 0-15 사이의 값이어야 합니다.")
        elif target_angle < 0 or target_angle > 180:
            print("잘못된 각도입니다. 각도는 0-180 사이여야 합니다.")
        else:
            move_servo_smoothly(motor_number, target_angle, step=1, delay=0.03)
            print(f"{motor_number}번 서보 모터를 {target_angle}도로 이동했습니다.")

        continue_prompt = input("다른 서보 모터를 제어하시겠습니까? (y/n): ")
        if continue_prompt.lower() != 'y':
            break
