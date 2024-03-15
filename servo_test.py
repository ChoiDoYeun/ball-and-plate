from adafruit_servokit import ServoKit
import time

# PCA9685 모듈 설정 (16채널 PWM 드라이버)
kit = ServoKit(channels=16)

# 각 서보 모터의 최소 및 최대 펄스 길이를 설정합니다 (서보 모터에 따라 조정할 수 있음)
min_pulse = 500
max_pulse = 2500

# 서보 모터를 순차적으로 움직이는 함수
def move_servos_sequentially():
    for i in range(6):  # 4개의 서보 모터 제어
        kit.servo[i].set_pulse_width_range(min_pulse, max_pulse)
        kit.servo[i].angle = 0  # 0도로 서보 모터 회전
        time.sleep(1)
        kit.servo[i].angle = 20  # 180도로 서보 모터 회전
        time.sleep(1)
        kit.servo[i].angle = 10  # 다시 90도로 서보 모터 회전 (중간 위치)
        time.sleep(1)

if __name__ == '__main__':
    move_servos_sequentially()
