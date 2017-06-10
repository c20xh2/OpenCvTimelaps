import cv2
import time
import subprocess
import os


def framecapture(username, password, protocol, camerapath, interval, nbframe, i):
	camera = str(protocol) + "://" + str(username) + ":" + str(password) + "@" + str(camerapath)
	vcap = cv2.VideoCapture(camera)
	filename  = "capture_" + str(i) + ".png"
	grabbed, frame = vcap.read()
	cv2.imwrite(filename, frame)
	vcap.release()
	


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
length = int(input("[|] Enter length of final video (in seconds): "))
eventlast = float(input("[|] How long the event will last (in hours): "))
finalname = input("[|] Please enter the name for the final file (don't forget the .mp4): ")

# Video specs calculations

nbframe = fps * length
eventlastsec = eventlast * 3600
interval = eventlastsec / nbframe
interval = round(interval, 0)

i = 0
time.sleep(1)
# Validate infos before starting capture

print ("\n" *200)

print ("###### Validations ######")
print ("\n[+] Output file name: " + str(finalname))
print (" [|] Event length: " + str(eventlast) + " h.")
print (" [|] Final Video length: " + str(length) + " sec.")

print ("\n[+] Video specs: ")
print (" [|] Fps: " + str(fps) +".")
print (" [|] Number of frames: " + str(nbframe) + ".") 
print (" [|] Interval between shots: " + str(interval) + " sec.")
print ("")

launch = input('[*] Ready ? (y/n) : ')

# Ready to launch ?
if launch == ('n'):
	print ('\nAbording Capture...')
elif launch == ('y'):
	print ('\nStarting Capture...')
	while (i < nbframe):

		# Get info for how long left
		frameleft = nbframe - i
		timeleft = frameleft * interval / 60
		timeleft = round(timeleft, 0)
		
		# Grab the frame
		framecapture(username, password, protocol, camerapath, interval, nbframe, i)
		time.sleep(interval)
		
		# Print Progress
		print ("\n" *200)
		print ("\n[+] Video specs: ")
		print (" [|] Fps: " + str(fps) +".")
		print (" [|] Number of frames: " + str(nbframe) + ".") 
		print (" [|] Interval between shots: " + str(interval) + " sec.")
		print ("")
		print ("\n[+] " + str(i) + "/" + str(nbframe) +" Captured")
		print ("| " + str(timeleft) + " minutes left")
		
		i = i + 1
	
	# Capture is over, putting all the images together to create video file

	print("\n[+] Creating video file please wait... ")
	FNULL = open(os.devnull, 'w')
	subprocess.call(["avconv", "-r", str(fps), "-i", 'capture_%d.png', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', str(finalname)], stdout=FNULL, stderr=subprocess.STDOUT)
	print("\n[!] Congrats ! Filename: " + str(finalname))

else:
	print ('\nAbording Capture...')
