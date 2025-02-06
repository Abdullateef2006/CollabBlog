from django.urls import path, re_path
from .views import *


urlpatterns = [
    path('category/', Category_api.as_view()),
    path('review/', Review_api.as_view()),

    path('post/', Post_api.as_view()),
    path('category/<str:name>/', Course_List_Category.as_view()), 
    path('profile/', ProfileCreateEdit.as_view(), name='edit_profile'),  # Regular view
    path('api/create_post/', PostCreateAPIView.as_view(), name='post_create'),
    path('post/<str:name>/', Post_detail_api.as_view(),  name="post_detail"),
    path('posts/<str:name>/comments/', CommentListCreateView.as_view(), name='comment-list-create'),
    path('send_invitation/<str:name>/',SendInvitationView.as_view(), name='send_invitations'),

    path('api/send_invitation/<int:post_id>/',send_invitation, name='send_invitation'),
    path('api/accept_invitation/<uuid:token>/', accept_invitation, name='accept_invitation'),
    path('api/list_contributors/<str:name>/', list_contributors, name='list_contributors'),
    path('api/edit_post/<str:name>/', EditPostView.as_view(), name='edit-post'),
    path('subscribe/', SubscriptionView.as_view(), name='subscribe'),
    path('creator_profile/<int:id>/', CreatorProfileAPIView.as_view(), name='creator_profile'),



]
    
    
    
