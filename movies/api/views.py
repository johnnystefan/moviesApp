from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter, OrderingFilter

from users.models import User
from movies.models import MoviePost
from movies.api.serializers import MoviePostSerializer, MoviePostUpdateSerializer, MoviePostCreateSerializer

SUCCESS = 'success'
ERROR = 'error'
DELETE_SUCCESS = 'deleted'
UPDATE_SUCCESS = 'updated'
CREATE_SUCCESS = 'created'

# Url: https://<your-domain>/api/movie/<slug>/
# Headers: Authorization: Token <token>
@api_view(['GET', ])
@permission_classes((IsAuthenticated, ))
def api_detail_movie_view(request, slug):

	try:
		movie_post = MoviePost.objects.get(slug=slug)
	except MoviePost.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	if request.method == 'GET':
		serializer = MoviePostSerializer(movie_post)
		return Response(serializer.data)

# Url: https://<your-domain>/api/movie/<slug>/update
# Headers: Authorization: Token <token>
@api_view(['PUT',])
@permission_classes((IsAuthenticated,))
def api_update_movie_view(request, slug):

	try:
		movie_post = MoviePost.objects.get(slug=slug)
	except MoviePost.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	user = request.user
	if movie_post.author != user:
		return Response({'response':"You don't have permission to edit that."})

	if request.method == 'PUT':
		serializer = MoviePostUpdateSerializer(movie_post, data=request.data, partial=True)
		data = {}
		if serializer.is_valid():
			serializer.save()
			data['response'] = UPDATE_SUCCESS
			data['pk'] = movie_post.pk
			data['title'] = movie_post.title
			data['director'] = movie_post.director
			data['gender'] = movie_post.gender
			data['body'] = movie_post.body
			data['slug'] = movie_post.slug
			data['date_updated'] = movie_post.date_updated
			image_url = str(request.build_absolute_uri(movie_post.image.url))
			if "?" in image_url:
				image_url = image_url[:image_url.rfind("?")]
			data['image'] = image_url
			data['username'] = movie_post.author.username
			return Response(data=data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET',])
@permission_classes((IsAuthenticated,))
def api_is_author_of_moviepost(request, slug):
	try:
		movie_post = MoviePost.objects.get(slug=slug)
	except MoviePost.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	data = {}
	user = request.user
	if movie_post.author != user:
		data['response'] = "You don't have permission to edit that."
		return Response(data=data)
	data['response'] = "You have permission to edit that."
	return Response(data=data)

# Url: https://<your-domain>/api/movie/<slug>/delete
# Headers: Authorization: Token <token>
@api_view(['DELETE',])
@permission_classes((IsAuthenticated, ))
def api_delete_movie_view(request, slug):

	try:
		movie_post = MoviePost.objects.get(slug=slug)
	except MoviePost.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	user = request.user
	if movie_post.author != user:
		return Response({'response':"You don't have permission to delete that."}) 

	if request.method == 'DELETE':
		operation = movie_post.delete()
		data = {}
		if operation:
			data['response'] = DELETE_SUCCESS
		return Response(data=data)

# Url: https://<your-domain>/api/movie/create
# Headers: Authorization: Token <token>
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def api_create_movie_view(request):

	if request.method == 'POST':

		data = request.data
		data['author'] = request.user.pk
		serializer = MoviePostCreateSerializer(data=data)

		data = {}
		if serializer.is_valid():
			movie_post = serializer.save()
			data['response'] = CREATE_SUCCESS
			data['pk'] = movie_post.pk
			data['title'] = movie_post.title
			data['director'] = movie_post.director
			data['gender'] = movie_post.gender
			data['body'] = movie_post.body
			data['slug'] = movie_post.slug
			data['date_updated'] = movie_post.date_updated
			image_url = str(request.build_absolute_uri(movie_post.image.url))
			if "?" in image_url:
				image_url = image_url[:image_url.rfind("?")]
			data['image'] = image_url
			data['username'] = movie_post.author.username
			return Response(data=data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Url:
#		1) list: https://<your-domain>/api/movie/list
#		2) pagination: http://<your-domain>/api/movie/list?page=2
#		3) search: http://<your-domain>/api/movie/list?search=johnny
#		4) ordering: http://<your-domain>/api/movie/list?ordering=-date_updated
#		4) search + pagination + ordering: <your-domain>/api/movie/list?search=johnny&page=2&ordering=-date_updated
# Headers: Authorization: Token <token>
class ApiMovieListView(ListAPIView):
	queryset = MoviePost.objects.all()
	serializer_class = MoviePostSerializer
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)
	pagination_class = PageNumberPagination
	filter_backends = (SearchFilter, OrderingFilter)
	search_fields = ('title', 'body', 'gender', 'director', 'author__username')