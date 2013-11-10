quantified-selfies
==================

Take a photo of yourself every day using your webcam.

```
usage: quantifiedselfies.py [-h] [-i CAMERA_INDEX] [-d DIR] [-c CASCADE] [-w]
                            [-b] [--random_interval RANDOM_INTERVAL]
                            [--retry_interval RETRY_INTERVAL]
```

Take a photo containing a face with your webcam after an random interval.

If no face was found, wait another random interval and try again.

Tip: schedule this to run daily.

```
optional arguments:
  -h, --help            show this help message and exit
  -i CAMERA_INDEX, --camera_index CAMERA_INDEX
                        Camera index. Usually 0 but try other integers.
                        (default: 0)
  -d DIR, --dir DIR     Directory to save photos (default:
                        /Users/hugo/Dropbox/images/faces/)
  -c CASCADE, --cascade CASCADE
                        Haar cascade file (default: /Users/hugo/macports/share
                        /OpenCV/haarcascades/haarcascade_frontalface_alt.xml)
  -w, --window          Show camera image in window (default: False)
  -b, --box             Draw a box around the detected face (default: False)
  --random_interval RANDOM_INTERVAL
                        Max hours to wait before taking a photo (default: 3)
  --retry_interval RETRY_INTERVAL
                        Max hours to wait between attempts at taking a photo,
                        in case no face detected (default: 1)
```