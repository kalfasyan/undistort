import numpy as np
import cv2
import glob
import time
import os


chessboard_dir = './chessboard_images/'
stickyplates_dir = './stickyplate_images/'
undistortedplates_dir = './undistorted_images'

paths = [f"{chessboard_dir}/output_allbnw", 
        f"{chessboard_dir}/output_success", 
        f"{chessboard_dir}/result_params",
        f"{undistortedplates_dir}",
        f"{stickyplates_dir}",
        f"{stickyplates_dir}"]

for p in paths:
    os.system(f"rm -rf {p}/*")