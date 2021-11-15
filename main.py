import cv2
import numpy as np
import os
import moviepy.editor as mp
from moviepy.editor import VideoFileClip
from PIL import Image
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import imageio
import matplotlib.pyplot as plt


dir_path = os.path.dirname(os.path.realpath('videp.mp4'))

def createFrames():
    #Playing video from file:
    cap = cv2.VideoCapture('video.mp4')
    
    duration = VideoFileClip("video.mp4").duration

    try:
        if not os.path.exists('./Output/Original/frames'):
            os.makedirs('./Output/Original/frames')
    except OSError:
        print ('Error: Creating directory of frames')

    currentFrame = 0
    while(True and currentFrame<=30):

        #True: Se guarda un frame por segundo (Sólo los primeros 30 segundos)
        #False: Se guardan los primeros 30 frames del video.
        if(duration>30):
            cap.set(cv2.CAP_PROP_POS_MSEC,(currentFrame*1000))

        #Capture frame-by-frame
        ret, frame = cap.read()

        #Saves image of the current frame in jpg file
        name = './Output/Original/frames/frame' + str(currentFrame) + '.jpg'
        print ('Creating..' + name)
        cv2.imwrite(name, frame)

        #To stop duplicate images
        currentFrame += 1

    #When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

def createWav():
    video = mp.VideoFileClip('video.mp4')
    video.audio.write_audiofile('./Output/Original/audio.wav')

def resizeFrames():
    try:
        if not os.path.exists('./Output/Adapted/framesResized'):
            os.makedirs('Output/Adapted/framesResized')
    except OSError:
        print ('Error: Creating directory of framesResized')
    for i in range(1,31):
        name = './Output/Original/frames/frame' + str(i) + '.jpg'
        print('Resizing..' + name)
        image = Image.open(name)
        new_image = image.resize((80, 80))
        new_image.save('./Output/Adapted/framesResized/frame' + str(i) + '.jpg')


def trimWav():
    print("Trimming audio file...")
    ffmpeg_extract_subclip("./Output/Original/audio.wav", 0, 1, targetname="./Output/Adapted/trimmed_audio.wav")


def createTxt(num):
    try:
        if not os.path.exists('./Output/Adapted/bmp'):
            os.makedirs('./Output/Adapted/bmp')
    except OSError:
        print ('Error: Creating directory of bmp')

    try:
        if not os.path.exists('./Output/Adapted/txt'):
            os.makedirs('./Output/Adapted/txt')
    except OSError:
        print ('Error: Creating directory of txt')

    dirpath = './Output/Adapted/'
    print('current directory is: ' + dirpath)
    foldername = 'bmp'
    print('Directory name is : ' + foldername)

    #2
    imagen = imageio.imread ('./Output/Adapted/framesResized/frame'+num+'.jpg')
    im0 = Image.fromarray(imagen)
    im0 = im0.resize((320, 240),Image.ANTIALIAS)
    imagen = np.asarray(im0,'uint8')
    im1 = Image.fromarray(imagen)
    im1 = im1.save('./Output/Adapted/bmp/frame'+num+'.bmp')

    #3
    print(imagen.shape)
    red = imagen [:,:,0].flatten()
    print(red.shape)
    green = imagen [:,:,1].flatten()
    print(green.shape)
    blue = imagen [:,:,2].flatten()
    print(blue.shape)

    #4
    azul = np.uint16(np.trunc((blue/255.0)*(2**5-1)))
    verde = np.uint16(np.trunc((green/255.0)*(2**6-1))*(2**5))
    rojo = np.uint16(np.trunc((red/255.0)*(2**5-1))*(2**11))
    representacion = np.uint16(rojo+verde+azul)

    #5
    for i in range(20):
        print("     .word  "+hex(representacion[i]))

    f = open('./Output/Adapted/txt/frame'+num+'.txt',"w")
    for i in range(len(representacion)):
        f.write("     .word  "+hex(representacion[i])+"\n")
    f.close()



createFrames()
createWav()
resizeFrames()
trimWav()

for i in range(1,31):
    createTxt(str(i))
