import RPi.GPIO as GPIO
import cv2
import numpy as np

# 서보모터 초기화 함수 추가해야함
# 서보모터 초기화 함수 수정 사항
    # 주행모드
        #2번 0도
        #3도 180도

# GPIO 설정 초기화
GPIO.setwarnings(False)
GPIO.cleanup()
GPIO.setmode(GPIO.BCM)

# 모터 핀 설정
Motor1A, Motor1B, Motor1E = 20, 21, 26  # 진행 방향 (로봇팔 쪽) 왼쪽 모터
Motor2A, Motor2B, Motor2E = 8, 7, 11    # 진행 방향 (로봇팔 쪽) 오른쪽 모터

# 모터 핀 설정을 출력으로 설정
for pin in [Motor1A, Motor1B, Motor1E, Motor2A, Motor2B, Motor2E]:
    GPIO.setup(pin, GPIO.OUT)

# PWM 객체 생성 및 시작
pwm_frequency = 100
Motor1PWM = GPIO.PWM(Motor1E, pwm_frequency)
Motor2PWM = GPIO.PWM(Motor2E, pwm_frequency)
Motor1PWM.start(0)
Motor2PWM.start(0)

def calculate_pwm_values(center_position, width):
    deviation = center_position - (width / 2)
    base_pwm = 50  # 기본 PWM 값
    adjustment = int(deviation / width * 100)  # 조정량 계산
    pwm_left = base_pwm + adjustment
    pwm_right = base_pwm - adjustment
    return pwm_left, pwm_right

def set_motor_pwm(motor, direction, value):
    if value < 0: value = 0  # 값 보정
    if value > 100: value = 100  # 값 보정
    GPIO.output(motor[0], direction)
    GPIO.output(motor[1], not direction)
    motor[2].ChangeDutyCycle(value)

# 웹캠 설정
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # 영상 처리 로직
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY_INV)  # 검정색 선 인식을 위한 이진화
    contours, _ = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        # 가장 큰 윤곽선 찾기
        largest_contour = max(contours, key=cv2.contourArea)
        M = cv2.moments(largest_contour)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])

            # 화면 중앙에 대한 선의 위치 찾기
            height, width = frame.shape[:2]
            cv2.line(frame, (width // 2, 0), (width // 2, height), (255, 0, 0), 2)  # 화면 중앙 세로선
            cv2.circle(frame, (cx, cy), 5, (0, 255, 0), -1)  # 선의 중앙 위치
            
            pwm_left, pwm_right = calculate_pwm_values(cx, width)

            # 모터 속도 조절
            set_motor_pwm((Motor1A, Motor1B, Motor1PWM), True, pwm_left)
            set_motor_pwm((Motor2A, Motor2B, Motor2PWM), True, pwm_right)

    #cv2.imshow('Frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 자원 해제
Motor1PWM.stop()
Motor2PWM.stop()
cap.release()
cv2.destroyAllWindows()
GPIO.cleanup()
