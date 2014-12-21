# Attempt to find faces and draw rectangles around them using openCV
# Dan Kolbman
import sys, cv2

def detect( path ):
  img = cv2.imread( path )
  face_cascade = cv2.CascadeClassifier( 'haarcascade_frontalface_default.xml' )
  eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

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

  for (x,y,w,h) in faces:
    # Draws a square around the face
    cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
    roi_gray = gray[y:y+h, x:x+w]
    roi_color = img[y:y+h, x:x+w]
    eyes = eye_cascade.detectMultiScale(roi_gray, 1.1, 5)
    for (ex,ey,ew,eh) in eyes:
        cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,0,255),2)

  print 'Found', len(faces),'faces'

  # Display the image
  cv2.imshow('img',img)
  # Wait for user to press a key
  k = cv2.waitKey()
  # Close everything
  cv2.destroyAllWindows()


################################################################################

if(len(sys.argv) < 2):
  print 'Usage: python face_detect.py <image.jpg>'
else:
  detect( sys.argv[1] )
