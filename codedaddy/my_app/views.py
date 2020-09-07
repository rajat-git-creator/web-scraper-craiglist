from django.shortcuts import render
import requests
from requests.compat import quote_plus
from bs4 import BeautifulSoup
from my_app import models

# Create your views here.

BASE_URL = 'https://kolkata.craigslist.org/search/jjj?query={}'
BASE_IMG_URL = 'https: // images.craigslist.org/_{}_300x300.jpg'


def home(request):
    return render(request, 'base.html')


def new_search(request):
    search = request.POST.get('search')
    models.Search.objects.create(search=search)
    final_url = BASE_URL.format(quote_plus(search))

    response = requests.get(final_url)
    data = response.text

    # using  beautifulSoup to scrape
    soup = BeautifulSoup(data, features='html.parser')
    # print(soup) search just to check wether it is parsing the html and writing in terminal or not
    # now go to craiglist and seee which class contain the whole post lists and  prices and ratings and save it so that we filter and scrape using beautifulsoup
    post_listing = soup.find_all('li', {'class': 'result-row'})

    final_posting = []

    for post in post_listing:

        post_title = post.find(class_='result-title').text
        post_url = post.find('a').get('href')

        final_posting.append((post_title, post_url,))

    frontend = {
        'search': search,
        'final_posting': final_posting,
    }
    return render(request, 'my_app/new_search.html', context=frontend)
