from adafruit_servokit import ServoKit
import time

# PCA9685 모듈 설정 (16채널 PWM 드라이버)
kit = ServoKit(channels=16)

# 모든 서보 모터를 0도로 초기화하는 함수
def initialize_servos():
    for i in range(16):
        kit.servo[i].angle = None  # 연속 회전 서보의 경우, 초기화 방식을 확인해야 합니다.

# 360도 서보 모터의 속도와 방향을 조절하는 함수
def control_360_servo(motor_number, angle):
    # 0도: 한 방향 최소 속도, 90도: 정지, 180도: 반대 방향 최대 속도
    if angle <= 90:  # 한 방향으로 회전
        speed = (90 - angle)  # 속도 조절 로직, 실제로는 서보 모터에 맞게 조정 필요
    else:  # 반대 방향으로 회전
        speed = (angle - 90)  # 속도 조절 로직, 실제로는 서보 모터에 맞게 조정 필요
    
    print(f"모터 #{motor_number}를 {angle}도에 해당하는 속도로 제어합니다: 속도 = {speed}")
    # 실제 속도 제어 로직 구현 필요

if __name__ == '__main__':
    initialize_servos()

    while True:
        motor_number = int(input("제어할 서보 모터 번호를 입력하세요 (0-15): "))
        angle = int(input("각도를 입력하세요 (0-180): "))
        
        if motor_number < 0 or motor_number > 15:
            print("잘못된 서보 모터 번호입니다. 0-15 사이의 값이어야 합니다.")
        elif angle < 0 or angle > 180:
            print("잘못된 각도입니다. 각도는 0-180 사이여야 합니다.")
        else:
            control_360_servo(motor_number, angle)

        continue_prompt = input("다른 서보 모터를 제어하시겠습니까? (y/n): ")
        if continue_prompt.lower() != 'y':
            break
