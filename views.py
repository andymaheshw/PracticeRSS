from django.http import HttpResponse
from django.template import Template, Context
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.contrib.auth.forms import UserCreationForm
from mysite.forms import ContactForm
import datetime
import feedparser
import goslate
from bs4 import BeautifulSoup
from books.models import Book

from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response

import urllib2
from urllib2 import urlopen

def hello(request):
	return HttpResponse("Hello world")

def main_page(request):
    return render_to_response('index.html')

def logout_page(request):
    """
    Log users out and re-direct them to the main page.
    """
    logout(request)
    return HttpResponseRedirect('/')

def current_datetime(request):
	now = datetime.datetime.now()
#	fp = open('/Users/anirudhmaheshwari/desktop/mysite/templates/mytemplate.html')
#	t = Template(fp.read())
#	fp.close()
#	html = t.render(Context({'current_date': now}))
#	return HttpResponse(html)	
	return render(request, 'mytemplate.html', {'current_date':now})

def new_time(request, offset):
	try: 
		offset = int(offset)
	except ValueError: 
		raise Http404()
	dt = datetime.datetime.now() + datetime.timedelta(hours=offset)
	html = "<html><body>we are now %s hours ahead, it will be %s.</body></html>" %(offset,dt)
	return HttpResponse(html)

def search_form(request):
	return render(request, 'search_form.html')

def search(request):
	if 'q' in request.GET and request.GET['q']:
		q = request.GET['q']
		books = Book.objects.filter(title__icontains=q)
		return render(request, 'search_results.html',
            {'books': books, 'query': q})
	else: 
		return render(request, 'search_form.html', {'error': True})
	return HttpResponse(message)

def next(request):
	return render(request, 'search_form.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
    	return render(request, 'contact.html', {'form':form})
    else:
        form = UserCreationForm()
    return render(request, "register.html", {
        'form': form,
    })

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
             #send_mail(cd['subject'],
             #   cd['message'],
             #   cd.get('email', 'noreply@example.com'),
             #   ['siteowner@example.com'],
            #)
            return HttpResponseRedirect('/contact/thanks/')
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})

def main_page(request):
    return render_to_response('index.html')

def logout_page(request):
    """
    Log users out and re-direct them to the main page.
    """
    logout(request)
    return HttpResponseRedirect('/')


def rss(request): 
	d = feedparser.parse('http://www.lemonde.fr/economie/rss_full.xml')
	gs = goslate.Goslate()
	v = gs.translate(d['entries'][0]['description'], 'en')
	link = d['entries'][0]['link']
	pageFile = urllib2.urlopen(link)
	pageHtml = pageFile.read()
	pageFile.close()
	soup = BeautifulSoup("".join(pageHtml))
	sAll = soup.find_all('div', {'id': 'articleBody'})
	parsed = sAll[0]
	#parsed = 'hello'
	#parsed = temp.encode('ascii', 'replace')
	g2 = goslate.Goslate()
	t = g2.translate('la ministre', 'en')
	html = "<html><body> Old translate %s, Pull article %s. Translated: %s. link %s </body> </html>" %(v, parsed, t, link)
	return HttpResponse(html)
