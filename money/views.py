from django.shortcuts import render
from .models import Article, Feed
from .forms import FeedForm 
from django.shortcuts import redirect

import feedparser
import datetime
# Create your views here.


def articles_list(request):
	NYR_articles = []
	NYG_articles = []
	NYK_articles = []
	articles = Article.objects.all().order_by('-publication_date')
	for art in articles:
		if art.feed.title == 'NYR':
			NYR_articles.append(art)
		elif art.feed.title == 'NYG':
			NYG_articles.append(art)
		elif art.feed.title == 'NYK':
			NYK_articles.append(art)
	return render(request, 'news/articles_list.html', {'NYR_articles': NYR_articles, 'NYG_articles': NYG_articles, 'NYK_articles': NYK_articles})

def feeds_list(request):
	feeds = Feed.objects.all()
	return render(request, 'news/feeds_list.html', {'feeds': feeds})

def new_feed(request):
	if request.method == "POST":
		form = FeedForm(request.POST)
		if form.is_valid():
			feed = form.save(commit=False)

			feedData = feedparser.parse(feed.url)

			#set fields
			feed.title = feedData.feed.title
			feed.save()

			for entry in feedData.entries:
				article = Article()
				article.title = entry.title
				article.url = entry.link
				if hasattr(entry, 'description'):
					article.description = entry.description
				else:
					article.description = ""
				if hasattr(entry, 'summary'):
					article.summary = entry.summary
				else:
					article.summary = ""
				d=datetime.datetime(*(entry.published_parsed[0:6]))
				dateString = d.strftime('%Y-%m-%d %H:%M:%S')
				
				article.publication_date = dateString
				article.feed = feed
				article.save()

			return redirect('news.views.feeds_list')
	else:
		form = FeedForm()
	return render(request, 'news/new_feed.html', {'form': form})
