import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tango_with_django_project.settings")

import django
import random

django.setup()
from rango.models import Category, Page


def populate():

    python_pages = [
        {
            "title": "Official Python Tutorial",
            "url": "http://docs.python.org/3/tutorial/",
        },
        {
            "title": "How to Think like a Computer Scientist",
            "url": "http://www.greenteapress.com/thinkpython/",
        },
        {
            "title": "Learn Python in 10 Minutes",
            "url": "http://www.korokithakis.net/tutorials/python/",
        },
    ]

    django_pages = [
        {
            "title": "Official Django Tutorial",
            "url": "https://docs.djangoproject.com/en/2.1/intro/tutorial01/",
        },
        {"title": "Django Rocks", "url": "http://www.djangorocks.com/"},
        {"title": "How to Tango with Django", "url": "http://www.tangowithdjango.com/"},
    ]

    other_pages = [
        {"title": "Bottle", "url": "http://bottlepy.org/docs/dev/",},
        {"title": "Flask", "url": "http://flask.pocoo.org"},
    ]

    cats = {
        "Python": {"pages": python_pages},
        "Django": {"pages": django_pages},
        "Other Frameworks": {"pages": other_pages},
    }

    for cat, cat_data in cats.items():
        c = add_cat(cat)
        for p in cat_data['pages']:
            add_page(c, p["title"], p["url"], random.randint(1,1000))

    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print(f" - {c} : {p}")


def add_page(cat, title, url, views=0):
    page = Page.objects.get_or_create(category=cat, title=title)[0]
    page.url = url
    # Put a random number of views for each page
    page.views = views
    page.save()
    return page


def add_cat(title):
    cat = Category.objects.get_or_create(name=title)[0]
    if title=="Python":
        cat.views = 128
        cat.likes = 64
    elif title=="Django":
        cat.views = 64
        cat.likes = 32
    else:
        cat.views = 32
        cat.likes = 16  
    cat.save()
    return cat


# Start exec
if __name__ == "__main__":
    print("Starting Rango DB population")
    populate()
