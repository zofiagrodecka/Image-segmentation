# Author: Jan Prokop, Zofia Grodecka
# OS: WINDOWS

import cv2 as cv
import numpy as np
import sys
import pathlib
from copy import deepcopy
from itertools import chain 


def converting_to_gray_scale(file_name, show=False):
    # cwd = pathlib.Path().absolute()
    # file_path = str(cwd) + "\\Photos\\" + file_name
    
    image = cv.imread(file_name)
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    
    if show:
        cv.imshow('ORIGINAL', image)
        cv.imshow('GRAY_SCALE', gray)
        
    return gray


def gaussian_blurring(image, show=False):
    gaussed = cv.GaussianBlur(image, (0,0), cv.BORDER_DEFAULT)

    if show:
        cv.imshow('BLURRED', gaussed)

    return gaussed


def split_into_tones(image, show=False, brackets=[]):
    
    # Prepering shade sections
    division = [0]
    if len(brackets) != 0:
        for i in brackets:
            division.append(i)
    division.append(255)
    print(division)

    if len(division) == 2:  # DEFAULT: For now I break the intensity into 5 equal sections
        Tones = [ [] for i in range(5) ]

        for y in range(image.shape[1]):
            for x in range(image.shape[0]):
                intensity = image[x, y]
                Tones[ intensity//51 ].append([x,y])

        if show:
            print_by_tones(image, Tones)

        return Tones

    else:  # with user-described sections of gray spectrum
        Tones = [ [] for i in range( len(division) - 1 ) ]

        for y in range(image.shape[1]):
            for x in range(image.shape[0]):
                intensity = image[x, y]

                for i in range(1,len(division)):
                    if division[i-1] <= intensity <= division[i]:
                        Tones[i-1].append([x,y])
                        break

        if show:
            print_by_tones(image, Tones)

        return Tones


def print_by_tones(image, Tones):
    N = len(Tones)
    for i in range(N):
            print(f"Tone {i+1}: {len(Tones[i])}")
            copy = deepcopy(image)
            for (x, y) in Tones[i]:
                copy[x, y] = 255

            copy_scaled = cv.resize(copy, None, fx=0.3, fy=0.3, interpolation = cv.INTER_LINEAR)
            cv.imshow(f"Tone {i+1}", copy_scaled[:,:])


def calculate_threshold(image, Tones, original):
    N = len(Tones)
    mask = np.zeros(image.shape[:2], np.uint8)

    for i in range(N):
        for (x, y) in Tones[i]:
            mask[x, y] = 255
        masked_img = cv.bitwise_and(original, original, mask=mask)
        otsu_threshold, image_result = cv.threshold(masked_img, 0, 255, cv.THRESH_TOZERO + cv.THRESH_OTSU)
        # cv.imshow(f"Mask {i + 1}", mask)
        masked_img_scaled = cv.resize(masked_img, None, fx=0.6, fy=0.6, interpolation = cv.INTER_LINEAR)
        cv.imshow(f"Masked image {i + 1}", masked_img_scaled)
        """if i == N-2:
            change_threshold(masked_img, 200)"""
        print(f"Threshold value for {i+1} tone: {otsu_threshold}")
        image_result_scaled = cv.resize(image_result, None, fx=0.6, fy=0.6, interpolation = cv.INTER_LINEAR)
        cv.imshow(f"Tone {i + 1} after threshold", image_result_scaled)
        mask = np.zeros(image.shape[:2], np.uint8)


def change_threshold(image, new_value):
    threshold, image_result = cv.threshold(image, new_value, 255, cv.THRESH_TOZERO)
    cv.imshow("After change of threshold", image_result)


if __name__ == "__main__":
    
    file_path = sys.argv[1]
    gray_scale_div = []
    for i in range(2, len(sys.argv)):
        parameter = sys.argv[i]
        gray_scale_div.append(int(parameter))

    gray = converting_to_gray_scale(file_path, show=False)
    gaussed = gaussian_blurring(gray, show=False)
    Tones = split_into_tones(gaussed, brackets=gray_scale_div, show=True)

    calculate_threshold(gaussed, Tones, gray)

    cv.waitKey()
 