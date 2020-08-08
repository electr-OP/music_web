from django.urls import path
from . import views


app_name = 'music'

urlpatterns = [
    # /music/
    path('', views.indexview.as_view(), name='index'),

    path('registration_data/', views.UserFormView.as_view(), name='registration'),

    # /music/741/
    #path('<int:pk>/', views.songdetailview.as_view(), name='detail'),
    path('<int:pk>/', views.detailview.as_view(), name='detail'),

    

    path('album/add/', views.AlbumCreate.as_view(), name='add-album'),


    path('album/<int:pk>/', views.AlbumUpdate.as_view(), name='update_album'),

    path('album/<int:pk>/delete/', views.AlbumDelete.as_view(), name='delete_album'),



]
