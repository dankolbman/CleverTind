# Create a histogram for word count data
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
 
  wc = []
  pct = []
  # Read wc data
  with open(path) as f:
    for line in f:
      s = line.split()
      if len(s) == 3:
        wc.append( int(s[0]) )
        pct.append( float(s[2]) )

  avg = 0.0
  for i in range(len(wc)):
    avg += wc[i]*pct[i]/100.0

  print('Mean word count:', avg)
  
  fig, ax = plt.subplots()
  plt.ylabel('Percent of Users')

  rects1 = ax.bar(wc, pct, 1.0, color='#1FB3F2', alpha=1.0, lw=0)
  #rects1 = ax2.bar(wc, pct, 1.0, color='#FF9F21', alpha=1.0, lw=0)

  # Draw mean line
  plt.axvline( avg, lw=7, ls='--', color='k' )
  ax.text( avg*1.08, 5, 'Mean: '+str(round(avg*10.0)/10.0)+' words' )

  #ax.set_xticks( [ 20.5, 25.5, 30.5, 35.5, 40 ] )
  #ax.set_xticklabels( [ '20', '25', '30', '35', '40'] )

  ax.set_yscale('log')

  plt.xlim(0, 100)
  plt.ylim(0,50)

  #plt.xlabel('Words')

  fig.set_size_inches(7,6)

  plt.tight_layout()

  
  plt.savefig('wc.png', transparent=True, dpi=100)
  plt.show()
        
 
################################################################################

if(len(sys.argv) < 2):
  print('Usage: python wc_hist.py word_count.dat')
elif( len(sys.argv) == 2 ):
  main( sys.argv[1] )

