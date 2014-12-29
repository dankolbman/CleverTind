# Create a histogram for name data
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
  N = 15
  h = 0.75
  names = []
  pct = []
  # Read name data
  with open(path) as f:
    for line in f:
      s = line.split()
      if len(s) == 3:
        names.append( s[0] )
        pct.append( float(s[2]) )

  fig, ax = plt.subplots()
  yt = np.arange(N)
  yt = yt[::-1]

  fig.set_size_inches(7,9)
  rects1 = ax.barh( yt, pct[0:N], h, color='#1FB3F2', alpha=1.0, lw=0)
  #rects1 = ax.barh( yt, pct[0:N], h, color='r', alpha=0.3, hatch='///')
  #rects1 = ax.barh( yt, pct[0:N], h, color='none', lw=5)


  ax.set_yticks(yt+0.3)
  ax.set_yticklabels( yt[::-1]+1 ) 
  #ax.set_yticklabels( names[0:N] ) 
  plt.ylim(0, N)
  ax.set_xticks( [0.0, 0.5, 1.0, 1.5] )
  ax.set_xticklabels( ['0%', '0.5%', '1%', '1.5%'] )

  for i in range(N):
    plt.text(0.04, N-i-0.85, names[i], fontsize=22)
    plt.text(pct[i]+0.03, N-i-0.85, str(round(pct[i]*100.0)/100.0)+'%', fontsize=22)

  plt.xlim(0.0, 1.8)
  plt.ylim(-0.25, N)

  plt.ylabel('Rank')
  plt.xlabel('Percent of Users')
  plt.tight_layout()

  
  plt.savefig('names.png', dpi=100, transparent=True)

  plt.show()
        
 
################################################################################

if(len(sys.argv) < 2):
  print('Usage: python name_hist.py name_data.dat')
elif( len(sys.argv) == 2 ):
  main( sys.argv[1] )

