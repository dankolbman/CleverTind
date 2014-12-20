CleverTind
==========
Robot dating for the year 21XX
----------

CleverTind interacts with the Tinder api to like and download users profiles.
It starts and holds conversations with matches via cleverbot.

Composite profile pictures can be created from downloaded user profiles using
the included `average.py` script.

The composite creator uses openCV and Haar Cascades to recognize faces. The default
training data is included here, but you can get different cascade sets
 [here](https://github.com/Itseez/opencv/tree/master/data/haarcascades)
or even [train your own](http://docs.opencv.org/doc/user_guide/ug_traincascade.html).

Install
-------
The bot requires [pyro](https://github.com/nneal/tinder_pyro) and
[cleverbot](https://github.com/benmanns/cleverbot)
The image averager requires `python 2.7`, `numpy`, and `openCV` (for facial
detection)
The quick image averager (no facial detection) requires `PIL`
