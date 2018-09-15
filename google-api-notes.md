So it wasn't until September 2018 that I discovered an apparently sane and supported API for google photos:

    https://developers.google.com/photos/library/guides/overview

I'm itching to get started!  Clearly I need to create some credentials ... the docs suggest that I want OAuth2 client credentials ...

    https://console.developers.google.com/apis/api/photoslibrary.googleapis.com/overview?project=pure-zoo-153401

(I suspect "project-pure-zoo-153401" is the name of my existing-but-empty "upload to google photos" app)

To create OAuth2 credentials, however, it seems I must supply the URL of my web service, and it's gotta be https, which I've never gotten around to enabling, since it's a pain in the ass.

And I _have_ to have a web service, as opposed to just a command-line tool, since the tool needs temporary credentials, and the only way to get those, it seems, is to have some web browser get redirected ...

... or maybe not; I fooled it into giving me credentials by claiming that I was going to be using a command-line tool _with a UI_.

https://console.developers.google.com/apis/credentials?project=pure-zoo-153401
