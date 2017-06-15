import cv2
import time
import subprocess
import os
import sys
import argparse

def framecapture(username, password, protocol, camerapath, interval, nbframe, created, savepath, i):
	camera = str(protocol) + "://" + str(username) + ":" + str(password) + "@" + str(camerapath)
	vcap = cv2.VideoCapture(camera)
	filename  = savepath + "/" + str(i) + ".png"
	grabbed, frame = vcap.read()
	cv2.imwrite(filename, frame)
	statinfo = os.stat(filename)
	vcap.release()
	if statinfo.st_size < 5:
		i = i - 1
	
def videoexport(fps, finalname, created, outputpath, savepath):
	print("\n[+] Creating video file please wait... ")
	FNULL = open(os.devnull, 'w')
	subprocess.call(["avconv", "-r", str(fps), "-i", str(savepath) + '/%d.png', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', str(outputpath) + str(finalname)], stdout=FNULL, stderr=subprocess.STDOUT)
	print("\n[!] Congrats ! Filename: " + str(finalname))

# Argument parsing

parser = argparse.ArgumentParser()

parser.add_argument('-u', dest='username', help='Camera username', type=str)
parser.add_argument('-p', dest='password', help='Camera password', type=str)
parser.add_argument('-t', dest='protocol', help='Type of stream (ex:rtsp, http)', type=str)
parser.add_argument('-c', dest='camerapath', help='Camera path (ex:\'192.168.1.75/live/ch0\')', type=str)
parser.add_argument('-l', dest='length', help='Length of the output video (in seconds)', type=int)
parser.add_argument('-e', dest='eventlast', help='How long will the event last (in hours)', type=int)
parser.add_argument('-n', dest='correction', help='How long will the event last (in hours)', type=int)
parser.add_argument('-f', dest='fps', help='frame per seconds', type=int)

args = parser.parse_args()

username = args.username
password = args.password
protocol = args.protocol
camerapath = args.camerapath
fps = args.fps
length = args.length
eventlast = args.eventlast
correction = args.correction

# Camera info

camera = str(protocol) + "://" + str(username) + ":" + str(password) + "@" + str(camerapath)
cameraip = camerapath.split('/')[0]
resetcommand = ("http://" + str(username) + ":" + str(password) + "@" + str(cameraip) + ":80/hy-cgi/device.cgi?cmd=sysreboot")

# Get video info

created = time.strftime("%D")
created = created.replace('/', '')

finalname = (str(created) + "-" + str(fps) + "-" + str(length) + "-" + str(eventlast) + ".mp4" )



# make sure savepath exist
savepath = "autopng/" + str(created)
outputpath = 'output/'
logpath = 'logs/'
try: 
    os.makedirs(savepath)
except OSError:
    if not os.path.isdir(savepath):
        raise
try: 
    os.makedirs(outputpath)
except OSError:
    if not os.path.isdir(outputpath):
        raise
try: 
    os.makedirs(logpath)
except OSError:
    if not os.path.isdir(logpath):
        raise
# Video specs calculations

nbframe = fps * length
eventlastsec = eventlast * 3600
askedinterval = eventlastsec / nbframe

# Correct the interval, camera take 4 seconde to react when we try to grab image (cheap camera lol)
interval = askedinterval - correction

if interval < 1:
	interval = 0
# Validate infos before starting capture
i = 0
launched = time.strftime("%c")

with open(str(logpath) + str(created), 'a') as logfile:
	log = ("\n" + str(finalname) + "\nFps:" + str(fps) + "\nEventlast:" + str(eventlast) + "\nFinalVideo:" + str(length) + "\nNbframe:" + str(nbframe) + "\nInterval:" + str(askedinterval))
	logfile.write(log)
	logfile.close()

while (i < 30):

	try:

		# Get info for how long left
		frameleft = nbframe - i
		timeleft = frameleft * askedinterval / 60
		timeleft = round(timeleft, 0)
		# Grab the frame
		framecapture(username, password, protocol, camerapath, interval, nbframe, created, savepath, i)
		time.sleep(interval)
		i = i + 1
	except Exception as e:
		print (e)
# Capture is over, putting all the images together to create video file
videoexport(fps, finalname, created, outputpath)
