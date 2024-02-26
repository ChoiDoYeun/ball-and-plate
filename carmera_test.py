import cv2

# 테스트하려는 인덱스 목록
camera_indices = [10, 11, 12, 13, 14, 15, 16, 18, 19, 20, 21, 22, 23, 31]

# 각 인덱스에 대한 카메라 테스트
for camera_index in camera_indices:
    # 비디오 캡처 객체 생성 시도
    cap = cv2.VideoCapture(camera_index)
    
    # 카메라가 성공적으로 열렸는지 확인
    if cap.isOpened():
        print(f"카메라가 /dev/video{camera_index}에서 성공적으로 열렸습니다.")
        
        # 프레임 캡처 시도
        ret, frame = cap.read()
        if ret:
            # 캡처된 프레임 표시
            cv2.imshow(f"Test Frame from /dev/video{camera_index}", frame)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        else:
            print(f"/dev/video{camera_index}에서 프레임을 캡처할 수 없습니다.")
        
        # 카메라 자원 해제
        cap.release()
    else:
        print(f"/dev/video{camera_index}에서 카메라를 열 수 없습니다.")
