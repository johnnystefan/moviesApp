from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.generics import UpdateAPIView
from django.contrib.auth import authenticate
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from users.api.serializers import RegistrationSerializer, UserPropertiesSerializer, ChangePasswordSerializer
from users.models import User
from rest_framework.authtoken.models import Token

# Register
# Url: https://<your-domain>/api/user/register
@api_view(['POST', ])
@permission_classes([])
@authentication_classes([])
def registration_view(request):

	if request.method == 'POST':
		data = {}
		email = request.data.get('email', '0').lower()
		if validate_email(email) != None:
			data['error_message'] = 'That email is already in use.'
			data['response'] = 'Error'
			return Response(data)

		username = request.data.get('username', '0')
		if validate_username(username) != None:
			data['error_message'] = 'That username is already in use.'
			data['response'] = 'Error'
			return Response(data)

		serializer = RegistrationSerializer(data=request.data)

		if serializer.is_valid():
			user = serializer.save()
			data['response'] = 'successfully registered new user.'
			data['email'] = user.email
			data['username'] = user.username
			data['pk'] = user.pk
			token = Token.objects.get(user=user).key
			data['token'] = token
		else:
			data = serializer.errors
		return Response(data)

def validate_email(email):
	user = None
	try:
		user = User.objects.get(email=email)
	except User.DoesNotExist:
		return None
	if user != None:
		return email

def validate_username(username):
	user = None
	try:
		user = User.objects.get(username=username)
	except User.DoesNotExist:
		return None
	if user != None:
		return username


# User properties
# Url: https://<your-domain>/api/user/
# Headers: Authorization: Token <token>
@api_view(['GET', ])
@permission_classes((IsAuthenticated, ))
def user_properties_view(request):

	try:
		user = request.user
	except User.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	if request.method == 'GET':
		serializer = UserPropertiesSerializer(user)
		return Response(serializer.data)


# User update properties
# Url: https://<your-domain>/api/user/properties/update
# Headers: Authorization: Token <token>
@api_view(['PUT',])
@permission_classes((IsAuthenticated, ))
def update_user_view(request):

	try:
		user = request.user
	except User.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	if request.method == 'PUT':
		serializer = UserPropertiesSerializer(user, data=request.data)
		data = {}
		if serializer.is_valid():
			serializer.save()
			data['response'] = 'User update success'
			return Response(data=data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# LOGIN
# URL: http://127.0.0.1:8000/api/user/login
class ObtainAuthTokenView(APIView):

	authentication_classes = []
	permission_classes = []

	def post(self, request):
		context = {}

		email = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(email=email, password=password)
		if user:
			try:
				token = Token.objects.get(user=user)
			except Token.DoesNotExist:
				token = Token.objects.create(user=user)
			context['response'] = 'Successfully authenticated.'
			context['pk'] = user.pk
			context['email'] = email.lower()
			context['token'] = token.key
		else:
			context['response'] = 'Error'
			context['error_message'] = 'Invalid credentials'

		return Response(context)




@api_view(['GET', ])
@permission_classes([])
@authentication_classes([])
def does_user_exist_view(request):

	if request.method == 'GET':
		email = request.GET['email'].lower()
		data = {}
		try:
			user = User.objects.get(email=email)
			data['response'] = email
		except User.DoesNotExist:
			data['response'] = "User does not exist"
		return Response(data)



class ChangePasswordView(UpdateAPIView):

	serializer_class = ChangePasswordSerializer
	model = User
	permission_classes = (IsAuthenticated,)
	authentication_classes = (TokenAuthentication,)

	def get_object(self, queryset=None):
		obj = self.request.user
		return obj

	def update(self, request, *args, **kwargs):
		self.object = self.get_object()
		serializer = self.get_serializer(data=request.data)

		if serializer.is_valid():
			# Check old password
			if not self.object.check_password(serializer.data.get("old_password")):
				return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)

			# confirm the new passwords match
			new_password = serializer.data.get("new_password")
			confirm_new_password = serializer.data.get("confirm_new_password")
			if new_password != confirm_new_password:
				return Response({"new_password": ["New passwords must match"]}, status=status.HTTP_400_BAD_REQUEST)

			# set_password also hashes the password that the user will get
			self.object.set_password(serializer.data.get("new_password"))
			self.object.save()
			return Response({"response":"successfully changed password"}, status=status.HTTP_200_OK)

		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





















