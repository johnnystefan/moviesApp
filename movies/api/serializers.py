from rest_framework import serializers
from movies.models import MoviePost

import os
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.storage import FileSystemStorage
IMAGE_SIZE_MAX_BYTES = 1024 * 1024 * 2 # 2MB
MIN_TITLE_LENGTH = 5
MIN_BODY_LENGTH = 50

from movies.utils import is_image_aspect_ratio_valid, is_image_size_valid


class MoviePostSerializer(serializers.ModelSerializer):

	username = serializers.SerializerMethodField('get_username_from_author')
	image 	 = serializers.SerializerMethodField('validate_image_url')

	class Meta:
		model = MoviePost
		fields = ['pk', 'title', 'slug', 'body', 'gender', 'director', 'image', 'date_updated', 'username']


	def get_username_from_author(self, movie_post):
		username = movie_post.author.username
		return username

	def validate_image_url(self, movie_post):
		image = movie_post.image
		new_url = image.url
		if "?" in new_url:
			new_url = image.url[:image.url.rfind("?")]
		return new_url




class MoviePostUpdateSerializer(serializers.ModelSerializer):

	class Meta:
		model = MoviePost
		fields = ['title', 'body', 'image']

	def validate(self, movie_post):
		try:
			title = movie_post['title']
			if len(title) < MIN_TITLE_LENGTH:
				raise serializers.ValidationError({"response": "Enter a title longer than " + str(MIN_TITLE_LENGTH) + " characters."})

			body = movie_post['body']
			if len(body) < MIN_BODY_LENGTH:
				raise serializers.ValidationError({"response": "Enter a body longer than " + str(MIN_BODY_LENGTH) + " characters."})

			image = movie_post['image']
			url = os.path.join(settings.TEMP , str(image))
			import pdb; pdb.set_trace()
			storage = FileSystemStorage(location=url)

			with storage.open('', 'wb+') as destination:
				for chunk in image.chunks():
					destination.write(chunk)
				destination.close()

			# Check image size
			if not is_image_size_valid(url, IMAGE_SIZE_MAX_BYTES):
				os.remove(url)
				raise serializers.ValidationError({"response": "That image is too large. Images must be less than 2 MB. Try a different image."})

			# Check image aspect ratio
			if not is_image_aspect_ratio_valid(url):
				os.remove(url)
				raise serializers.ValidationError({"response": "Image height must not exceed image width. Try a different image."})

			os.remove(url)
		except KeyError:
			pass
		return movie_post


class MoviePostCreateSerializer(serializers.ModelSerializer):


	class Meta:
		model = MoviePost
		fields = ['title', 'body', 'image', 'gender', 'director', 'date_updated', 'author']


	def save(self):

		try:
			image = self.validated_data['image']
			title = self.validated_data['title']
			if len(title) < MIN_TITLE_LENGTH:
				raise serializers.ValidationError({"response": "Enter a title longer than " + str(MIN_TITLE_LENGTH) + " characters."})

			body = self.validated_data['body']
			if len(body) < MIN_BODY_LENGTH:
				raise serializers.ValidationError({"response": "Enter a body longer than " + str(MIN_BODY_LENGTH) + " characters."})

			movie_post = MoviePost(
								author=self.validated_data['author'],
								title=title,
								body=body,
								image=image,
								)

			url = os.path.join(settings.TEMP , str(image))
			storage = FileSystemStorage(location=url)

			with storage.open('', 'wb+') as destination:
				for chunk in image.chunks():
					destination.write(chunk)
				destination.close()

			# Check image size
			if not is_image_size_valid(url, IMAGE_SIZE_MAX_BYTES):
				os.remove(url)
				raise serializers.ValidationError({"response": "That image is too large. Images must be less than 2 MB. Try a different image."})

			# Check image aspect ratio
			if not is_image_aspect_ratio_valid(url):
				os.remove(url)
				raise serializers.ValidationError({"response": "Image height must not exceed image width. Try a different image."})

			os.remove(url)
			movie_post.save()
			return movie_post
		except KeyError:
			raise serializers.ValidationError({"response": "You must have a title, some content, and an image."})