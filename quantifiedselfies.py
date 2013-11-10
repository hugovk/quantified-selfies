#!/usr/bin/env python
"""
Take a photo containing a face with your webcam after an random interval.
If no face was found, wait another random interval and try again.
Tip: schedule this to run daily.
"""
import argparse
import cv2.cv as cv
import datetime
import os
import time
from random import randrange

# Parameters for haar detection
# From the API:
# The default parameters (scale_factor=2, min_neighbors=3, flags=0) are tuned 
# for accurate yet slow object detection. For a faster operation on real video 
# images the settings are: 
# scale_factor=1.2, min_neighbors=2, flags=CV_HAAR_DO_CANNY_PRUNING, 
# min_size=<minimum possible face size

min_size = (20, 20)
image_scale = 2
haar_scale = 1.2
min_neighbors = 2
haar_flags = 0

count = 10 # Don't save first face as it could be blurred if just entering the scene
window_name = "Quantified Selfies"

def image_from_camera(camera_index):
    cascade = cv.Load(args.cascade)
    face_found = False
    ready_to_save = False
    face_saved = False
    attempts = 0
    
    capture = cv.CreateCameraCapture(int(camera_index))
#    cv.WaitKey(5000) # For Mac camera to wake up [1]

    cv.NamedWindow(window_name, 1)

    if capture:
        frame_copy = None
        while not face_saved:
            frame = cv.QueryFrame(capture)
            if not frame:
                cv.WaitKey(10) # Was 0,     but give Mac cam a chance to wake up [1]
                continue       # Was break, but give Mac cam a chance to wake up [1]
            if not frame_copy:
                frame_copy = cv.CreateImage((frame.width,frame.height),
                                            cv.IPL_DEPTH_8U, frame.nChannels)
            if frame.origin == cv.IPL_ORIGIN_TL:
                cv.Copy(frame, frame_copy)
            else:
                cv.Flip(frame, frame_copy, 0)
            
            face_saved = detect_and_save(frame_copy, cascade)
            if face_found:
                count -= 1
                if count == 0:
                    ready_to_save = True

            if cv.WaitKey(10) >= 0:
                break
            attempts += 1
            if attempts >= 160: # about a minute on my machine
                # Try again later
                return False

        return True

def timestamp_filename():
    timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%d-%H%M")
    filename = os.path.join(args.dir, timestamp+".jpg")
    print filename
    return filename


def detect_and_save(img, cascade):
    global count
    saved = False
    
    # allocate temporary images
    gray = cv.CreateImage((img.width,img.height), 8, 1)
    small_img = cv.CreateImage((cv.Round(img.width / image_scale),
                   cv.Round (img.height / image_scale)), 8, 1)

    # convert color input image to grayscale
    cv.CvtColor(img, gray, cv.CV_BGR2GRAY)

    # scale input image for faster processing
    cv.Resize(gray, small_img, cv.CV_INTER_LINEAR)

    cv.EqualizeHist(small_img, small_img)

    if(cascade):
        t = cv.GetTickCount()
        faces = cv.HaarDetectObjects(small_img, cascade, cv.CreateMemStorage(0),
                                     haar_scale, min_neighbors, haar_flags, min_size)
        t = cv.GetTickCount() - t
        print "detection time = %gms" % (t/(cv.GetTickFrequency()*1000.))
        if faces:
            if args.box:
                for ((x, y, w, h), n) in faces:
                    # the input to cv.HaarDetectObjects was resized, so scale the 
                    # bounding box of each face and convert it to two CvPoints
                    pt1 = (int(x * image_scale), int(y * image_scale))
                    pt2 = (int((x + w) * image_scale), int((y + h) * image_scale))
                    cv.Rectangle(img, pt1, pt2, cv.RGB(255, 0, 0), 3, 8, 0)
            
            count -= 1
            if count <= 0:
                cv.SaveImage(timestamp_filename(), img)
                saved = True

    if args.window:
        cv.ShowImage(window_name, img)

    return saved

def create_dirs(dir):
    import os
    import shutil
    if not os.path.isdir(dir):
        os.makedirs(dir)

def sleep_for_up_to(hours):
    if hours == 0:
        print "No sleep"
        return
    
    seconds = randrange(hours * 60 * 60) # max time
    print "Sleep for", seconds/60, "minutes"
    time.sleep(seconds)
    print "Woke up"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Take a photo containing a face with your webcam after an random interval. If no face was found, wait another random interval and try again. Tip: schedule this to run daily.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', '--camera_index', type=int, default=0,
        help="Camera index. Usually 0 but try other integers.")
#     parser.add_argument('-b', '--begin', type=int, default=1,
#         help="Photo to begin at")
    parser.add_argument('-d', '--dir', default="/Users/hugo/Dropbox/images/faces/",
        help="Directory to save photos")
    parser.add_argument('-c', '--cascade', 
        help="Haar cascade file", 
        default = '/Users/hugo/macports/share/OpenCV/haarcascades/haarcascade_frontalface_alt.xml')
    parser.add_argument('-w', '--window', action='store_true',
        help="Show camera image in window")
    parser.add_argument('-b', '--box', action='store_true',
        help="Draw a box around the detected face")
    parser.add_argument('--random_interval', type=int, default=3,
        help="Max hours to wait before taking a photo")
    parser.add_argument('--retry_interval', type=int, default=1,
        help="Max hours to wait between attempts at taking a photo, in case no face detected")
    args = parser.parse_args()

    try: import timing # optional
    except: pass

    print args

    sleep_for_up_to(args.random_interval)

    create_dirs(args.dir)
    saved = False
    while not saved:
        saved = image_from_camera(args.camera_index)
        cv.DestroyWindow(window_name)
        if not saved:
            sleep_for_up_to(args.retry_interval)

# End of file
