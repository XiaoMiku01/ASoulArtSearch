import cv2
import numpy as np
import json


async def pHash(img, leng=32, wid=32):
    img = cv2.resize(img, (leng, wid))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    dct = cv2.dct(np.float32(gray))
    dct_roi = dct[0:8, 0:8]
    avreage = np.mean(dct_roi)
    phash_01 = (dct_roi > avreage)+0
    phash_list = phash_01.reshape(1, -1)[0].tolist()
    hash = ''.join([str(x) for x in phash_list])
    return hex(int(hash, 2))


async def read_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data


def Hamming_distance(hash1, hash2):
    num = 0
    for index in range(len(hash1)):
        if hash1[index] != hash2[index]:
            num += 1
    return num
