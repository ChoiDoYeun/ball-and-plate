import cv2

# 카메라 인덱스 설정 (0은 일반적으로 첫 번째 카메라를 의미함)
camera_index = 14
cap = cv2.VideoCapture(camera_index)

if not cap.isOpened():
    print("카메라를 열 수 없음")
    # V4L2 드라이버를 로드 시도
    import os
    os.system('sudo modprobe bcm2835-v4l2')
    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        print("카메라를 다시 열 수 없음. 설정을 확인하세요.")
else:
    print("카메라가 성공적으로 연결되었습니다.")
    # 카메라 테스트를 위해 한 프레임 캡처
    ret, frame = cap.read()
    if ret:
        cv2.imshow("Test Frame", frame)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print("프레임을 가져올 수 없음")

# 사용이 끝난 자원 해제
cap.release()
