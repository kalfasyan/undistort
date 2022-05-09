# undistort  

Simple package to undistort images.  

1. Place all chessboard images in `chessboard_images/` folder.
2. Place all your sticky plate images (or whatever you want to undistort) in `stickyplate_images/` folder.
3. Run ```python main.py```. All undistorted images will be stored in an automatically created folder named `undistorted_images/`.  
4. (optional) Run ```python clean_all.py``` to clean all your directories and prepare them for copying the new session. 

Dependencies: `numpy`,`opencv`

**NOTE**: If you work on Windows, you will encounter issues with the file-paths. To solve them you have some options: 1) replace strings with "raw strings" (example: r"this is a raw string"), 2) make sure to replace all "/" characters in `main.py` and `clean_all.py` with "\\\\" (ignore the quotes) or 3) try using Python's pathlib to handle paths.  
