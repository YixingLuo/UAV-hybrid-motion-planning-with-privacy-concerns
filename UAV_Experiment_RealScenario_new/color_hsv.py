import cv2
import os
path = os.getcwd() + '/pic2/' + str(150)+'.jpg'
img = cv2.imread(path)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# blueLower = np.array([90, 55, 160])
# blueUpper = np.array([120, 200, 255])

# 102 [144 125  98] 43 91
# 103 [168 130 130] 49 492
# 105 [163 162 128] 1057 203
# 109 [166 149 128] 1192 205
# 110 [168 166 132] 162 414
# 111 [175 169 126] 92 452
# 112 [181 174 131] 80 458

def mouse_click(event, x, y, flags, para):
    if event == cv2.EVENT_LBUTTONDOWN:  # 左边鼠标点击
        # x = 91
        # y = 43
        print('PIX:', x, y)
        print("BGR:", img[y, x])
        print("GRAY:", gray[y, x])
        print("HSV:", hsv[y, x])


if __name__ == '__main__':
    cv2.namedWindow("img")
    cv2.setMouseCallback("img", mouse_click)
    while True:
        cv2.imshow('img', img)
        if cv2.waitKey() == ord('q'):
            break
    cv2.destroyAllWindows()
