from django.urls import path
from .views import *


urlpatterns = [
   path('', PostsList.as_view(), name='posts'),
   path('post/<int:pk>', PostDetail.as_view(), name='post_detail'),
   path('createpost', PostCreate.as_view(), name='post_create'),
   path('post/<int:pk>/delete', PostDelete.as_view(), name='post_delete'),
   path('post/<int:pk>/edit', PostUpdate.as_view(), name='post_edit'),
   path('mycomments/', CommentsList.as_view(), name='mycomments'),
   path('post/comment_sent_for_approval', CommentForApproval.as_view(), name='comment_sent_for_approval'),
]
