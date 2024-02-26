import cv2
import numpy as np

# 카메라 캡처 객체 생성
cap = cv2.VideoCapture(0)

# 카메라 해상도 설정 (예시)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# 플레이트의 실제 크기 (mm)
plate_width_mm = 187
plate_height_mm = 141

# 카메라 이미지의 크기 (픽셀) - 실제 카메라 설정에 따라 조정 필요
image_width_px = 640
image_height_px = 480

# mm 당 픽셀 비율 계산
scale_x = plate_width_mm / image_width_px
scale_y = plate_height_mm / image_height_px

while True:
    # 프레임별로 비디오 캡처
    ret, frame = cap.read()
    if not ret:
        break

    # BGR 이미지를 HSV 색공간으로 변환
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # 주황색 볼을 위한 HSV 색상 범위 정의
    lower_orange = np.array([5, 50, 50])
    upper_orange = np.array([10, 255, 255])

    # HSV 이미지에서 주황색만 추출하기 위한 마스크 생성
    mask = cv2.inRange(hsv, lower_orange, upper_orange)

    # 마스크에서 컨투어 찾기
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # 가장 큰 컨투어 찾기
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        (x, y), radius = cv2.minEnclosingCircle(largest_contour)
        center = (int(x), int(y))
        
        # 컨투어가 일정 크기 이상일 때만 중심에 원 그리기
        if radius > 10:
            cv2.circle(frame, center, int(radius), (0, 255, 0), 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)
            
            # 픽셀 좌표를 실제 좌표(mm)로 변환
            real_x_mm = (center[0] - image_width_px / 2) * scale_x
            real_y_mm = (center[1] - image_height_px / 2) * scale_y
            print(f"볼의 실제 위치: ({real_x_mm}mm, {real_y_mm}mm)")

    # 결과 이미지 표시
    cv2.imshow('Frame', frame)
    cv2.imshow('Mask', mask)

    # 'q' 키를 누르면 루프에서 벗어나기
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 자원 해제
cap.release()
cv2.destroyAllWindows()
