# from django.test import TestCase

from PIL import Image

# test_image = "download.jpg"
# original = Image.open(test_image)
# original.show()

# width, height = original.size   # Get dimensions
# left = width/4
# top = height/4
# right = 3 * width/4
# bottom = 3 * height/4
# cropped_example = original.crop((left, top, right, bottom))

# cropped_example.show()




pic = Image.open("download.jpg")
width, height = pic.size
sirina = 320
visina = 180

aspect_ratio = width / float(height)
if aspect_ratio < 1:						# ratio > 1 --> slika je sira
	aspect_ratio = 1/aspect_ratio
if (width / sirina > height / visina):		# 
	final_height = visina
	final_width = int(visina * aspect_ratio)
elif (width / sirina < height / visina):
	final_width = sirina
	final_height = int(sirina * aspect_ratio)
else:
	final_width = sirina
	final_height = int(sirina * aspect_ratio)

# imaged = pic.resize((final_width, final_height), Image.ANTIALIAS)
pic.thumbnail((32, 18), Image.ANTIALIAS)
# left = top = 0
# right =
# bottom = visina
# cropped = imaged.crop((left, top, right, bottom))
pic.save("thumb.jpg")
# cropped.save("test.jpg")
