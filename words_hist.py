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

  wanted = [ 'instagram', 'insta', 'ig', 'twitter', 'tweet', 'facebook', 'fb', 'snapchat', 'snap', 'sc' ]
  wanted = [ 'ny', 'nyc', 'nj']
  wanted = [ 'reading', 'books', 'watching', 'tv', 'netflix' ]
  wanted = [ 'math', 'physics', 'premed', 'nursing', 'science' ]
  wanted = [ 'dog', 'dogs', 'cat', 'cats' ]
  wanted = [ '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24' ]
  wanted = [ 'tall', 'short' ]
  wanted = [ 'sad', 'happy' ]
  wanted = [ 'whiskey', 'vodka', 'rum', 'gin' ]
  wanted = [ 'music', 'dancing', 'party' ]
  wanted = [ 'coffee', 'tea', 'beer', 'wine' ]
  wanted = [ '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24' ]
  wanted = [ 'hockey', 'soccer', 'football', 'basketball']
  pct = []
  
  for w in wanted:
    pct.append( words[w] )

  xt = np.arange(len(wanted))+0.1

  fig, ax = plt.subplots()
  rects1 = ax.bar(xt, pct, 0.8, color='#1FB3F2', alpha=1.0, lw=0)
  #rects1 = ax.bar(xt, pct, 1, color='none', alpha=0.2, hatch='//')
  #rects1 = ax.bar( xt, pct, 1, color='none', lw=5)
  fig.set_size_inches(7,6)

  ax.set_xticks(xt+0.4)
  ax.set_xticklabels( wanted, fontsize=16) 
  #ax.set_xticklabels( wanted, rotation='vertical', fontsize=16) 

  plt.ylabel('Percent of Users')

  plt.tight_layout()

  plt.savefig('sports.png', transparent=True, dpi=100)

  plt.show()
        
 
################################################################################

if(len(sys.argv) < 2):
  print('Usage: python words_hist.py word_data.dat')
elif( len(sys.argv) == 2 ):
  main( sys.argv[1] )

