from django.urls import path
from .views import*


urlpatterns = [
    path('uhome/',UserHome.as_view(),name="uhome"),
    path('profile/',ViewProfile.as_view(),name="profile"),
    path('addbio/',UserProfView.as_view(),name="addbio"),
    path('change-password/',ChangePasswordView.as_view(),name="change-password"),
    path('updatebio/<int:user_id>',UpdateBioView.as_view(),name="update-bio"),
    path('addcmnt/<int:id>',add_comment,name="add-cmnt"),
    path('bloglike/<int:bid>',add_like,name="add-like"),
    path('blog/',MyBlogs.as_view(),name="blog"),
]
