from django.shortcuts import render
from django.http import HttpResponse

# Import Category model
from rango.models import Category

# Import Page model
from rango.models import Page

# Import Forms
from rango.forms import CategoryForm, PageForm
from django.shortcuts import redirect

from django.urls import reverse

def index(request):
    # Initialise context_dictionary
    context_dict = {}
    # Query model for Categories
    category_list = Category.objects.order_by("-likes")[:5]
    context_dict["categories"] = category_list
    # print(category_list)
    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage matches to {{ boldmessage }} in the template!
    context_dict["boldmessage"] = "Crunchy, creamy, cookie, candy, cupcake!"
    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.
    context_dict["pages"] = Page.objects.order_by("-views")[:5]
    return render(request, template_name="rango/index.html", context=context_dict)


def show_category(request, category_name_slug):
    # Create a context dictionary
    context_dict = {}
    try:
        # Try find a category given the current name slug
        # Get raises an exception if not found
        category = Category.objects.get(slug=category_name_slug)

        # Retrieve all category pages
        pages = Page.objects.filter(category=category)

        # Add pages list to context dict
        context_dict["pages"] = pages

        # Add category to context dict to verify it exits
        context_dict["category"] = category
    except Category.DoesNotExist:
        # We didnt find a category with the given slug
        context_dict["pages"] = None
        context_dict["category"] = None

    return render(request, context=context_dict, template_name="rango/category.html")


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
    return render(
        request,
        template_name="rango/about.html",
        context={"yourName": "Alexander Simeonov"},
    )


def add_category(request):
    form = CategoryForm()

    # An HTTP POST check
    if request.method == "POST":
        # Retrieve form
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            # Saves category into DB
            return redirect("/rango/")
        else:
            # The supplied form contained errors -
            print(form.errors)
    # Will handle the bad form, new form, or no form supplied cases.
    # Render the form with error messages (if any).
    return render(request, "rango/add_category.html", {"form": form})

def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug = category_name_slug)
    except Category.DoesNotExist:
        category = None
    if category is None:
        return redirect('/rango/')
    form = PageForm()
    if request.method == "POST":
        # retrieve form
        form = PageForm(request.POST)
        if form.is_valid:
            page = form.save(commit=False)
            page.category = category
            page.views = 0
            page.save()
            # Saves category into DB
            return redirect(reverse('rango:show_category',kwargs={"category_name_slug":category_name_slug}))
        else:
            # The supplied form contained errors -
            print(form.errors)
    # Will handle the bad form, new form, or no form supplied cases.
    # Render the form with error messages (if any).
    context_dict = {"form":form,"category":category}
    return render(request, "rango/add_page.html", context_dict)