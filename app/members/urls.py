from django.urls import path, include
from . import new_apis

urlpatterns_members_signup = ([
    path('', new_apis.SiteSignUpAPIView.as_view()),
    path('check-username/', new_apis.SignUpCheckIDView.as_view()),

], 'signup')

urlpatterns_members = ([
    path('user/', new_apis.UserView.as_view()),
    path('signup/', include(urlpatterns_members_signup)),
    path('login/', new_apis.SiteAuthTokenAPIView.as_view()),
    path('social-login/', new_apis.SocialAuthTokenAPIView.as_view()),
    path('like-item/', new_apis.LikeItemListCreateDestroyView.as_view()),
], 'members')
