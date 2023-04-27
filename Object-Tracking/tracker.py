from time import sleep
import cv2
import numpy as np
from plot import Visualizer

#entry
def main():
    # read video
    cap_nuc = cv2.VideoCapture('./data/nuc/video/nuc_0422.mp4')

    # read csv
    nuc_loc = np.genfromtxt('./data/nuc/csv/nuc_loc_0422.csv', delimiter=',')[1:]
    orin_loc = np.genfromtxt('./data/nuc/csv/orin_loc_0422.csv', delimiter=',')[1:]
    obj_loc = np.genfromtxt('./data/nuc/csv/obj_loc_0422.csv', delimiter=',')[1:]

    # Create a 3D plot with 2 traces
    graph = Visualizer(5)
    # set trace color
    graph.set_color(0, (255, 0, 0, 255))
    graph.set_color(1, (0, 255, 0, 255))
    graph.set_color(2, (0, 0, 255, 255))
    graph.set_color(3, (200, 30, 128, 255))
    graph.set_color(4, (200, 30, 128, 255))
    # set axis limit
    graph.set_xlim((-1, 3))
    graph.set_ylim((0, 7))
    graph.set_zlim((0, 2))

    # Create a marker detector
    md_nuc = MarkerDetector('nuc')
    md_orin = MarkerDetector('orin')

    # create windows
    cv2.namedWindow('nuc', cv2.WINDOW_NORMAL)
    cv2.namedWindow('orin', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('nuc', 640, 480)
    cv2.resizeWindow('orin', 640, 360)

    startOrin = False
    startNuc = True
    orinCount = 0
    count = 0
    viconCount = 0

    sleep(5)

    while True:
        # print(count)
        viconCount = count
        # vicon rate: 100Hz
        graph.add_point(0, [nuc_loc[viconCount * 4][3], nuc_loc[viconCount * 4][4], nuc_loc[viconCount * 4][5]])
        graph.add_point(1, [orin_loc[viconCount * 4][3], orin_loc[viconCount * 4][4], orin_loc[viconCount * 4][5]])
        graph.add_point(2, [obj_loc[viconCount * 4][3], obj_loc[viconCount * 4][4], obj_loc[viconCount * 4][5]])

        # frame_nuc = cv2.imread('./data/nuc/image/left' + str(count).zfill(4) + '.jpg')
        frame_nuc = cap_nuc.read()[1]

        if startOrin:
            frame_orin = cv2.imread('./data/orin/image/left' + str(orinCount).zfill(4) + '.jpg')
            keypoints_orin = md_orin.detect(frame_orin)
            if len(keypoints_orin) > 0:
                deltaLoc = deltaLocation(keypoints_orin[0].pt, False)
                graph.add_point(4, [orin_loc[viconCount * 4][3] - deltaLoc[0], orin_loc[viconCount * 4][4] - deltaLoc[1], 0.2])
                
                x = int(keypoints_orin[0].pt[0])
                y = int(keypoints_orin[0].pt[1])
                frame_orin = cv2.circle(frame_orin, (x, y), 15, (255, 255, 255), 2)
            cv2.imshow('orin', frame_orin)
        
        if startNuc:
            keypoints_nuc = md_nuc.detect(frame_nuc)
            if len(keypoints_nuc) > 0:
                deltaLoc = deltaLocation(keypoints_nuc[0].pt)
                graph.add_point(3, [nuc_loc[viconCount * 4][3] - deltaLoc[0], nuc_loc[viconCount * 4][4] - deltaLoc[1], 0.2])

                x = int(keypoints_nuc[0].pt[0])
                y = int(keypoints_nuc[0].pt[1])
                frame_nuc = cv2.circle(frame_nuc, (x, y), 15, (255, 255, 255), 2)

            if count > 400:
                startOrin = True
            if count > 800:
                startNuc = False

        cv2.imshow('nuc', frame_nuc)

        # Exit if the user presses the 'q' key
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        count += 1
        if startOrin:
            orinCount += 1

def deltaLocation(loc, nuc=True):
    width = 640 if nuc else 1280
    height = 480 if nuc else 720
    ratio_x = 1 / height / 2
    ratio_y = 1 / width / 2
    return ((loc[1] - height / 2) * ratio_x, (loc[0] - width / 2) * ratio_y)

class MarkerDetector:
    def __init__(self, type):
        # Setup SimpleBlobDetector parameters.
        self.params = cv2.SimpleBlobDetector_Params()
        # Change thresholds
        self.params.minThreshold = 180
        # Filter by Circularity
        self.params.filterByCircularity = False
        # Filter by Convexity
        self.params.filterByConvexity = True
        self.params.minConvexity = 0.87
        # Filter by Inertia
        self.params.filterByInertia = True
        self.params.minInertiaRatio = 0.5

        # Filter by Area.
        self.params.filterByArea = True
        if type == 'orin':
            # for orin
            self.params.minArea = 2000
            self.params.maxArea = 3000
        elif type == 'nuc':
            # for nuc
            self.params.minArea = 1000
            self.params.maxArea = 2000

        self.detector = cv2.SimpleBlobDetector_create(self.params)

    def detect(self, frame):
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return self.detector.detect(frame_gray)

if __name__ == '__main__':
    main()