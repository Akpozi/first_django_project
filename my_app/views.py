from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
from requests.compat import quote_plus
from . import models

BASE_CRAIGSLIST_URL = 'https://helsinki.craigslist.org/search/sss?query={}'
BASE_IMAGE_URL = 'https://images.craigslist.org/{}_300x300.jpg'


# Create your views here.
def home(request):
    return render(request, 'base.html')


def new_search(request):
    search = request.POST.get('search')
    # print(quote_plus(search))
    models.Search.objects.create(search=search)
    final_url = BASE_CRAIGSLIST_URL.format(quote_plus(search))
    print(final_url)

    # Getting the Web-page, and creating a response object
    response = requests.get(final_url)
    # Extracting the source code
    data = response.text
    #print(data)
    # Pass the source code to BeautifulSoup to create a BeautifulSoup object for it
    soup = BeautifulSoup(data, features='html.parser')

    # Extracting all the <a> tags whose class name is 'result-title' into a list
    post_listings = soup.find_all('li', {'class': 'result-row'})

    final_postings = []

    for post in post_listings:
        post_title = post.find(class_='result-title').text
        post_url = post.find('a').get('href')

        # Check if result has Price
        if post.find(class_='result-price'):
            post_price = post.find(class_='result-price').text
        else:
            post_price = 'Not Available'

        if post.find(class_='result-image').get('data-ids'):
            post_image_id = post.find(class_='result-image').get('data-ids').split(',')[0].split(':')[1]
            post_image_url = BASE_IMAGE_URL.format(post_image_id)
            print(post_image_url)
        else:
            post_image_url = 'https://images.theconversation.com/files/317421/original/file-20200226-24651-1or3uxq.jpg'

        final_postings.append((post_title, post_url, post_price, post_image_url))

    # Stuff for front end
    design_frontend = {
        'search': search,
        'final_postings': final_postings,
    }

    return render(request, 'my_app/new_search.html', design_frontend)