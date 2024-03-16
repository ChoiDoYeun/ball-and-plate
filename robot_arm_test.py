from adafruit_servokit import ServoKit
import time

# 사용할 서보 모터의 개수
NUM_SERVOS = 6

# 서보 모터 키트 초기화 (PCA9685 모듈 사용 시)
kit = ServoKit(channels=16)

# 모든 서보 모터를 0도로 초기화하는 함수
def initialize_servos():
    global min_pulse, max_pulse  # 전역 변수 사용 선언
    for i in range(16):
        kit.servo[i].set_pulse_width_range(min_pulse, max_pulse)
        kit.servo[i].angle = 0
        time.sleep(0.05)

def calculate_duration(angle):
    """
    주어진 각도에 대해 서보 모터가 회전하는 데 필요한 시간을 계산합니다.
    
    :param angle: 회전할 각도
    :return: 회전에 필요한 시간 (초)
    """
    return (angle / 60.0) * 0.17

def rotate_servo(servo_number, direction, angle):
    """
    지정된 번호의 360도 서보 모터를 원하는 방향과 각도로 회전시킵니다.
    
    :param servo_number: 서보 모터의 번호 (0부터 시작)
    :param direction: 회전 방향 (+1: 시계 방향, -1: 반시계 방향)
    :param angle: 회전할 각도
    """
    duration = calculate_duration(angle)
    speed = direction * 1.0
    kit.continuous_servo[servo_number].throttle = speed
    time.sleep(duration)
    kit.continuous_servo[servo_number].throttle = 0
    print(f"서보 모터 {servo_number}가 {direction} 방향으로, {angle}도 회전했습니다.")

def get_user_input(prompt, input_type):
    """
    사용자로부터 특정 타입의 입력을 받습니다.

    :param prompt: 사용자에게 보여줄 메시지
    :param input_type: 입력 타입 (int 또는 float)
    :return: 변환된 입력 값
    """
    while True:
        user_input = input(prompt)
        try:
            return input_type(user_input)
        except ValueError:
            print(f"잘못된 입력입니다. {input_type.__name__} 타입의 숫자를 입력해야 합니다.")

def main():
    initialize_servos()
    servo_number = get_user_input("서보 모터 번호를 입력하세요 (0-5): ", int)
    direction = get_user_input("회전 방향을 입력하세요 (+1: 시계 방향, -1: 반시계 방향): ", int)
    angle = get_user_input("회전할 각도를 입력하세요: ", float)

    if servo_number not in range(NUM_SERVOS):
        print(f"잘못된 서보 모터 번호입니다. 0에서 {NUM_SERVOS-1} 사이의 값을 입력하세요.")
        return
    if direction not in [-1, 1]:
        print("회전 방향은 +1 또는 -1 이어야 합니다.")
        return
    if angle < 0 or angle > 360:
        print("각도는 0에서 360 사이여야 합니다.")
        return

    rotate_servo(servo_number, direction, angle)

if __name__ == "__main__":
    main()
