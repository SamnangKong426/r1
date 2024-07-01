import cv2 as cv
import imutils
import numpy as np

class BallDetector:
    def __init__(self):
        self.cap = cv.VideoCapture(0)
        self.lower_red1 = np.array([0, 70, 50])
        self.upper_red1 = np.array([7, 255, 255])
        self.lower_red2 = np.array([170, 70, 50])
        self.upper_red2 = np.array([180, 255, 255])
        self.lower_blue = np.array([100, 50, 50])
        self.upper_blue = np.array([130, 255, 255])

    def findBalls(self, contours):
        minArea = 800
        ballsFound = []
        for contour in contours:
            area = cv.contourArea(contour)
            if area > minArea:
                perimeter = cv.arcLength(contour, True)
                approx = cv.approxPolyDP(contour, 0.01 * perimeter, True)
                if len(approx) < 3 or len(approx) > 6:
                    circularity = 4 * np.pi * area / (perimeter * perimeter)
                    hull = cv.convexHull(contour)
                    hull_area = cv.contourArea(hull)
                    solidity = float(area) / hull_area
                    if circularity > 0.7 and solidity > 0.9:
                        ballsFound.append(contour)
        return ballsFound

    def processFrame(self, color_image):
        height, width, _ = color_image.shape
        gaussBlurImg = cv.GaussianBlur(color_image, (9, 9), cv.BORDER_DEFAULT)
        HSVResult = cv.cvtColor(gaussBlurImg, cv.COLOR_BGR2HSV)

        kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (5, 5))
        red1_mask = cv.inRange(HSVResult, self.lower_red1, self.upper_red1)
        red2_mask = cv.inRange(HSVResult, self.lower_red2, self.upper_red2)
        red_mask = cv.bitwise_or(red1_mask, red2_mask)
        filterErodeRed = cv.erode(red_mask, kernel, iterations=3)
        filterDilateRed = cv.dilate(filterErodeRed, kernel, iterations=2)

        blue_mask = cv.inRange(HSVResult, self.lower_blue, self.upper_blue)
        filterErodeBlue = cv.erode(blue_mask, kernel, iterations=3)
        filterDilateBlue = cv.dilate(filterErodeBlue, kernel, iterations=2)

        red_contours = cv.findContours(filterDilateRed, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        red_contours = imutils.grab_contours(red_contours)
        blue_contours = cv.findContours(filterDilateBlue, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        blue_contours = imutils.grab_contours(blue_contours)

        red_found = self.findBalls(red_contours)
        blue_found = self.findBalls(blue_contours)

        red_mid = self.drawCircles(color_image, red_found, (0, 0, 255))
        blue_mid = self.drawCircles(color_image, blue_found, (255, 0, 0))

        cv.imshow('Video Stream', color_image)
        cv.imshow('Blue', filterDilateBlue)
        cv.imshow('Dilate Red', filterDilateRed)
        return red_mid, blue_mid


    def drawCircles(self, image, contours, color):
        for contour in contours:
            moments = cv.moments(contour)
            if moments["m00"] != 0:
                coreX = int(moments["m10"] / moments["m00"])
                coreY = int(moments["m01"] / moments["m00"])
                ((x1, y1), r) = cv.minEnclosingCircle(contour)
                if r > 15:
                    cv.circle(image, (int(x1), int(y1)), int(r), color, 2)
                    cv.circle(image, (coreX, coreY), 10, color, -1)
                    cv.circle(image, (340, 240), 10, color, -1)
                    cv.line(image, (coreX, coreY), (340, 240), color, 2)
                    mid_point = (int(x1), int(y1))
                    cv.putText(image, f'({mid_point[0]}, {mid_point[1]})', mid_point, cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                    return mid_point
    def run(self):
        while True:
            ret, color_image = self.cap.read()
            if not ret:
                break
            red_mid, blue_mid = self.processFrame(color_image)
            print(f'Red: {red_mid}, Blue: {blue_mid}')
            if cv.waitKey(1) & 0xFF == ord('d'):
                break
        self.cap.release()
        cv.destroyAllWindows()

if __name__ == "__main__":
    detector = BallDetector()
    detector.run()