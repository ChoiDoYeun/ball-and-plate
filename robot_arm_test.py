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
    # 모터 스펙: 0.17초 / 60도
    return (angle / 60.0) * 0.17

def rotate_servo(servo_number, direction, angle):
    """
    지정된 번호의 360도 서보 모터를 원하는 방향과 각도로 회전시킵니다.
    
    :param servo_number: 서보 모터의 번호 (0부터 시작)
    :param direction: 회전 방향 (+1: 시계 방향, -1: 반시계 방향)
    :param angle: 회전할 각도
    """
    if 0 <= servo_number < NUM_SERVOS:
        # 회전에 필요한 시간 계산
        duration = calculate_duration(angle)
        # 속도 설정 (최대 속도로 설정)
        speed = direction * 1.0
        kit.continuous_servo[servo_number].throttle = speed
        print(f"서보 모터 {servo_number}를 {direction} 방향으로, {angle}도 회전시킵니다.")
        time.sleep(duration)  # 계산된 시간 동안 회전
        kit.continuous_servo[servo_number].throttle = 0  # 회전 정지
        print("회전 완료")
    else:
        print(f"잘못된 서보 모터 번호입니다. 0에서 {NUM_SERVOS-1} 사이의 값을 입력하세요.")

# 사용자 입력 처리
def main():
    try:
        initialize_servos()
        servo_number = int(input("서보 모터 번호를 입력하세요 (0-5): "))
        direction = int(input("회전 방향을 입력하세요 (+1: 시계 방향, -1: 반시계 방향): "))
        angle = float(input("회전할 각도를 입력하세요: "))
        
        # 입력 값 검증
        if direction not in [-1, 1]:
            print("회전 방향은 +1 또는 -1 이어야 합니다.")
            return
        if angle < 0:
            print("각도는 0보다 크거나 같아야 합니다.")
            return
        
        rotate_servo(servo_number, direction, angle)
    except ValueError:
        print("잘못된 입력입니다. 숫자를 입력해야 합니다.")
    except KeyboardInterrupt:
        print("\n프로그램을 종료합니다.")

if __name__ == "__main__":
    main()
