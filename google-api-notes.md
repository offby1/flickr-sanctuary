So it wasn't until September 2018 that I discovered an apparently sane and supported API for google photos:

    https://developers.google.com/photos/library/guides/overview

I'm itching to get started!  Clearly I need to create some credentials ... the docs suggest that I want OAuth2 client credentials ...

    https://console.developers.google.com/apis/api/photoslibrary.googleapis.com/overview?project=pure-zoo-153401

(I suspect "project-pure-zoo-153401" is the name of my existing-but-empty "upload to google photos" app)

To create OAuth2 credentials, however, it seems I must supply the URL of my web service, and it's gotta be https, which I've never gotten around to enabling, since it's a pain in the ass.

And I _have_ to have a web service, as opposed to just a command-line tool, since the tool needs temporary credentials, and the only way to get those, it seems, is to have some web browser get redirected ...

... or maybe not; I fooled it into giving me credentials by claiming that I was going to be using a command-line tool _with a UI_.

The `client_id.json` file, which I suspect oughtn't be checked in to
revision control, can be downloaded from
here

    https://console.developers.google.com/apis/credentials?project=pure-zoo-153401

https://developers.google.com/identity/protocols/OAuth2ForDevices appears to be relevant
otoh that page says

> Alternatives
>
> If you are writing an app for a platform like Android, iOS, macOS, Linux, or Windows (including the Universal Windows Platform), that has access to the browser and full input capabilities, use the [OAuth 2.0 flow for mobile and desktop applications](https://developers.google.com/identity/protocols/OAuth2InstalledApp). (You should use that flow even if your app is a command-line tool without a graphical interface.)
>

Gaaah, https://developers.google.com/identity/protocols/OAuth2InstalledApp says
> Note that in most cases where the platform does not have a usable browser, the OAuth 2.0 for TVs & Devices flow is recommended.

Apparently in any case I need some "scopes", which are short strings.  But which? https://developers.google.com/identity/protocols/googlescopes is supposedly the authoritative list, but there are one bazillion entries on that page, most of which seem irrelevant.  The only ones that have the word "photo" in them are

- https://www.googleapis.com/auth/drive.photos.readonly
- https://www.googleapis.com/auth/plus.media.upload

So I guess I want those?
