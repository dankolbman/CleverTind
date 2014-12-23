# Create a histogram for age data
# Dan Kolbman 2014
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 32}

matplotlib.rc('font', **font)

def main( path ):
 
  ages = []
  pct = []
  # Read age data
  with open(path) as f:
    for line in f:
      s = line.split()
      if len(s) == 3:
        ages.append( int(s[0]) )
        pct.append( float(s[2]) )

  avg = 0.0
  for i in range(len(ages)):
    avg += ages[i]*pct[i]/100.0

  print('Mean age:', avg)
  
  fig, ax = plt.subplots()
  rects1 = ax.bar(ages, pct, 1, color='b', alpha=0.7)

  # Draw mean line
  plt.axvline( avg, lw=7, ls='--', color='k' )
  ax.text( avg*1.02, 17, 'Mean: '+str(round(avg*10.0)/10.0)+'yr' )

  plt.xlim(18, 40)
  plt.xlabel('Age (Years)')
  plt.ylabel('Percent of Users')

  plt.tight_layout()

  plt.show()
        
 
################################################################################

if(len(sys.argv) < 2):
  print('Usage: python prof_hist.py age_data.dat')
elif( len(sys.argv) == 2 ):
  main( sys.argv[1] )

