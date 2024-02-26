import cv2

# 사용 가능한 비디오 디바이스 인덱스 범위를 설정합니다.
# 스크린샷에 따라 0부터 31까지로 설정했습니다.
for camera_index in range(32):
    cap = cv2.VideoCapture(camera_index)
    if cap.isOpened():
        ret, frame = cap.read()
        if ret:
            cv2.imshow(f"Test Frame from /dev/video{camera_index}", frame)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            print(f"카메라가 /dev/video{camera_index}에서 작동합니다.")
            break
        cap.release()
    else:
        print(f"/dev/video{camera_index}에서 카메라를 열 수 없음.")

# 자원 해제
if cap:
    cap.release()
