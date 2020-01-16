from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.http import HttpResponse

from movies.models import MoviePost
from movies.forms import CreateMoviePostForm, UpdateMoviePostForm

from users.models import User


def create_movie_view(request):

	context = {}

	user = request.user
	if not user.is_authenticated:
		return redirect('must_authenticate')

	form = CreateMoviePostForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		obj = form.save(commit=False)
		author = User.objects.filter(email=user.email).first()
		obj.author = author
		obj.save()
		form = CreateMoviePostForm()

	context['form'] = form

	return render(request, "movies/create_movie.html", context)


def detail_movie_view(request, slug):

	context = {}

	movie_post = get_object_or_404(MoviePost, slug=slug)
	context['movie_post'] = movie_post

	return render(request, 'movies/detail_movie.html', context)



def edit_movie_view(request, slug):

	context = {}

	user = request.user
	if not user.is_authenticated:
		return redirect("must_authenticate")

	movie_post = get_object_or_404(MoviePost, slug=slug)

	if movie_post.author != user:
		return HttpResponse("You are not the author of that post.")

	if request.POST:
		form = UpdateMoviePostForm(request.POST or None, request.FILES or None, instance=movie_post)
		if form.is_valid():
			obj = form.save(commit=False)
			obj.save()
			context['success_message'] = "Updated"
			movie_post = obj

	form = UpdateMoviePostForm(
			initial = {
					"title": movie_post.title,
					"body": movie_post.body,
					"image": movie_post.image,
			}
		)

	context['form'] = form
	return render(request, 'movies/edit_movie.html', context)


def get_movie_queryset(query=None):
	queryset = []
	queries = query.split(" ")
	for q in queries:
		posts = MoviePost.objects.filter(
				Q(title__icontains=q) | 
				Q(gender__icontains=q) | 
				Q(director__icontains=q) |
				Q(body__icontains=q)
			).distinct()

		for post in posts:
			queryset.append(post)

	return list(set(queryset))	