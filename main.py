import numpy as np
import cv2
import glob
import time
import argparse
import os

clean = True

chessboard_dir = './chessboard_images/'
stickyplates_dir = './stickyplate_images/'
undistortedplates_dir = './undistorted_images'

paths = [f"{chessboard_dir}/output_allbnw", 
        f"{chessboard_dir}/output_success", 
        f"{chessboard_dir}/result_params",
        f"{undistortedplates_dir}"]

for p in paths:
    if not os.path.isdir(f"{p}/"):
        os.mkdir(f"{p}/")
    if clean:
        os.system(f"rm -rf {p}/*")

# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((7*7,3), np.float32)
objp[:,:2] = np.mgrid[0:7,0:7].T.reshape(-1,2) * 10

# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.

# Checking dirs if they're empty  or if they are suspiciously full 
# (e.g. if not using this software with one imaging session but more)
stickyplate_images = glob.glob(f'{stickyplates_dir}/*.jpg')
assert len(stickyplate_images) > 0, f"Please add some sticky plates to undistort into {stickyplate_images}"

images = glob.glob(f'{chessboard_dir}/*.jpg')
assert len(images) > 5, "Too few chessboard images for this session"
assert len(images) < 15, "Too many chessboard images for this session"


a, b = 7,7 # chessboard dims

for fpath in images:
    fname = fpath.split('/')[-1][:-4]
    print(f'\nPROCESSING : {fname}')

    assert "color" not in fname, "Error: Color image detected. Please use ONLY chessboard images."
    assert "chess" in fname, "Check that you put chessboard images only in this folder."

    t = time.time()
    img = cv2.imread(fpath)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray,9,55,55)
    gray = cv2.medianBlur(gray, 5)
    gray = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)[1] # threshold = 127  
  
    cv2.imwrite(f'{chessboard_dir}/output_allbnw/{fname}_bnw.jpg',gray)

    # Find the chess board corners
    ret, corners = cv2.findChessboardCorners(gray, (a,b),None)

    # If found, add object points, image points (after refining them)
    if ret == True:
        print("SUCCESS: Found points successfully! Adding object points.")
        
        objpoints.append(objp)

        corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
        imgpoints.append(corners2)

        # Draw and display the corners
        img = cv2.drawChessboardCorners(img, (7,7), corners2,ret)
        cv2.imshow('img',cv2.resize(img, (828, 746)))
        cv2.waitKey(100)
        cv2.imwrite(f'{chessboard_dir}/output_success/{fname}_chessboard_found.jpg',img)
    print(f'Elapsed time for {fname}: {time.time() - t} seconds')
cv2.destroyAllWindows()

""" CAMERA CALIBRATION """

ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1],None,None)

np.savez(f'{chessboard_dir}/result_params/calib_params.npz', ret=ret, mtx=mtx, dist=dist,
                                        rvecs=rvecs, tvecs=tvecs)

""" UNDISTORTION """

data = np.load(f'{chessboard_dir}/result_params/calib_params.npz')

for fpath in stickyplate_images:
    fname = fpath.split('/')[-1][:-4]
    print(f'\nUNDISTORTING : {fname}')

    ret, mtx, dist, rvecs, tvecs = data['ret'], data['mtx'], data['dist'], data['rvecs'], data['tvecs']

    img = cv2.imread(f'{stickyplates_dir}/{fname}.jpg')
    h,  w = img.shape[:2]
    newcameramtx, roi=cv2.getOptimalNewCameraMatrix(mtx,dist,(w,h),1,(w,h))

    # undistort
    dst = cv2.undistort(img, mtx, dist, None, newcameramtx)

    # crop the image
    x,y,w,h = roi
    dst = dst[y:y+h, x:x+w]
    cv2.imwrite(f'{undistortedplates_dir}/UNDISTORTED_{fname}.png',dst)