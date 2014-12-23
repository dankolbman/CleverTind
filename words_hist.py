# Create a histogram for word data
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
 
  words = dict()

  # Read word data
  with open(path) as f:
    for line in f:
      s = line.split()
      if len(s) == 3:
        words[s[0]] = float(s[2])

  wanted = [ 'coffee', 'tea', 'beer', 'wine' ]
  wanted = [ 'instagram', 'insta', 'ig', 'twitter', 'tweet', 'facebook', 'fb', 'snapchat', 'snap', 'sc' ]
  wanted = [ 'ny', 'nyc', 'nj']
  wanted = [ 'reading', 'books', 'watching', 'tv', 'netflix' ]
  wanted = [ 'baseball', 'football', 'basketball', 'hockey' ]
  wanted = [ 'math', 'physics', 'premed', 'nursing', 'science' ]
  wanted = [ 'dog', 'dogs', 'cat', 'cats' ]
  wanted = [ '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24' ]
  wanted = [ 'tall', 'short' ]
  wanted = [ 'sad', 'happy' ]
  wanted = [ 'whiskey', 'vodka', 'rum', 'gin' ]
  wanted = [ 'music', 'dancing', 'party' ]
  pct = []
  
  for w in wanted:
    pct.append( words[w] )

  xt = np.arange(len(wanted))

  fig, ax = plt.subplots()
  rects1 = ax.bar(xt, pct, 1, color='b', alpha=0.7)

  ax.set_xticks(xt+0.5)
  ax.set_xticklabels( wanted ) 

  plt.ylabel('Percent of Users')

  plt.tight_layout()

  plt.show()
        
 
################################################################################

if(len(sys.argv) < 2):
  print('Usage: python words_hist.py word_data.dat')
elif( len(sys.argv) == 2 ):
  main( sys.argv[1] )

