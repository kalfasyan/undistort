# undistort  

Simple package to undistort images.  

1. Place all chessboard images in `chessboard_images/` folder.
2. Place all your sticky plate images (or whatever you want to undistort) in `stickyplate_images/` folder.
3. Run ```python main.py```. All undistorted images will be stored in an automatically created folder named `undistorted_images/`.  

Dependencies: `numpy`,`opencv`

**NOTE**: If you work on Windows, make sure to replace all "/" characters in `main.py` with "\\\" (ignore the quotes). This might be fixed later using Python's pathlib.  
