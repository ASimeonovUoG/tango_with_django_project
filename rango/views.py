from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from datetime import datetime

# Import Category model
from rango.models import Category

# Import Page model
from rango.models import Page

# Import Forms
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from django.shortcuts import redirect

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
    # extract response object to pass to cookie handler

    # Call handler to handle cookies and edit response accordingly
    visitor_cookie_handler(request)
    
    response = render(request, template_name="rango/index.html", context=context_dict)
    return response


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

    # Call Cookies handler that sets the visits cookie
    visitor_cookie_handler(request)
    # Retrieve visits cookie
    visits = request.session['visits']
    # This method can be passed whole HTML files
    return render(
        request,
        template_name="rango/about.html",
        context={"yourName": "Alexander Simeonov", "visits": visits},
    )

@login_required
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

@login_required
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
        if form.is_valid():
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

def register(request):
    # A boolean value saying if registration is successful
    registered = False

    # If a request is POST we need to handle form processing 
    if request.method == "POST":
        # Attempt to grab information from the raw form user form
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        # if the two forms are valid
        if user_form.is_valid() and profile_form.is_valid():
            # save the user's form data into the database
            user = user_form.save()

            # Hash the password with the set_password method and update object
            user.set_password(user.password)
            user.save()

            # Sort out UserProfile instance 
            profile = profile_form.save(commit=False)
            profile.user = user

            # If user provided a profile pic, retrieve it and put it in UserForm and update it
            if "picture" in request.FILES:
                profile.picture = request.FILES['picture']
            profile.save()

            # Update success flag to indicate registration is complete
            registered = True
        else:
            # Invalid form or forms - mistakes ?
            print(user_form.errors, profile_form.errors)

    else:
        # Request is of type GET - render form using both models
        user_form = UserForm()
        profile_form = UserProfileForm()
    
    context_dictionary = {"user_form" : user_form, "profile_form" : profile_form , "registered" : registered}
    # Render the template depending on the context.
    return render(request,'rango/register.html', context_dictionary)

def user_login(request):

    if request.method == "POST":

        username = request.POST.get('username')
        password = request.POST.get('password')

        # Use Django machinery to authenticate user, if success a user is provided
        user = authenticate(username=username, password=password)

        if user:
            # Is the account active ? Could be disabled
            if user.is_active:
                # If valid and active we can log them in, send to homepage
                login(request, user)
                return redirect(reverse('rango:index'))
            else:
                # User account is correct but not active
                return HttpResponse("Your account is disabled.")
        else:
            # Bad login details provided
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
    else:
        # If request is not POST then render login template
        return render(request, 'rango/login.html')

@login_required
def restricted(request):
    return render(request, "rango/restricted.html")

# Use the login_required() decorator to ensure only those logged in can
# access the view.
@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)
    # Take the user back to the homepage.
    return redirect(reverse('rango:index'))


# Helper method for requesting session cookies
def get_server_side_cookie(request, cookie, default_val = None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val

def visitor_cookie_handler(request):
    # Get the number of visits to the site.
    # We use the COOKIES.get() function to obtain the visits cookie.
    # If the cookie exists, the value returned is casted to an integer.
    # If the cookie doesn't exist, then the default value of 1 is used.
    visits = int(get_server_side_cookie(request,'visits','1'))

    last_visit_cookie = get_server_side_cookie(request,'last_visit', str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7],'%Y-%m-%d %H:%M:%S')

    # If it has been more than a day since last visit - update counter
    if (datetime.now() - last_visit_time).days > 0:
        visits = visits + 1
        # Update the last visit cookie now that we have updated count
        request.session["last_visit"] = str(datetime.now())
    else:
        # Set the last visit cookie
        request.session['last_visit'] = last_visit_cookie
    
    # Update/set the visits of the cookie
    request.session['visits'] = visits