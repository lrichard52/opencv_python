import cv2
import time
import numpy as np
from time import sleep
import RPi.GPIO as GPIO
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import argparse
from CountsPerSec import CountsPerSec
from VideoGet import VideoGet
from VideoShow import VideoShow
#from matplotlib import rc
from matplotlib.widgets import Button
#from matplotlib.figure import Figure
import threading
import queue
from vidgear.gears import CamGear

DIR = 20    # Direction GPIO Pin
STEP = 21   # Step GPIO Pin
CW = 1      # Clockwise Rotation
CCW = 0     # Counterclockwise Rotation
SPR = 200    # Steps per Revolution (360 / 1.8 )

#GPIO.cleanup()
GPIO.setmode(GPIO.BCM)
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(STEP, GPIO.OUT)

GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)

MODE = (14, 15, 18)
GPIO.setup(MODE, GPIO.OUT)

RESOLUTION = {'Full':(0,0,0),
              'Half':(1,0,0),
              '1/4' :(0,1,0),
              '1/8' :(1,1,0),
              '1/16':(0,0,1),
              '1/32':(1,0,1)}
GPIO.output(MODE, RESOLUTION['1/8'])

step_counta = 200
delaya = 1/2000 #1/800
GPIO.output(DIR, CW)
for i in range(step_counta):
    GPIO.output(STEP, GPIO.HIGH)
    sleep(delaya)
    GPIO.output(STEP, GPIO.LOW)
    sleep(delaya)



step_count = 1400
delay = 1/1500 #1/800

GPIO.output(DIR, CCW)

bolean0 = True
while bolean0 == True:
    input_state = GPIO.input(23)
    GPIO.output(STEP, GPIO.HIGH)
    sleep(delay)
    GPIO.output(STEP, GPIO.LOW)
    sleep(delay)
    if input_state == True:
        #print('First Home')
        bolean0 = False
        continue

GPIO.output(MODE, RESOLUTION['1/8'])    
GPIO.output(DIR, CW)
time.sleep(1)
soft_home = 200
delay_home = 1/1000       
for i in range(soft_home):
    GPIO.output(STEP, GPIO.HIGH)
    sleep(delay_home)
    GPIO.output(STEP, GPIO.LOW)
    sleep(delay_home)

delay_home1 = 1/250
GPIO.output(DIR, CCW)
bolean1 = True
while bolean1 ==True:
    input_state = GPIO.input(23)
    GPIO.output(STEP, GPIO.HIGH)
    sleep(delay_home1)
    GPIO.output(STEP, GPIO.LOW)
    sleep(delay_home1)
    if input_state == True:
        #print('Second Home')
        bolean1 = False
        continue
print('Initial Homing Complete')

"""
while True:
    input_state = GPIO.input(23)
    GPIO.output(STEP, GPIO.HIGH)
    sleep(delay)
    GPIO.output(STEP, GPIO.LOW)
    sleep(delay)
    if input_state == True:
        print('Unit Homed')
        time.sleep(0.1)
        break
"""

cap0 = cv2.VideoCapture(0)
cap0.set(3, 1920) # set the resolution
cap0.set(4, 1080)

cap1 = cv2.VideoCapture(2)
cap1.set(3, 1920) # set the resolution
cap1.set(4, 1080)

cap2 = cv2.VideoCapture(4)
cap2.set(3, 1920) # set the resolution
cap2.set(4, 1080)

cap3 = cv2.VideoCapture(6)
cap3.set(3, 1920) # set the resolution
cap3.set(4, 1080)


def cap0_capture():
    retval0, im0 = cap0.read()
    return im0

def cap1_capture():
    retval1, im1 = cap1.read()
    return im1

def cap2_capture():
    retval2, im2 = cap2.read()
    return im2

def cap3_capture():
    retval3, im3 = cap3.read()
    return im3


#Camera Warm-up / Ramping
ramp_frames = 30

time.sleep(0.25)
for i in range(ramp_frames):
    temp0 = cap0.read()
frame0 = cap0_capture()
cap0.release()

time.sleep(0.25)
for i in range(ramp_frames):
    temp1 = cap1.read()
frame1 = cap1_capture() 
cap1.release()

time.sleep(0.25)
for i in range(ramp_frames):
    temp2 = cap2.read()
frame2 = cap2_capture() 
cap2.release()

time.sleep(0.25)
for i in range(ramp_frames):
    temp3 = cap3.read()
frame3 = cap3_capture() 
cap3.release()

"""
ret_0,frame0 = cap0.read()
time.sleep(0.5)
cap0.release()
ret_1,frame1 = cap1.read()
time.sleep(0.5)
cap1.release()
ret_2,frame2 = cap2.read()
time.sleep(0.5)
cap2.release()
ret_3,frame3 = cap3.read()
time.sleep(0.5)
cap3.release()
"""

plt.figure()
plt.subplot(2,2,1)
plt.imshow(frame0)
plt.subplot(2,2,2)
plt.imshow(frame1)
plt.subplot(2,2,3)
plt.imshow(frame2)
plt.subplot(2,2,4)
plt.imshow(frame3)
plt.show()
"""
plt.figure()
plt.imshow(frame1)
plt.show()
"""
c_wash_frame0 = frame0[576:590, 610:620]  
c_wash_frame1 = frame1[576:590, 610:620]  
c_wash_frame2 = frame2[576:590, 610:620]   
c_wash_frame3 = frame3[576:590, 610:620]  

b_c_f0, g_c_f0, r_c_f0 = cv2.split(c_wash_frame0)
g_c_f0_diff = np.mean(g_c_f0)-abs((np.mean(b_c_f0) + np.mean(r_c_f0))/2)

b_c_f1, g_c_f1, r_c_f1 = cv2.split(c_wash_frame1)
g_c_f1_diff = np.mean(g_c_f1)-abs((np.mean(b_c_f1) + np.mean(r_c_f1))/2)

b_c_f2, g_c_f2, r_c_f2 = cv2.split(c_wash_frame2)
g_c_f2_diff = np.mean(g_c_f2)-abs((np.mean(b_c_f2) + np.mean(r_c_f2))/2)

b_c_f3, g_c_f3, r_c_f3 = cv2.split(c_wash_frame3)
g_c_f3_diff = np.mean(g_c_f3)-abs((np.mean(b_c_f3) + np.mean(r_c_f3))/2)

b_wash_frame0 = frame0[1015:1028, 1286:1294]
b_wash_frame1 = frame1[1015:1028, 1286:1294]
b_wash_frame2 = frame2[1015:1028, 1286:1294]
b_wash_frame3 = frame3[1015:1028, 1286:1294]

b_b_f0, g_b_f0, r_b_f0 = cv2.split(b_wash_frame0)
g_b_f0_diff = np.mean(g_b_f0)-((np.mean(b_b_f0) + np.mean(r_b_f0))/2)

b_b_f1, g_b_f1, r_b_f1 = cv2.split(b_wash_frame1)
g_b_f1_diff = np.mean(g_b_f1)-((np.mean(b_b_f1) + np.mean(r_b_f1))/2)

b_b_f2, g_b_f2, r_b_f2 = cv2.split(b_wash_frame2)
g_b_f2_diff = np.mean(g_b_f2)-((np.mean(b_b_f2) + np.mean(r_b_f2))/2)

b_b_f3, g_b_f3, r_b_f3 = cv2.split(b_wash_frame3)
g_b_f3_diff = np.mean(g_b_f3)-((np.mean(b_b_f3) + np.mean(r_b_f3))/2)

a_wash_frame0 = frame0[960:974, 1020:1030]
a_wash_frame1 = frame1[960:974, 1020:1030]
a_wash_frame2 = frame2[960:974, 1020:1030]
a_wash_frame3 = frame3[960:974, 1020:1030]

b_a_f0, g_a_f0, r_a_f0 = cv2.split(a_wash_frame0)
g_a_f0_diff = np.mean(g_a_f0)-((np.mean(b_a_f0) + np.mean(r_a_f0))/2)

b_a_f1, g_a_f1, r_a_f1 = cv2.split(a_wash_frame1)
g_a_f1_diff = np.mean(g_a_f1)-((np.mean(b_a_f1) + np.mean(r_a_f1))/2)

b_a_f2, g_a_f2, r_a_f2 = cv2.split(a_wash_frame2)
g_a_f2_diff = np.mean(g_a_f2)-((np.mean(b_a_f2) + np.mean(r_a_f2))/2)

b_a_f3, g_a_f3, r_a_f3 = cv2.split(a_wash_frame3)
g_a_f3_diff = np.mean(g_a_f3)-((np.mean(b_a_f3) + np.mean(r_a_f3))/2)


d_wash_frame0 = frame0[675:685, 905:921]
d_wash_frame1 = frame1[675:685, 905:921]
d_wash_frame2 = frame2[675:685, 905:921]
d_wash_frame3 = frame3[675:685, 905:921]

b_d_f0, g_d_f0, r_d_f0 = cv2.split(d_wash_frame0)
g_d_f0_diff = np.mean(g_d_f0)-((np.mean(b_d_f0) + np.mean(r_d_f0))/2)

b_d_f1, g_d_f1, r_d_f1 = cv2.split(d_wash_frame1)
g_d_f1_diff = np.mean(g_d_f1)-((np.mean(b_d_f1) + np.mean(r_d_f1))/2)

b_d_f2, g_d_f2, r_d_f2 = cv2.split(d_wash_frame2)
g_d_f2_diff = np.mean(g_d_f2)-((np.mean(b_d_f2) + np.mean(r_d_f2))/2)

b_d_f3, g_d_f3, r_d_f3 = cv2.split(d_wash_frame3)
g_d_f3_diff = np.mean(g_d_f3)-((np.mean(b_d_f3) + np.mean(r_d_f3))/2)

if np.mean(g_c_f0_diff) > 50:
    c_wash_cap = 0
if np.mean(g_c_f1_diff) > 50:
    c_wash_cap = 2
if np.mean(g_c_f2_diff) > 50:
    c_wash_cap = 4
if np.mean(g_c_f3_diff) > 50:
    c_wash_cap = 6
"""    
print(np.mean(g_c_f0_diff))
print(np.mean(g_c_f1_diff))
print(np.mean(g_c_f2_diff))
print(np.mean(g_c_f3_diff))
print(c_wash_cap)
"""
if np.mean(g_b_f0_diff) > 30:
    b_wash_cap = 0
if np.mean(g_b_f1_diff) > 30:
    b_wash_cap = 2
if np.mean(g_b_f2_diff) > 30:
    b_wash_cap = 4
if np.mean(g_b_f3_diff) > 30:
    b_wash_cap = 6
"""
print(np.mean(g_b_f0_diff))
print(np.mean(g_b_f1_diff))
print(np.mean(g_b_f2_diff))
print(np.mean(g_b_f3_diff))
"""
print(b_wash_cap)

if np.mean(g_a_f0_diff) > 35:
    a_wash_cap = 0
if np.mean(g_a_f1_diff) > 35:
    a_wash_cap = 2
if np.mean(g_a_f2_diff) > 35:
    a_wash_cap = 4
if np.mean(g_a_f3_diff) > 35:
    a_wash_cap = 6
"""
print('washerA')
print(np.mean(g_a_f0_diff))
print(np.mean(g_a_f1_diff))
print(np.mean(g_a_f2_diff))
print(np.mean(g_a_f3_diff))
"""
#print(a_wash_cap)

if np.mean(g_d_f0_diff) > 50:
    d_wash_cap = 0
if np.mean(g_d_f1_diff) > 50:
    d_wash_cap = 2
if np.mean(g_d_f2_diff) > 50:
    d_wash_cap = 4
if np.mean(g_d_f3_diff) > 50:
    d_wash_cap = 6
#print(d_wash_cap)

print("Camera Initialization Complete")

global good_part_count
good_part_count = 0


#Trims

#Washer Trims
a_s_x_t = 513
a_s_x_b = 518
a_s_y_t = 365
a_s_y_b = 370

a_d_x_t = 513
a_d_x_b = 518
a_d_y_t = 315
a_d_y_b = 320

b_s_x_t = 1175
b_s_x_b = 1180
b_s_y_t = 360
b_s_y_b = 365

b_d_x_t = 1175
b_d_x_b = 1180
b_d_y_t = 320
b_d_y_b = 325

c_s_x_t = 794
c_s_x_b = 799
c_s_y_t = 265
c_s_y_b = 270

c_d_x_t = 794
c_d_x_b = 799
c_d_y_t = 248
c_d_y_b = 253


#Centering Trims
a_c_x_t = 582
a_c_x_b = 656
a_c_y_t = 322
a_c_y_b = 397

b_c_x_t = 632
b_c_x_b = 704
b_c_y_t = 291
b_c_y_b = 364

c_c_x_t = 608
c_c_x_b = 688
c_c_y_t = 346
c_c_y_b = 426

options_a = {"CAP_PROP_FRAME_WIDTH ":1280, "CAP_PROP_FRAME_HEIGHT":720, "CAP_PROP_FPS ":60} # define tweak parameters

stream_a = CamGear(source=a_wash_cap, time_delay=1, logging=False, **options_a).start() # To open video stream on first index(i.e. 0) device

options_b = {"CAP_PROP_FRAME_WIDTH ":1280, "CAP_PROP_FRAME_HEIGHT":720, "CAP_PROP_FPS ":60} # define tweak parameters

stream_b = CamGear(source=b_wash_cap, time_delay=1, logging=False, **options_b).start()

options_c = {"CAP_PROP_FRAME_WIDTH ":1280, "CAP_PROP_FRAME_HEIGHT":720, "CAP_PROP_FPS ":60} # define tweak parameters

stream_c = CamGear(source=c_wash_cap, time_delay=1, logging=False, **options_c).start()

options_d = {"CAP_PROP_FRAME_WIDTH ":1280, "CAP_PROP_FRAME_HEIGHT":720, "CAP_PROP_FPS ":60} # define tweak parameters

stream_d = CamGear(source=d_wash_cap, time_delay=.25, logging=False, **options_d).start()

frame_da = 0
frame_dc = 0
#Start of main script
while True:
    print(frame_da)
    print(frame_dc)
    start = time.time()
    camera_capture_start = time.time()
    frame_a = 0
    frame_b = 0
    frame_c = 0
    frame_dc = 0
    frame_da = 0
    frame_db = 0
    time.sleep(0.5)
    frame_da = np.array(stream_d.read())
    time.sleep(0.5)
    #print(frame_da)
    print(np.mean(frame_da))
    if frame_da is None:
        break
    
    frame_a = stream_a.read()
    
    frame_b = stream_b.read()
    
    frame_c = stream_c.read()
    
    
    
    camera_capture_end = time.time()
    camera_capture_time = camera_capture_end - camera_capture_start
    #print("camera capture time:")
    #print(camera_capture_time)
    """
    plt.figure()
    plt.imshow(frame_a)
    plt.show()

    plt.figure()
    plt.imshow(frame_b)
    plt.show()

    plt.figure()
    plt.imshow(frame_c)
    plt.show()
    """
    start_basic_transforms = time.time()
    frame_db = np.array(np.rot90(frame_da, k=2))
    frame_aa = np.array(frame_a)

    frame_a = cv2.cvtColor(frame_a, cv2.COLOR_BGR2GRAY)
    frame_b = cv2.cvtColor(frame_b, cv2.COLOR_BGR2GRAY)
    frame_c = cv2.cvtColor(frame_c, cv2.COLOR_BGR2GRAY)
    frame_dc = cv2.cvtColor(frame_db, cv2.COLOR_BGR2GRAY)
    a_ttrim = frame_dc[a_s_y_t:a_s_y_b, a_s_x_t:a_s_x_b]
    b_ttrim = frame_dc[b_s_y_t:b_s_y_b, b_s_x_t:b_s_x_b]
    c_ttrim = frame_dc[c_s_y_t:c_s_y_b, c_s_x_t:c_s_x_b]

    a_dtrim = frame_dc[a_d_y_t:a_d_y_b, a_d_x_t:a_d_x_b]
    b_dtrim = frame_dc[b_d_y_t:b_d_y_b, b_d_x_t:b_d_x_b]
    c_dtrim = frame_dc[c_d_y_t:c_d_y_b, c_d_x_t:c_d_x_b]

    frame_a = frame_a[a_c_y_t:a_c_y_b, a_c_x_t:a_c_x_b]
    frame_b = frame_b[b_c_y_t:b_c_y_b, b_c_x_t:b_c_x_b]
    frame_c = frame_c[c_c_y_t:c_c_y_b, c_c_x_t:c_c_x_b]

  

    end_basic_transforms = time.time()
    time_basic_transforms = end_basic_transforms - start_basic_transforms
    #print("Basic Transforms Time:")
    #print(time_basic_transforms)


    washer_pressence_start = time.time()
    
    c_check_list = []
    b_check_list = []
    a_check_list = []
    d_check_list = []

    #Washer Pressence and Thickness

    
    
    fig, ax = plt.subplots(1)
    ax.imshow(frame_dc)
    a_s_rect = patches.Rectangle((a_s_x_t,a_s_y_t), (a_s_x_b-a_s_x_t),(a_s_y_b-a_s_y_t)
                                 , linewidth=1, edgecolor='r', facecolor='none')

    a_d_rect = patches.Rectangle((a_d_x_t,a_d_y_t), (a_d_x_b-a_d_x_t),(a_d_y_b-a_d_y_t)
                                 , linewidth=1, edgecolor='b', facecolor='none')

    b_s_rect = patches.Rectangle((b_s_x_t,b_s_y_t), (b_s_x_b-b_s_x_t),(b_s_y_b-b_s_y_t)
                                 , linewidth=1, edgecolor='r', facecolor='none')

    b_d_rect = patches.Rectangle((b_d_x_t,b_d_y_t), (b_d_x_b-b_d_x_t),(b_d_y_b-b_d_y_t)
                                 , linewidth=1, edgecolor='b', facecolor='none')

    c_s_rect = patches.Rectangle((c_s_x_t,c_s_y_t), (c_s_x_b-c_s_x_t),(c_s_y_b-c_s_y_t)
                                 , linewidth=1, edgecolor='r', facecolor='none')

    c_d_rect = patches.Rectangle((c_d_x_t,c_d_y_t), (c_d_x_b-c_d_x_t),(c_d_y_b-c_d_y_t)
                                 , linewidth=1, edgecolor='b', facecolor='none')
    
    ax.add_patch(a_s_rect)
    ax.add_patch(a_d_rect)

    ax.add_patch(b_s_rect)
    ax.add_patch(b_d_rect)

    ax.add_patch(c_s_rect)
    ax.add_patch(c_d_rect)
    plt.show()
    
    frame_da = 0
    frame_db = 0
    frame_dc = 0
    """
    plt.figure()
    plt.subplot(2,3,1)
    plt.imshow(a_ttrim, label='Washer A')
    plt.legend()
    plt.subplot(2,3,2)
    plt.imshow(b_ttrim, label='Washer B')
    plt.legend()  
    plt.subplot(2,3,3)
    plt.imshow(c_ttrim, label='Washer C')
    plt.legend()

    plt.subplot(2,3,4)
    plt.imshow(a_dtrim, label='Double Washer A')
    plt.legend()
    plt.subplot(2,3,5)
    plt.imshow(b_dtrim, label='Double Washer B')
    plt.legend()  
    plt.subplot(2,3,6)
    plt.imshow(c_dtrim, label='Double Washer C')
    plt.legend()
    
    plt.show()
    """
    a_t_avg = np.mean(a_ttrim)
    b_t_avg = np.mean(b_ttrim)
    c_t_avg = np.mean(c_ttrim)
    print('******')
    print(a_t_avg)
    print('******')
    a_d_avg = np.mean(a_dtrim)
    b_d_avg = np.mean(b_dtrim)
    c_d_avg = np.mean(c_dtrim)
    print(a_d_avg)
    print('******')
    a_wash = []
    b_wash = []
    c_wash = []

    if a_t_avg >= 125:
        a_wash.append(1)
    if a_t_avg <= 125:
        a_wash.append(0)

    if a_d_avg >= 80:
        a_wash.append(1)
    if a_d_avg <= 80:
        a_wash.append(0)

    if b_t_avg >= 125:
        b_wash.append(1)
    if b_t_avg <= 125:
        b_wash.append(0)

    if b_d_avg >= 80:
        b_wash.append(1)
    if b_d_avg <= 80:
        b_wash.append(0)
        
   
    if c_t_avg >= 100:
        c_wash.append(1)
    if c_t_avg <= 100:
        c_wash.append(0)

    if c_d_avg >= 100:
        c_wash.append(1)
    if c_d_avg <= 100:
        c_wash.append(0)
    
    washer_pressence_binary = 0
    if c_wash == [1,0] and b_wash == [1,0] and a_wash == [1,0]:
        washer_pressence_binary = 1
        
    washer_pressence_end = time.time()
    washer_pressence_time = washer_pressence_end - washer_pressence_start
    #print("Washer Pressence Time:")
    #print(washer_pressence_time)

    centering_start = time.time()
    
    """
    plt.figure()
    plt.imshow(frame_a)
    plt.show()
    
    plt.figure()
    plt.imshow(frame_b)
    plt.show()

    plt.figure()
    plt.imshow(frame_c)
    plt.show()
    """   
    cv2.circle(frame_a,(37,37),25,(0,0,0),-1)
    cv2.circle(frame_a,(37,37),50,(0,0,0),25)
    
    #plt.figure()
    #plt.imshow(frame_a)
    #plt.show()
    
    cv2.circle(frame_b,(36,36),25,(0,0,0),-1)
    cv2.circle(frame_b,(36,36),50,(0,0,0),25)
    
    #plt.figure()
    #plt.imshow(frame_b)
    #plt.show()
    
    cv2.circle(frame_c,(40,40),25,(0,0,0),-1)
    cv2.circle(frame_c,(40,39),53,(0,0,0),25)
    cv2.rectangle(frame_c,(7,23),(20,34),(0,0,0),-20)
    cv2.rectangle(frame_c,(63,23),(75,34),(0,0,0),-20)

    #plt.figure()
    #plt.imshow(frame_c)
    #plt.show()
    
    frame_c_flat = frame_c.flatten()
    frame_a_flat = frame_a.flatten()
    frame_b_flat = frame_b.flatten()
    
    frame_c_count = 0
    frame_a_count = 0
    frame_b_count = 0

    a_wash_binary = 0
    b_wash_binary = 0
    c_wash_binary = 0

    for i in frame_a_flat:
        if i>225:
            frame_a_count = frame_a_count + 1
            
    print(frame_a_count)

    if frame_a_count <= 200:
        a_wash_binary = 1

    for i in frame_b_flat:
        if i>225:
            frame_b_count = frame_b_count + 1
    print(frame_b_count)
    if frame_b_count <= 350:
        b_wash_binary = 1

    for i in frame_c_flat:
        if i>170:
            frame_c_count = frame_c_count + 1
    print(frame_c_count)
    if frame_c_count <= 300:
        c_wash_binary = 1

    a_wash_center_string = ''
    b_wash_center_string = ''
    c_wash_center_string = ''
    
    if a_wash_binary == 1:
        a_wash_center_string = 'A Washer Centered'
    else:
        a_wash_center_string = 'A Washer is NOT Centered'
    if b_wash_binary == 1:
        b_wash_center_string = 'B Washer Centered'
    else:
        b_wash_center_string = 'B Washer is NOT Centered'
    if c_wash_binary == 1:
        c_wash_center_string = 'C Washer Centered'
    else:
        c_wash_center_string = 'C Washer is NOT Centered'

        
    general_presence_string = ''
    a_wash_pressence_string = ''
    b_wash_pressence_string = ''
    c_wash_pressence_string = ''
    
    if a_wash == [1,0]:
        a_wash_pressence_string = 'A-Washer Present'
    if a_wash == [1,1]:
        a_wash_pressence_string = 'A-Washer is Double Washer'
    if a_wash == [0,0]:
        a_wash_pressence_string = 'A-Washer is Missing'

    if b_wash == [1,0]:
        b_wash_pressence_string = 'B-Washer Present'
    if b_wash == [1,1]:
        b_wash_pressence_string = 'B-Washer is Double Washer'
    if b_wash == [0,0]:
        b_wash_pressence_string = 'B-Washer is Missing'

    if c_wash == [1,0]:
        c_wash_pressence_string = 'C-Washer Present'
    if c_wash == [1,1]:
        c_wash_pressence_string = 'C-Washer is Double Washer'
    if c_wash == [0,0]:
        c_wash_pressence_string = 'C-Washer is Missing'

  
    centering_end = time.time()
    centering_time = centering_end - centering_start
    #print("Washer Centering Time:")
    #print(centering_time)


    plotting_start = time.time()    
    good_part_str = "Good Part Count: "   
    part_count_string = good_part_str + str(good_part_count)
    #print(good_part_count)

    
    ax = plt.subplot(111)
    #ax.tick_params(axis=u'both',which=u'both', length=0)
        
    if a_wash == [1,0] and b_wash == [1,0] and c_wash == [1,0]:
        ax.text(50,200,'All Washers Present', fontsize=15, color='Green')
        ax.text(50,100,part_count_string,fontsize=15,color='Yellow')
    else:
        ax.text(50,300, a_wash_pressence_string, fontsize=15, color='Red')
        ax.text(50,400, b_wash_pressence_string, fontsize=15, color='Red')
        ax.text(50,500, c_wash_pressence_string, fontsize=15, color='Red')
        ax.text(50,100,part_count_string,fontsize=15,color='Yellow')
    if a_wash_binary == 1 and b_wash_binary == 1 and c_wash_binary == 1:
        ax.text(50,600, 'All Washers Centered', fontsize=15, color='Green')
    else:
        ax.text(50,600, a_wash_center_string, fontsize=15, color='Red')
        ax.text(50,700, b_wash_center_string, fontsize=15, color='Red')
        ax.text(50,800, c_wash_center_string, fontsize=15, color='Red')
            
    def _yes(event):
        plt.close('all')

    def _restart_count(event):
        global good_part_count
        good_part_count=0
        plt.close('all')
        print(good_part_count)
    ax.imshow(frame_aa, cmap="gray", vmin=0, vmax=255)
    axcut = plt.axes([0.6, 0.05, 0.1, 0.075])
    axcut1 = plt.axes([0.75, 0.05, 0.2, 0.075])
    bcut = Button(axcut, 'NEXT', color='white', hovercolor='green')
    bcut.on_clicked(_yes)
    c_cut = Button(axcut1, 'RESET COUNT', color='white', hovercolor='green')
    c_cut.on_clicked(_restart_count)

    
    #mng  = ax.get_current_fig_manager()
    #mng.window.showMaximized()
    #mng.resize(*mng.window.maxsize())
    ax.set_xticks([])
    ax.set_yticks([])
    plt.show()

    plotting_end = time.time()
    plotting_time = plotting_end - plotting_start
    print("Plotting Time:")
    print(plotting_time)
    
    end = time.time()
    print("\n")
    print("\n")
    print("Run Time:")
    print(end-start)
    
    if a_wash_binary == 1 and b_wash_binary == 1 and c_wash_binary == 1 and washer_pressence_binary == 1:
        frame_da = 'hiipo'
        frame_dc= 'hiipo'
        good_part_count = good_part_count + 1
        GPIO.output(MODE, RESOLUTION['1/4'])

        step_count = 1750
        delay = 1/3000 #1/800
        GPIO.output(DIR, CW)
        for i in range(step_count):
            GPIO.output(STEP, GPIO.HIGH)
            sleep(delay)
            GPIO.output(STEP, GPIO.LOW)
            sleep(delay)
        
        GPIO.output(DIR, CCW)
        step_count1 = 1250
        delay1 = 1/3000
        for i in range(step_count1):
            GPIO.output(STEP, GPIO.HIGH)
            sleep(delay1)
            GPIO.output(STEP, GPIO.LOW)
            sleep(delay1)

        delay = 1/1500
        bolean0 = True
        while bolean0 == True:
            input_state = GPIO.input(23)
            GPIO.output(STEP, GPIO.HIGH)
            sleep(delay)
            GPIO.output(STEP, GPIO.LOW)
            sleep(delay)
            if input_state == True:
                print('First Home')
                bolean0 = False
                continue

        GPIO.output(MODE, RESOLUTION['1/8'])    
        GPIO.output(DIR, CW)
        time.sleep(1)
        soft_home = 60
        delay_home = 1/1000       
        for i in range(soft_home):
            GPIO.output(STEP, GPIO.HIGH)
            sleep(delay_home)
            GPIO.output(STEP, GPIO.LOW)
            sleep(delay_home)
            
        delay_home1 = 1/500
        GPIO.output(DIR, CCW)
        bolean1 = True
        while bolean1 ==True:
            input_state = GPIO.input(23)
            GPIO.output(STEP, GPIO.HIGH)
            sleep(delay_home1)
            GPIO.output(STEP, GPIO.LOW)
            sleep(delay_home1)
            if input_state == True:
                print('Second Home')
                bolean1 = False
                continue
    else:
        frame_dc = "hippo"
        frame_da = "hippo"
        print('frame_d_wiped')
GPIO.cleanup()
end = time.time()
print("\n")
print("\n")
print("Run Time:")
print(end-start)
