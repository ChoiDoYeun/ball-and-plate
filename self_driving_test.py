import RPi.GPIO as GPIO
import cv2
import numpy as np
import time

# GPIO 설정 초기화
GPIO.setwarnings(False)
GPIO.cleanup()  # 이전 실행의 설정을 정리
GPIO.setmode(GPIO.BCM)

# 모터 핀 설정
Motor1A, Motor1B, Motor1E = 17, 18, 27  # 모터 1 (왼쪽 앞 바퀴)
Motor2A, Motor2B, Motor2E = 22, 23, 24  # 모터 2 (오른쪽 앞 바퀴)
Motor3A, Motor3B, Motor3E = 20, 21, 26  # 모터 3 (왼쪽 뒷 바퀴)
Motor4A, Motor4B, Motor4E = 8, 7, 11    # 모터 4 (오른쪽 뒷 바퀴)

# 모터 핀 설정
def setup_motor_pins():
    pins = [Motor1A, Motor1B, Motor1E, Motor2A, Motor2B, Motor2E, Motor3A, Motor3B, Motor3E, Motor4A, Motor4B, Motor4E]
    for pin in pins:
        GPIO.setup(pin, GPIO.OUT)

# 모터 제어 함수
def drive_motor(motor, direction, speed=100):
    if motor == 1:
        pinA, pinB, pinE = Motor1A, Motor1B, Motor1E
    elif motor == 2:
        pinA, pinB, pinE = Motor2A, Motor2B, Motor2E
    elif motor == 3:
        pinA, pinB, pinE = Motor3A, Motor3B, Motor3E
    else:
        pinA, pinB, pinE = Motor4A, Motor4B, Motor4E
    
    GPIO.output(pinE, GPIO.HIGH)
    if direction == 'forward':
        GPIO.output(pinA, GPIO.HIGH)
        GPIO.output(pinB, GPIO.LOW)
    else:
        GPIO.output(pinA, GPIO.LOW)
        GPIO.output(pinB, GPIO.HIGH)
    # PWM 속도 제어를 추가할 수 있습니다. 예를 들어, GPIO.PWM(pinE, 1000).start(speed)

def stop_motor(motor):
    if motor == 1:
        pinE = Motor1E
    elif motor == 2:
        pinE = Motor2E
    elif motor == 3:
        pinE = Motor3E
    else:
        pinE = Motor4E
    
    GPIO.output(pinE, GPIO.LOW)

def stop_all_motors():
    stop_motor(1)
    stop_motor(2)
    stop_motor(3)
    stop_motor(4)


def adjust_steering(center_x, image_center_x):
    offset = center_x - image_center_x
    if abs(offset) < 20:
        # 중앙에 가까우면 모든 모터 전진
        for motor in range(1, 5):
            drive_motor(motor, 'forward')
    elif offset < 0:
        # 중앙값이 왼쪽에 있으면 왼쪽 모터 속도 감소
        drive_motor(1, 'forward', speed=50)
        drive_motor(3, 'forward', speed=50)
        drive_motor(2, 'forward')
        drive_motor(4, 'forward')
    else:
        # 중앙값이 오른쪽에 있으면 오른쪽 모터 속도 감소
        drive_motor(1, 'forward')
        drive_motor(3, 'forward')
        drive_motor(2, 'forward', speed=50)
        drive_motor(4, 'forward', speed=50)

def process_image_and_control_steering(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY_INV)
    edges = cv2.Canny(binary, 50, 150, apertureSize=3)
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 100, minLineLength=100, maxLineGap=10)
    centers = []

    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            centers.append(((x1 + x2) // 2, (y1 + y2) // 2))

    if len(centers) > 0:
        center_x, center_y = np.mean(centers, axis=0).astype(int)
        image_center_x = frame.shape[1] // 2

        # 중앙값 위치에 큰 빨간색 원 그리기
        cv2.circle(frame, (center_x, center_y), 10, (0, 0, 255), -1)
        
        # 조향 결정
        offset = center_x - image_center_x
        if abs(offset) < 20:  # 중앙에 가까우면 직진
            for motor in range(1, 5):
                drive_motor(motor, 'forward', speed=100)
        elif offset < 0:  # 중앙값이 왼쪽에 있으면 좌회전
            drive_motor(1, 'forward', speed=50)  # 속도 조절로 좌회전 구현
            drive_motor(3, 'forward', speed=50)
            drive_motor(2, 'forward', speed=100)
            drive_motor(4, 'forward', speed=100)
        else:  # 중앙값이 오른쪽에 있으면 우회전
            drive_motor(1, 'forward', speed=100)  # 속도 조절로 우회전 구현
            drive_motor(3, 'forward', speed=100)
            drive_motor(2, 'forward', speed=50)
            drive_motor(4, 'forward', speed=50)
    else:
        stop_all_motors() # 선을 감지하지 못하면 정지

    # 결과 이미지 표시
    cv2.imshow("Steering Adjustment", frame)


def main():
    setup_motor_pins()
    
    # 웹캠 설정
    cap = cv2.VideoCapture(0)
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # 이미지 처리 및 조향 제어
            process_image_and_control_steering(frame)

            # ESC 키를 누르면 종료
            if cv2.waitKey(1) & 0xFF == 27:
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()
        stop_all_motors()
        GPIO.cleanup()

if __name__ == '__main__':
    main()
