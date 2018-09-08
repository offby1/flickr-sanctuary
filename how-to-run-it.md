So here's this thing I wrote called flickr.py.  I know it works, since
I've used it, and my flickr photos are indeed safely copied to s3.

But as an exercise, how would one run this thing?

I'm going to convert it to use python3 and pipenv, since those are The Future™.

Run it like this

    pipenv run python flickr.py

It's more or less safe to do so, since it won't upload anything if it sees that there's already something in s3 with the same name.
