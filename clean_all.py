import os


chessboard_dir = './chessboard_images/'
stickyplates_dir = './stickyplate_images/'
undistortedplates_dir = './undistorted_images'

paths = [f"{chessboard_dir}/output_allbnw", 
        f"{chessboard_dir}/output_success", 
        f"{chessboard_dir}/result_params",
        undistortedplates_dir,
        stickyplates_dir,
        chessboard_dir]

for p in paths:
    print(f"Cleaning: {p}")
    if p in [chessboard_dir, stickyplates_dir]:
        os.system(f"rm -rf {p}/*.jpg")
    else:
        os.system(f"rm -rf {p}/*")
