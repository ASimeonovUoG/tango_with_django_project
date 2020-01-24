from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage matches to {{ boldmessage }} in the template!
    context_dict = {"boldmessage": "Crunchy, creamy, cookie, candy, cupcake!"}
    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.
    return render(request,template_name = "rango/index.html",context=context_dict)


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
    return render(request,template_name="rango/about.html", context= {"yourName": "Alexander Simeonov"})
