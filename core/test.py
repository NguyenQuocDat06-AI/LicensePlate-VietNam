from LicensePlate import recognizeLicensePlate
import argparse
import cv2

# import server
# server.start("0.0.0.0", 9049)

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument('-i', '--image', required=False, help='path to input image')
    args = ap.parse_args()

    imgPath = "/home/thanhntmany/lab/parking-system/misc/LicensePlate-Server/core/LicensePlate/_test/input.jpg"
    if args.image:
        imgPath = args.image

    imgNumpy = cv2.imread(imgPath)

    recognizeLicensePlate(imgNumpy)