from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    returnString = """
    Rango says here is the about page.
    <!DOCTYPE html>
    <html>
    <body>
    <p> Rango says hey there partner!  </p>
    <a href="/rango/about/">About</a>
    </body>
    </html>
    """
    return HttpResponse(returnString)

def about(request):
    returnString = """
    Rango says here is the about page.
    <!DOCTYPE html>
<html>
<body>

<h2>Links</h2>
<p><a href="https://en.wikipedia.org/wiki/Wikipedia:About">Well, no idea</a></p>
<a href="/rango/">Index</a>

</body>
</html>
    """
    # This method can be passed whole HTML files
    return HttpResponse(returnString)