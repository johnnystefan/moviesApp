from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from users.forms import RegistrationForm, UserAuthenticationForm, UserUpdateForm

from movies.models import MoviePost

def registration_view(request):
	context = {}
	if request.POST:
		form = RegistrationForm(request.POST)
		if form.is_valid():
			form.save()
			email = form.cleaned_data.get('email').lower()
			raw_password = form.cleaned_data.get('password1')
			user = authenticate(email=email, password=raw_password)
			login(request, user)
			return redirect('home')
		else:
			context['registration_form'] = form

	else:
		form = RegistrationForm()
		context['registration_form'] = form
	return render(request, 'users/register.html', context)


def logout_view(request):
	logout(request)
	return redirect('/')


def login_view(request):

	context = {}

	user = request.user
	if user.is_authenticated:
		return redirect("home")

	if request.POST:
		form = UserAuthenticationForm(request.POST)
		if form.is_valid():
			email = request.POST['email']
			password = request.POST['password']
			user = authenticate(email=email, password=password)

			if user:
				login(request, user)
				return redirect("home")

	else:
		form = UserAuthenticationForm()

	context['login_form'] = form

	# print(form)
	return render(request, "users/login.html", context)


def user_view(request):

	if not request.user.is_authenticated:
			return redirect("login")

	context = {}
	if request.POST:
		form = UserUpdateForm(request.POST, instance=request.user)
		if form.is_valid():
			form.initial = {
					"email": request.POST['email'],
					"username": request.POST['username'],
			}
			form.save()
			context['success_message'] = "Updated"
	else:
		form = UserUpdateForm(

			initial={
					"email": request.user.email,
					"username": request.user.username,
				}
			)

	context['user_form'] = form

	movie_posts = MoviePost.objects.filter(author=request.user)
	context['movie_posts'] = movie_posts

	return render(request, "users/user.html", context)


def must_authenticate_view(request):
	return render(request, 'users/must_authenticate.html', {})

