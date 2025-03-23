import cv2 as cv
import numpy as np
import sys
import os
import time

# ascii characters used
ascii_chars = '@%#*+=-:. '


def read_video() -> cv.VideoCapture:
    # read the argument
    if len(sys.argv) != 2:
        print('Usage: python script.py <video_path>')
        sys.exit(1)
    argument = sys.argv[1]
    # load the video
    return cv.VideoCapture(argument)


def gray_frame(frame: np.ndarray) -> np.ndarray:
    # grayscale the frame
    return cv.cvtColor(frame, cv.COLOR_BGR2GRAY)


def scale_frame(frame: np.ndarray) -> tuple:
    # rescale the frame to terminal size
    aspect_ratio = (frame.shape[1] / frame.shape[0])
    terminal_size = os.get_terminal_size()
    columns, rows = terminal_size
    height = int((columns / aspect_ratio) / 3)
    return cv.resize(frame, (columns, height)), columns, height


def convert_ascii(frame: np.ndarray, width: int, height: int) -> str:
    # convert frame to string of ascii character
    ascii_image = ''
    for y in range(height):
        for x in range(width):
            pixel = frame[y, x]
            # depending on floor devision we choose which ascii to use
            ascii_image += ascii_chars[pixel // 32]
        ascii_image += '\n'
    return ascii_image


def display_frame(ascii_image: str, fps : float) -> None:
    # clear the terminal and print ascii image
    os.system('cls' if os.name == 'nt' else 'clear')
    print(ascii_image)
    # pause between frame to make it the right speed
    time.sleep(1 / fps)


# Main --------------------------------------------------------------------------------------------
def main() -> None:
    video = read_video()                    # load the video 
    fps = video.get(cv.CAP_PROP_FPS)        # fps property of the video

    # while the video isn't finished for every iteration:
    # 1. get the current frame
    # 2. make it into a grascale image and resize it fittingly
    # 3. convert to ascii
    # 4. display the frame
    while video.isOpened():
        ret, frame = video.read()
        if not ret:
            break
        frame_gray_scaled, width, height = scale_frame(gray_frame(frame))
        frame_ascii = convert_ascii(frame_gray_scaled, width, height)
        display_frame(frame_ascii, fps)


if __name__ == '__main__':
    main()
