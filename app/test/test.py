import cv2
import numpy as np

import urllib.request

req = urllib.request.urlopen("https://firebasestorage.googleapis.com/v0/b/fintrack-f100a.appspot.com/o/images%2Fbill.jpg?alt=media&token=cfbba278-bf1e-4578-b770-2fe09caeedd6")
arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
img = cv2.imdecode(arr, -1)

cv2.imshow('lalala', img)
if cv2.waitKey() & 0xff == 27: quit()