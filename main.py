import cv2
import time



def framecapture(username, password, protocol, camerapath, interval, nbframe, i = 1):
	print ("Opening Camera: ")
	camera = str(protocol) + "://" + str(username) + ":" + str(password) + "@" + str(camerapath)
	vcap = cv2.VideoCapture(camera)

	while(i < nbframe):
		filename  = "capture_" + str(i) + ".png"
		grabbed, frame = vcap.read()
		cv2.imwrite(filename, frame)
		print ("\n[+] " + str(filename) + " Capture saved: " + str(i))
		print ("[-] Next capture in: " + str(interval) + "sec.")
		time.sleep(interval)
		i = i + 1
	print ("\n\n[*] Successful.")


username = "admin"
password = "hidden"
protocol = "rtsp"
camerapath = "192.168.1.75/live/ch0"

fps = 24
length = 45

nbframe = fps * length
eventlast = 8
eventlastsec = eventlast * 3600
interval = eventlastsec / nbframe
interval = round(interval, 0) - 1

print ("\n" *200)
print ("[+] Event length: " + str(eventlast) + " h.")
print ("[+] Final Video length: " + str(length) + " sec.")

print ("\n[+] Fps: " + str(fps) +".")
print ("[+] Number of frames: " + str(nbframe) + ".") 
print ("[+] Interval between shots: " + str(interval) + " sec.")


print ("")

launch = input('Ready ? (y/n) : ')
if launch == ('n'):
	print ('\nAbording Capture...')
elif launch == ('y'):
	print ('\nStarting Capture...')
	framecapture(username, password, protocol, camerapath, interval, nbframe)
else:
	print ('\nAbording Capture...')
