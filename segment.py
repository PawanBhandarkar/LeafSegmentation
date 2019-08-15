import cv2
import matplotlib.pyplot as plt
import numpy as np


def detect_leaf(img):
    l_b = np.array([30, 0, 50])
    u_b = np.array([255, 255, 255])

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, l_b, u_b)

    res = cv2.bitwise_and(img, img, mask=mask)

    return mask


def display_image(title, image):
    cv2.namedWindow(title, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(title, 600, 600)
    cv2.imshow(title, image)
    while True:
        key = cv2.waitKey(1)
        if key == 27:
            break
    cv2.destroyAllWindows()


def nothing(x):
    pass


def check_HLS(img):

    cv2.namedWindow("Tracker")
    cv2.createTrackbar("LH", "Tracker", 0, 255, nothing)
    cv2.createTrackbar("UH", "Tracker", 255, 255, nothing)
    cv2.createTrackbar("LL", "Tracker", 0, 255, nothing)
    cv2.createTrackbar("UL", "Tracker", 255, 255, nothing)
    cv2.createTrackbar("LS", "Tracker", 0, 255, nothing)
    cv2.createTrackbar("US", "Tracker", 255, 255, nothing)

    while True:

        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HLS)

        l_h = cv2.getTrackbarPos("LH", "Tracker")
        l_l = cv2.getTrackbarPos("LL", "Tracker")
        l_s = cv2.getTrackbarPos("LS", "Tracker")

        u_h = cv2.getTrackbarPos("UH", "Tracker")
        u_l = cv2.getTrackbarPos("UL", "Tracker")
        u_s = cv2.getTrackbarPos("US", "Tracker")

        l_b = np.array([l_h, l_l, l_s])
        u_b = np.array([u_h, u_l, u_s])

        mask = cv2.inRange(hsv, l_b, u_b)

        res = cv2.bitwise_and(hsv, hsv, mask=mask)
        res2 = cv2.bitwise_and(img, img, mask=mask)

        blurred = cv2.GaussianBlur(res, (3, 3), 0)
        laplacian = cv2.Laplacian(blurred, ddepth=-1)

        cv2.namedWindow('image', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('image', 600, 600)
        cv2.imshow("image", res2)

        cv2.namedWindow('Mask', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Mask', 600, 600)
        cv2.imshow("Mask", mask)

        cv2.namedWindow('Result', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Result', 600, 600)
        cv2.imshow("Result", res)

        key = cv2.waitKey(1)
        if key == 27:
            break

    # cap.release()
    cv2.destroyAllWindows()


def check_Canny(img):
    cv2.namedWindow("Tracker")
    cv2.createTrackbar("LB", "Tracker", 0, 255, nothing)
    cv2.createTrackbar("UB", "Tracker", 255, 255, nothing)
    while True:

        l_b = cv2.getTrackbarPos("LB", "Tracker")
        u_b = cv2.getTrackbarPos("UB", "Tracker")

        canny = cv2.Canny(img, l_b, u_b)

        cv2.namedWindow('Canny', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Canny', 600, 600)
        cv2.imshow("Canny", canny)

        key = cv2.waitKey(1)
        if key == 27:
            break

    # cap.release()
    cv2.destroyAllWindows()


def equalize_histogram_color(img):
    img_yuv = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)
    img_yuv[:, :, 0] = cv2.equalizeHist(img_yuv[:, :, 0])
    img = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2BGR)
    return img


img = cv2.imread("7.jpeg")
eq = equalize_histogram_color(img)
# check_HLS(img)


display_image("Image", img)
display_image("Equalized", eq)

lap = cv2.Sobel(eq, dx=1, dy=1, ddepth=-1)
display_image("Lap", lap)

blur = cv2.GaussianBlur(lap, (5, 5), 0)
display_image("Lap", blur)

edges = cv2.Canny(blur, 50, 150)
display_image("Edges", edges)
