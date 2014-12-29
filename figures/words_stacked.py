# Create a histogram for word data
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
 
  words = dict()

  # Read word data
  with open(path) as f:
    for line in f:
      s = line.split()
      if len(s) == 3:
        words[s[0]] = float(s[2])

  w1 = [ 'dog', 'cat' ]
  w2 = [ 'dogs', 'cats' ]
  pct1 = []
  pct2 = []
  
  for w in range(len(w1)):
    pct1.append( words[w1[w]])
  for w in range(len(w2)):
    pct2.append( words[w2[w]])

  xt = np.arange(len(w1))+0.1

  fig, ax = plt.subplots()
  rects1 = ax.bar(xt, pct1, 0.8, color='#1FB3F2', alpha=1.0, lw=0)
  rects1 = ax.bar(xt, pct2, 0.8, color='#FF9F21', alpha=1.0, lw=0, bottom=pct1)
  fig.set_size_inches(7,6)

  for w in range(len(w1)):
    plt.text(w+0.5, pct1[w]/2.0-0.075 , w1[w]+'\n('+str(pct1[w])+'%)', ha='center')
  for w in range(len(w2)):
    plt.text(w+0.5, pct1[w]+pct2[w]/2.0-0.075 , w2[w]+'\n('+str(pct2[w])+'%)', ha='center')

  ax.set_xticks(xt+0.4)
  ax.set_xticklabels( [] )
  #ax.set_xticklabels( wanted, fontsize=16) 
  #ax.set_xticklabels( wanted, rotation='vertical', fontsize=16) 

  plt.ylabel('Percent of Users')

  plt.tight_layout()

  plt.savefig('pets.png', transparent=True, dpi=100)

  plt.show()
        
 
################################################################################

if(len(sys.argv) < 2):
  print('Usage: python words_hist.py word_data.dat')
elif( len(sys.argv) == 2 ):
  main( sys.argv[1] )

