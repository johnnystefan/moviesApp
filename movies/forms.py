from django import forms

from movies.models import MoviePost


class CreateMoviePostForm(forms.ModelForm):

	class Meta:
		model = MoviePost
		fields = ['title', 'body', 'image', 'gender', 'director']



class UpdateMoviePostForm(forms.ModelForm):

	class Meta:
		model = MoviePost
		fields = ['title', 'body', 'image']

	def save(self, commit=True):
		movie_post = self.instance
		movie_post.title = self.cleaned_data['title']
		movie_post.body = self.cleaned_data['body']

		if self.cleaned_data['image']:
			movie_post.image = self.cleaned_data['image']

		if commit:
			movie_post.save()
		return movie_post