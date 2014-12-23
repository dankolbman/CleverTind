import os
import sys
import numpy as np
import time
import cv2

# Deterimens if a photo is a face and returns a scaled image if it is. Returns
# False if it is not a face.
# Params:
#   path - path to the image
#   haar_map - path to the haar_cascade training data
#   pw - the picture width
#   ph - the picture height
def is_face( path, haar_map, pw, ph ):
  good_face = True
  face_cascade = cv2.CascadeClassifier( haar_map )
  #eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
  #smile_cascade = cv2.CascadeClassifier('haarcascade_smile.xml')

  img = cv2.imread( path )
  try:
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  except cv2.error:
    # Some images have problems being converted to grayscale
    print 'Couldn\'t convert to grayscale'
    return False

  faces = face_cascade.detectMultiScale(
    gray,
    scaleFactor=1.2,
    minNeighbors=5,
    minSize=(30, 30),
    flags = cv2.cv.CV_HAAR_SCALE_IMAGE
  )

  # Draw rectangles around detected features
  #for (x,y,w,h) in faces:
    # Draws a square around the face
    #cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
    #roi_gray = gray[y:y+h, x:x+w]
    #roi_color = img[y:y+h, x:x+w]
     # eyes = eye_cascade.detectMultiScale(roi_gray, 1.1, 5)
     # for (ex,ey,ew,eh) in eyes:
     #     cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,0,255),2)
     # smiles = smile_cascade.detectMultiScale(roi_gray, 1.1, 8)
     # for (sx,sy,sw,sh) in smiles:
     #     cv2.rectangle(roi_color,(sx,sy),(sx+sw,sy+sh),(0,255,0),2)

  # Check that there is only one face and that is large enough
  if( len(faces) != 1 ):
    # not a single face
    good_face = False
  else:
    # Dimensions of the face
    x,y,w,h = faces[0]
    if( w < 100 or h < 100 ):
      # too small
      good_face = False

  # If those conditions were met
  if( good_face ):
    img = center_face(img, x, y, w, h, pw, ph)
    return cv2.resize(img, ( pw, ph ) )
  else:
    return good_face

# Center a face in the image and return the new image
# Params:
#   img - the face image
#   x,y - the coords of the bottom left corner of the face
#   w,h - the dimensions of the face
#   pw,ph - the image dimensions
def center_face(img, x, y, w, h, pw, ph):
  # Margins
  m1 = 0.2*pw
  m2 = 0.8*pw
  pts1 = np.float32([[x,y],[x+w,y],[x,y+h],[x+w,y+h]])
  pts2 = np.float32([[m1,m1],[m2,m1],[m1,m2],[m2,m2]])
  M = cv2.getPerspectiveTransform(pts1,pts2)
  dst = cv2.warpPerspective(img,M,(pw,ph))
  return dst

# Shows a face and waits for user to press a key. exit the program if the
# escape key is pressed
# Params
#   img - the image to display
def show_face( img ):
  cv2.destroyAllWindows()
  cv2.imshow('img',img)
  k = cv2.waitKey(50)
  if k == 27 and accepted > 0:
    exit()

################################################################################

def main( prof_path, output_path='output', haar_map='haarcascade_frontalface_default.xml' ):

  # Access all JPG files in directory
  imlist = [os.path.join(root, name)
             for root, dirs, files in os.walk( os.path.join(os.getcwd(), prof_path) )
             for name in files
             if name.endswith((".jpeg", ".jpg"))]

  # Make output directory if it doesn't exist
  if( not os.path.isdir(output_path) ):
    os.makedirs( output_path )

  # Assuming all images are the same size, get dimensions of first image
  img = cv2.imread(imlist[0],0)
  h, w = img.shape[:2]
  # Book keeping
  N = len(imlist)
  accepted = 0.0
  rate = 0.0
  avg_face = None

  print 'Found', N, 'profiles'

  for im in range( N ):
    try:
      # Face match
      face = is_face(imlist[im], haar_map, w, h)
      # It returned a scaled face
      if( type(face) != bool ):
        if( avg_face == None ):
          avg_face = face
        else:
          # Do running average
          alpha = 1.0/(float(accepted) + 1.0)
          #alpha = np.ceil(alpha*100.0)/100.0
          avg_face = cv2.addWeighted(face, alpha, avg_face, 1.0-alpha, 0.0, avg_face)
          #show_face(avg_face)
          
        accepted += 1.0
    except IOError:
      print 'Couldn\'t open image',im

    # Give Status report
    if ( accepted % 100 == 1 ):
      print 'Progress:', im,'/',N,'=',100.0*np.round(float(im)/float(N)*1000.0)/1000.0,'%'
      rate = accepted/float(im+1)
      print 'Accepted:', accepted,'/',N,'=',np.round(rate*100000.0)/1000.0,'%'
      if( avg_face != None ):
        #show_face( avg_face )
        print 'Saving Current Average'
        img_out = os.path.join(output_path, 'Average_Face_'+str(int(accepted))+'.png')
        cv2.imwrite( img_out, avg_face )
      #avg_out = None
  cv2.destroyAllWindows()

if(len(sys.argv) < 2):
  print 'Usage: python average.py profiles_dir/ <output/> <haar_cascade_default.xml>'
elif( len(sys.argv) == 2 ):
  main( sys.argv[1] )
elif( len(sys.argv) == 3 ):
  main( sys.argv[1], sys.argv[2] )
elif( len(sys.argv) == 4 ):
  main( sys.argv[1], sys.argv[2], sys.argv[3] )
