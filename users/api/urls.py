from django.urls import path
from users.api.views import(
	registration_view,
	ObtainAuthTokenView,
	user_properties_view,
	update_user_view,
	does_user_exist_view,
	ChangePasswordView,
)
from rest_framework.authtoken.views import obtain_auth_token

app_name = 'users'

urlpatterns = [
	path('check_if_user_exists/', does_user_exist_view, name="check_if_user_exists"),
	path('change_password/', ChangePasswordView.as_view(), name="change_password"),
	path('properties', user_properties_view, name="properties"),
	path('properties/update', update_user_view, name="update"),
	path('login', ObtainAuthTokenView.as_view(), name="login"),
	path('register', registration_view, name="register"),

]