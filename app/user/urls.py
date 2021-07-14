from django.urls import path  # helper function

from user import views

app_name = 'user'

# url calling a function from views
urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),  # for create_user wire a CreateUserView from views.py
    path('token/', views.CreateTokenView.as_view(), name='token'),  # for create token, wire a CreateTokenView from views.py
    path('me/', views.ManageUserView.as_view(), name='me'),  # for update user, wire a ManageUserView from views.py
]  # give name to identify when using the reverse lookup function

# once url is updated in user.urls, update in app.urls

