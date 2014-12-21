# Averages all images inside the current directory
# Dan Kolbman 2014

import os, numpy, PIL
from PIL import Image

# Access all PNG files in directory
imlist = [os.path.join(root, name)
             for root, dirs, files in os.walk( os.getcwd(), followlinks=True )
             for name in files
             if name.endswith((".jpeg", ".jpg", ".png"))]

print('Found',len(imlist),'images')


# Assuming all images are the same size, get dimensions of first image
w,h=Image.open(imlist[0]).size
N = len(imlist)

# Create a numpy array of floats to store the average (assume RGB images)
arr=numpy.zeros((h,w,3),numpy.float)

for im in range( N ):
    # Give status update
    if (im % 100 == 0):
      print('Progress:', im,'/',N,'=',numpy.round(im/N*1000.0)/10.0,'%')

    try:
      imarr=numpy.array(Image.open(imlist[im]),dtype=numpy.float)
    except IOError:
      print('Couldn\'t open image',im)
    # Make sure they are the same dimensions
    if imarr.shape == arr.shape:
      arr = arr + imarr/N

# Round values in array and cast as 8-bit integer
arr = numpy.array(numpy.round(arr),dtype=numpy.uint8)

# Generate and save final image
out = Image.fromarray(arr,mode="RGB")
out.save("Average.png")
out.show()
