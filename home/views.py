from django.shortcuts import render
from operator import attrgetter
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from movies.views import get_movie_queryset
from movies.models import MoviePost

MOVIE_POSTS_PER_PAGE = 10

def home_screen_view(request):
	
	context = {}

	query = ""
	query = request.GET.get('q', '')
	context['query'] = str(query)
	print("home_screen_view: " + str(query))

	movie_posts = sorted(get_movie_queryset(query), key=attrgetter('date_updated'), reverse=True)
	
	# Pagination
	page = request.GET.get('page', 1)
	movie_posts_paginator = Paginator(movie_posts, MOVIE_POSTS_PER_PAGE)

	try:
		movie_posts = movie_posts_paginator.page(page)
	except PageNotAnInteger:
		movie_posts = movie_posts_paginator.page(MOVIE_POSTS_PER_PAGE)
	except EmptyPage:
		movie_posts = movie_posts_paginator.page(movie_posts_paginator.num_pages)

	context['movie_posts'] = movie_posts

	return render(request, "home/home.html", context)
