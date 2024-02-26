import cv2

camera_index = 0 
cap = cv2.VideoCapture(camera_index)

# 카메라가 열렸는지 확인
if not cap.isOpened():
    print("카메라를 열 수 없습니다.")
else:
    print("카메라가 성공적으로 연결되었습니다.")

    # 카메라로부터 한 프레임 읽기 시도
    ret, frame = cap.read()
    if ret:
        # 프레임 읽기 성공, 화면에 표시
        cv2.imshow('Camera Test', frame)
        cv2.waitKey(0)  # 어떤 키를 누를 때까지 대기
        cv2.destroyAllWindows()
    else:
        # 프레임 읽기 실패
        print("카메라에서 이미지를 읽을 수 없습니다.")

    # 카메라 자원 해제
    cap.release()
