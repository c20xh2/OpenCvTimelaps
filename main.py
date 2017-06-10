import cv2
import time
import subprocess
import os
import sys


def framecapture(username, password, protocol, camerapath, interval, nbframe, i):
	camera = str(protocol) + "://" + str(username) + ":" + str(password) + "@" + str(camerapath)
	vcap = cv2.VideoCapture(camera)
	filename  = "png/capture_" + str(i) + ".png"
	grabbed, frame = vcap.read()
	cv2.imwrite(filename, frame)
	vcap.release()
	
def videoexport(fps, finalname):
	print("\n[+] Creating video file please wait... ")
	FNULL = open(os.devnull, 'w')
	subprocess.call(["avconv", "-r", str(fps), "-i", 'png/capture_%d.png', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', 'video/' + str(finalname)], stdout=FNULL, stderr=subprocess.STDOUT)
	print("\n[!] Congrats ! Filename: " + str(finalname))



print ("\n" *200)

# Camera info
print ("\n###### Camera Info ######")
username = input("\n[+] Enter username for the camera: ")
password = input(" [|] Enter password for the camera: ")
protocol = input(" [|] Enter protocol of the stream (ex: http, rtsp): ")
camerapath = input(" [|] Enter path of the camera (ex: 192.168.1.75/live/ch0): ")


# Get video info
print ("\n###### Videos Info ######")
fps = int(input("\n[+] Enter Frame per second of final video: "))
length = int(input(" [|] Enter length of final video (in seconds): "))
eventlast = float(input(" [|] How long the event will last (in hours): "))
finalname = input(" [|] Please enter the name for the final file (don't forget the .mp4): ")
correction = int(input(" [|] Network lag ? Correct the interval here (value will be remove from interval): "))

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
print ("\n" *200)

print ("###### Validations ######")
print ("\n[+] Output file name: " + str(finalname))
print (" [|] Event length: " + str(eventlast) + " h.")
print (" [|] Final Video length: " + str(length) + " sec.")

print ("\n[+] Video specs: ")
print (" [|] Fps: " + str(fps) +".")
print (" [|] Number of frames: " + str(nbframe) + ".") 
print (" [|] Interval between shots: " + str(askedinterval) + " sec.")
print ("")

# Ready to launch ?
launch = input('[*] Ready ? (y/n) : ')
if launch == ('n'):
	print ('\nAbording Capture...')

elif launch == ('y'):
	launched = time.strftime("%c")
	print ('\nStarting Capture...')
	while (i < nbframe):
		try:

			# Get info for how long left
			frameleft = nbframe - i
			timeleft = frameleft * askedinterval / 60
			timeleft = round(timeleft, 0)
			
			# Grab the frame
			framecapture(username, password, protocol, camerapath, interval, nbframe, i)
			time.sleep(interval)
			
			# Print Progress
			print ("\n" * 200)
			print ("[+] Process started: " + str(launched))
			print (" [|] Current time: " + time.strftime("%c"))
			print ("\n[+] Video specs: ")
			print (" [|] Fps: " + str(fps) +".")
			print (" [|] Number of frames: " + str(nbframe) + ".") 
			print (" [|] Interval between shots: " + str(askedinterval) + " sec.")
			print ("")
			print ("\n[+] " + str(i) + "/" + str(nbframe) +" Frames captured")
			print (" | " + str(timeleft) + " minutes left")
			print ("\n" * 5)
			
			i = i + 1
		except KeyboardInterrupt:
			print ("\n[!] Keyboard Interrupt ! ")
			videoexport(fps, finalname)
			sys.exit()
	# Capture is over, putting all the images together to create video file
	videoexport(fps, finalname)
	
	

else:
	print ('\nAbording Capture...')
