# Author: Jan Prokop, Zofia Grodecka
# OS: WINDOWS

import cv2 as cv
import numpy as np
import sys
import pathlib
from copy import deepcopy
from itertools import chain
from PIL import Image

BLUR_PARAM = 41


def converting_to_gray_scale(file_name, show=False):
    cwd = pathlib.Path().absolute()
    file_path = str(cwd) + "\\Photos\\" + file_name
    
    image = cv.imread(file_path)
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    
    if show:
        # cv.imshow('ORIGINAL', image)
        cv.imshow('GRAY_SCALE', gray)
        
    return gray


def gaussian_blurring(image, show=False):
    gaussed = cv.GaussianBlur(image, (BLUR_PARAM,BLUR_PARAM), cv.BORDER_DEFAULT)

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
            print_by_tones(image, Tones, [0, 51, 102, 153, 204, 255])

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
            print_by_tones(image, Tones, division)

        return Tones


def print_by_tones(image, Tones, division):
    masks = []
    N = len(Tones)
    for i in range(N):
            # print(f"Tone {i+1}: {len(Tones[i])}")
            copy = deepcopy(image)
            for (x, y) in Tones[i]:
                copy[x, y] = 255

            copy_scaled = cv.resize(copy, None, fx=0.2, fy=0.2, interpolation=cv.INTER_LINEAR)
            cv.imshow(f"Tone {i + 1} - {division[i]}:{division[i + 1]}", copy_scaled[:, :])
            masks.append(copy_scaled[:, :])

    # All = np.concatenate(masks, axis=1)
    # cv.imshow("Tonal sections", All)


def apply_threshold(blurred_image, gray_image, Tones, show=False):
    N = len(Tones)
    mask = np.zeros(blurred_image.shape[:2], np.uint8)
    masked = []
    results = []

    for i in range(N):
        for (x, y) in Tones[i]:
            mask[x, y] = 255
        masked_img = cv.bitwise_and(gray_image, gray_image, mask=mask)
        otsu_threshold, image_result = cv.threshold(masked_img, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
        # image_result = Image.fromarray(image_result.astype(np.uint8))
        # image_result = image_result.tobitmap()
        masked.append(masked_img)
        print(f"Threshold value for {i + 1} tone: {otsu_threshold}")
        if show:
            cv.imshow(f"Mask {i + 1}", mask)
            masked_img_scaled = cv.resize(masked_img, None, fx=0.6, fy=0.6, interpolation = cv.INTER_LINEAR)
            cv.imshow(f"Masked image {i + 1}", masked_img_scaled)
            image_result_scaled = cv.resize(image_result, None, fx=0.6, fy=0.6, interpolation = cv.INTER_LINEAR)
            image = np.array(image_result)
            cv.imshow(f"Tone {i + 1} after threshold", image)
        results.append(image_result)
        mask = np.zeros(blurred_image.shape[:2], np.uint8)
    return masked, results


def change_threshold(image, new_value, show=False):
    threshold, image_result = cv.threshold(image, new_value, 255, cv.THRESH_TOZERO)
    if show:
        cv.imshow("After change of threshold", image_result)
    return image_result


def merge_pictures(results, show=False):
    n = len(results)

    if n < 2:
        image_result = Image.fromarray(results[0].astype(np.uint8))
        image_result = image_result.tobitmap()
        return image_result

    merged = cv.bitwise_or(results[0], results[1])
    # cv.imshow(f"Tones {1, 2} after merge", merged)
    for i in range(2, len(results)):
        merged = cv.bitwise_or(merged, results[i])
        # cv.imshow(f"Tones {i+1} after merge", merged)

    image_result = Image.fromarray(merged.astype(np.uint8))

    if show:
        cv.imshow("Result", merged)

    return image_result


if __name__ == "__main__":

    # Getting input from usr
    file_name = sys.argv[1]
    gray_scale_div = []
    for i in range(2, len(sys.argv)):
        parameter = sys.argv[i]
        gray_scale_div.append(int(parameter))

    # Converting image
    gray = converting_to_gray_scale(file_name, show=True)

    gaussed = gaussian_blurring(gray, show=False)

    Tones = split_into_tones(gaussed, brackets=gray_scale_div, show=True)

    masked, thresholded = apply_threshold(gaussed, gray, Tones, show=False)

    result = merge_pictures(thresholded, show=True)

    cv.waitKey()

    # Saving result image
    usr_wants_to_save = "_"
    while usr_wants_to_save.upper() != "Y" or usr_wants_to_save.upper() != "N":
        usr_wants_to_save = input("Do you want to save the result? [Y/n]:\n> ")

        if usr_wants_to_save.upper() == "Y":
            result_file_name = input("Put result file name:\n> ")
            result.save(f"Results/{result_file_name}")
            break
        elif usr_wants_to_save.upper() == "N":
            break
        else:
            print("Wrong response character!")
 