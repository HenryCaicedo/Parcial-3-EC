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

#Creates 30 frames from the input video
def createFrames():

    #Playing video from file:
    cap = cv2.VideoCapture('video.mp4')
    
    #Duration of the video
    duration = VideoFileClip("video.mp4").duration

    #Create frames folder
    try:
        if not os.path.exists('./Output/Original/frames'):
            os.makedirs('./Output/Original/frames')
    except OSError:
        print ('Error: Creating directory of frames')

    #Generates frames
    currentFrame = 0
    while(True and currentFrame<=30):

        #True: One frame per second is generated (Only the first 30 seconds)
        #False: Only the first 30 frames of the video are generated.
        if(duration>30):
            cap.set(cv2.CAP_PROP_POS_MSEC,(currentFrame*1000))

        #Capture frame-by-frame
        ret, frame = cap.read()

        #Saves image of the current frame in jpg file
        name = './Output/Original/frames/frame' + str(currentFrame) + '.jpg'
        print ('Creating..' + name)
        cv2.imwrite(name, frame)

        #Stop duplicate images
        currentFrame += 1

    #When everything is done, release the capture
    cap.release()
    cv2.destroyAllWindows()


#Extracts the audio of the video to a new .wav file 
def createWav():
    video = mp.VideoFileClip('video.mp4')
    video.audio.write_audiofile('./Output/Original/audio.wav')

#Resizes frames to 80x80
def resizeFrames():

    #Creates folder
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


#Creates a .wav with only the first second of the audio extracted from the video
def trimWav():
    print("Trimming audio file...")
    ffmpeg_extract_subclip("./Output/Original/audio.wav", 0, 1, targetname="./Output/Adapted/trimmed_audio.wav")


#Creates a txt file from the bmp converted frames
def createTxt(num):

    #Create bmp folder
    try:
        if not os.path.exists('./Output/Adapted/bmp'):
            os.makedirs('./Output/Adapted/bmp')
    except OSError:
        print ('Error: Creating directory of bmp')

    #Create txt folder
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
    im0 = im0.resize((80,80),Image.ANTIALIAS)
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


#Functions 
createFrames()
createWav()
resizeFrames()
trimWav()
for i in range(1,31):
    createTxt(str(i))


#REFERENCES
#DEV Community. 2021. Extracting Audio from Video Clips using Python. [online] Available at: <https://dev.to/itsaditya/extracting-audio-from-video-clips-using-python-9d8> [Accessed 16 November 2021].
#Youtube.com. 2021. [online] Available at: <https://www.youtube.com/watch?v=uL-wCzVMPsc> [Accessed 16 November 2021].
#Codegrepper.com. 2021. import cv2 could not be resolved Code Example. [online] Available at: <https://www.codegrepper.com/code-examples/c/import+cv2+could+not+be+resolved> [Accessed 16 November 2021].
#moviepy.editor, C., Burrows, T., Kirubakaran, E. and Yotcho, N., 2021. Can't import moviepy.editor. [online] Stack Overflow. Available at: <https://stackoverflow.com/questions/41923492/cant-import-moviepy-editor/41923539> [Accessed 16 November 2021].
#GitHub. 2021. AttributeError: module 'ffmpeg' has no attribute 'input' · Issue #174 · kkroening/ffmpeg-python. [online] Available at: <https://github.com/kkroening/ffmpeg-python/issues/174> [Accessed 16 November 2021].
#specified, F. and Ogden, G., 2021. FileNotFoundError: [WinError 2] system can't find the file specified. [online] Stack Overflow. Available at: <https://stackoverflow.com/questions/56235766/filenotfounderror-winerror-2-system-cant-find-the-file-specified> [Accessed 16 November 2021].
#Auth0 - Blog. 2021. Image Processing in Python with Pillow. [online] Available at: <https://auth0.com/blog/image-processing-in-python-with-pillow/> [Accessed 16 November 2021].
#First, M., 2021. How to Cut, Clip and Convert Audio Files in Python. [online] Blog | Mobile First. Available at: <https://mobilefirst.me/blog/2019/08/14/how-to-cut-clip-and-convert-audio-files-in-python/> [Accessed 16 November 2021].
#Python?, H. and Gogol, N., 2021. How to get the duration of a video in Python?. [online] Stack Overflow. Available at: <https://stackoverflow.com/questions/3844430/how-to-get-the-duration-of-a-video-in-python> [Accessed 16 November 2021].