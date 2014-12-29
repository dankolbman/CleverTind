# Create a histogram for age data
# Dan Kolbman 2014
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 28}

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
  rects1 = ax.bar(ages, pct, 1.0, color='#1FB3F2', alpha=1.0, lw=0)
  #rects1 = ax.bar(ages, pct, 1, color='r', alpha=0.5, hatch='///')
  fig.set_size_inches(7,6)

  # Draw mean line
  plt.axvline( avg, lw=7, ls='--', color='k' )
  ax.text( avg*1.02, 17, 'Mean: '+str(round(avg*10.0)/10.0)+'yr' )

  ax.set_xticks( [ 20.5, 25.5, 30.5, 35.5, 40 ] )
  ax.set_xticklabels( [ '20', '25', '30', '35', '40'] )

  plt.xlim(18, 40)
  plt.xlabel('Age (Years)')
  plt.ylabel('Percent of Users')

  plt.tight_layout()

  
  plt.savefig('ages.png', transparent=True, dpi=100)
  plt.show()
        
 
################################################################################

if(len(sys.argv) < 2):
  print('Usage: python prof_hist.py age_data.dat')
elif( len(sys.argv) == 2 ):
  main( sys.argv[1] )

