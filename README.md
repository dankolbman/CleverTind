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

The `sample_data` directory contains some analyized data from more than 60,000
profiles which I have collected. You can generate your own analysis by running 
the bot and running through the profiles with `profile_parse.py`.

The `figures` directory contains scripts for creating visualizations of the 
parsed data.

Using
-------
The bot requires [pyro](https://github.com/nneal/tinder_pyro),
[cleverbot](https://github.com/benmanns/cleverbot),
and [httparty](https://github.com/jnunemaker/httparty).
The image averager requires `python 2.7`, `numpy`, and `openCV` (for facial
detection)
The quick image averager (no facial detection) requires `PIL`

Generating a site
---------
`site_gen.rb` can be used to generate a bunch of markdown files for messages 
history. It will place the files inside the `site` directory where there are
some files for [Pelican](https://github.com/getpelican/pelican) to generate a 
site. 
You can generate the pages and then the site as follows:

    ruby site_gen.rb
    cd site
    make html
    make serve

This will put a server on `localhost:8000` where you can view the site. See the
[Pelican Docs](http://docs.getpelican.com/en/3.5.0/) for more info on using
Pelican.
