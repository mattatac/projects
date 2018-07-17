import os, sys
from PIL import Image
import string
import time, datetime
import threading


# class myThread(threading.Thread):
	# def __init__(self, threadID, name, counter):
		# threading.Thread.__init__(self)
		# self.threadID = threadID
		# self.name = name
		# self.counter = counter
	
	# def run(self, func):
		# print('Running ' + func + ' on ' + self.name + '.')
		# func(
		
		

def convert_thumb(pic, size):
	'''
	Converts 'pic' to a thumbnail of the specified 'size'
	Returns the converted image
	'''
	return pic.thumbnail(size, Image.ANTIALIAS)

def create_thumb_dir(path, newpath):
	'''
	Creates a new folder called 'thumb' in the
	current directory for thumbnails to be saved
	'''
	if not os.path.exists(newpath):
		os.makedirs(newpath)

def save_thumb(pic, newpath, outfile, extension):
	'''
	Saves new thumbnail in the thumb folder
	'''
	return pic.save(newpath + outfile, extension)


print('\n\n=======  Image Thumbnail Creator  =======\n')

def main():
	yes = False
	while not yes:
		fType = str.lower(input('What type of file are you wanting to convert? Enter a period and the file type (e.g. ".jpg")\n'))
		path = input('\nEnter the path of the folder where your images are stored:\n')
		filelist = os.listdir(path)
		print()
		for infile in filelist:
			if infile[-4:] == fType:
				print(infile)
		correct = str.lower(input('\nThe above files will be copied and resized. Is this correct? (Y or N)\n'))
		if correct == 'y':
			yes = True

	valid = False
	while not valid:
		try:
			x = int(input('\nEnter the width you want your thumbnails to be saved with:\n'))
			if x > 0:
				valid = True
				y = x
				size = x, y
			else:
				print('Please enter a valid positive number.\n')
		except ValueError:
			print('Please enter a number.\n')

	newpath = path + '/thumbs/'

	time = datetime.datetime.now()

	for infile in filelist:
		outfile = os.path.splitext(infile)[0] + '_thumb.jpg'
		if infile != outfile and infile[-4:] == fType:
			try:
				pic = Image.open(path + '/' + infile)
				#convert_thumb(pic, size)
				thread1 = threading.Thread(target=convert_thumb(pic,size)).start()
				create_thumb_dir(path, newpath)
				#save_thumb(pic, newpath, outfile, 'JPEG')
				thread2 = threading.Thread(target=save_thumb(pic,newpath,outfile,'JPEG')).start()
				success = True
			except IOError:
				print("\n******Cannot create thumbnail for '%s'******" % infile)

	time = datetime.datetime.now() - time

	if success:
		print('\nAll files successfully converted!')
		print('Thumbnails stored in ' + newpath)

	print('\nYour request took ' + str(time) + ' seconds to process.\n')
	#input('Hit the return key to exit.')

	
main()