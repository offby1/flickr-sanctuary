So here's this thing I wrote called flickr.py.

Run it like this

    pipenv run python flickr.py

It's more or less safe to do so, since it won't upload anything if it sees that there's already something in s3 with the same name.

Note: it goes 5 or 10 times faster if you run it on an EC2 instance,
as compared to running it in my house via my cheap-ass DSL line.
