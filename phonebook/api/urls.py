from django.urls import path
from .views import RegistrationView, LoginView, SearchView, UserDetailsView, SpamView, ContactListView
urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('search/', SearchView.as_view(), name='search'),
    path('user/', UserDetailsView.as_view(), name='user-details'),
    path('contacts/', ContactListView.as_view(), name='contacts'),
    path('spam/', SpamView.as_view(), name='mark-contact-spam'),
]
