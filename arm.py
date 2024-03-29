from adafruit_servokit import ServoKit
import time
import math

# PCA9685 모듈 설정 (16채널 PWM 드라이버)
kit = ServoKit(channels=16)

# 각 서보 모터의 최소 및 최대 펄스 길이를 전역 변수로 설정
min_pulse = 500
max_pulse = 2500

def move_servo_smoothly(motor_number, target_angle, step=1, delay=0.05):
    global min_pulse, max_pulse
    kit.servo[motor_number].set_pulse_width_range(min_pulse, max_pulse)
    
    current_angle = kit.servo[motor_number].angle if kit.servo[motor_number].angle is not None else 0
    
    if current_angle < target_angle:
        for angle in range(int(current_angle), min(int(target_angle), 180)+1, step):
            kit.servo[motor_number].angle = angle
            time.sleep(delay)
    else:
        for angle in range(int(current_angle), max(int(target_angle), 0)-1, -step):
            kit.servo[motor_number].angle = angle
            time.sleep(delay)

def calculate_and_adjust_angles_complete(x, y, z, a1=13, a2=17.5, a3=5.5):
    def calculate_angles(x, y, z, a1, a2, a3):
        theta_base = math.atan2(y, x)
        z_eff = z - a1
        r = math.sqrt(x**2 + y**2)
        d = math.sqrt(r**2 + z_eff**2)
        cos_theta2 = (d**2 - a2**2 - a3**2) / (2 * a2 * a3)
        cos_theta2 = max(min(cos_theta2, 1), -1)  # cos_theta2 값을 [-1, 1] 범위 내로 제한
        
        theta2 = math.atan2(-math.sqrt(1 - cos_theta2**2), cos_theta2)
        theta2 = math.atan2(-math.sqrt(1 - cos_theta2**2), cos_theta2)
        angle_d = math.atan2(z_eff, r)
        cos_alpha = (a2**2 + d**2 - a3**2) / (2 * a2 * d)
        cos_alpha = max(min(cos_alpha, 1), -1)  # cos_alpha 값을 [-1, 1] 범위 내로 제한
        
        alpha = math.atan2(math.sqrt(1 - cos_alpha**2), cos_alpha)
        theta1 = angle_d + alpha
        return math.degrees(theta_base), math.degrees(theta1), math.degrees(theta2), 180 - (math.degrees(theta1) + math.degrees(theta2))

    base, shoulder, elbow, wrist = calculate_angles(x, y, z, a1, a2, a3)
    elbow = (elbow + 360) % 360
    if elbow > 180:
        elbow -= 180
    wrist = wrist % 360
    if wrist > 180:
        wrist -= 180
    return base, shoulder, elbow, wrist


def initialize_servos():
    global min_pulse, max_pulse  # 전역 변수 사용 선언
    # 초기 설정 값 지정
    initial_positions = [0, 60, 60, 150, 0, 0]  # 0~3번 서보 모터 각도 설정, 4, 5번 서보 모터는 0도
    for i in range(len(initial_positions)):
        kit.servo[i].set_pulse_width_range(min_pulse, max_pulse)
        kit.servo[i].angle = initial_positions[i]
        time.sleep(0.05)

if __name__ == '__main__':
    # 모터 초기화
    initialize_servos()
    print("서보 모터 초기화 완료")

    # 좌표 입력
    # 홈포지션
    home_x, home_y, home_z = 8.75, 0.0, 33.66

    # 홈포지션을 다시 (0,0,0)으로 설정했을때 이미지를 통해 얻은 x,y,z좌표값 (example)
    delta_x, delta_y, delta_z = 15, 10, 20

    # 최종 좌표
    final_x = home_x + delta_x
    final_y = home_y + delta_y
    final_z = home_z + delta_z
    angles = calculate_and_adjust_angles_complete(final_x, final_y, final_z)
    print("최종 좌표: ({}, {}, {})".format(final_x, final_y, final_z))
    print("기반 각도: {:.2f}, 어깨 각도: {:.2f}, 팔꿈치 각도: {:.2f}, 손목 각도: {:.2f}".format(*angles))

    # 계산된 각도로 서보 모터 조정
    for i, angle in enumerate(angles):
        move_servo_smoothly(i, angle, delay=0.05)
        print(f"{i}번 서보 모터를 {angle}도로 이동했습니다.")
