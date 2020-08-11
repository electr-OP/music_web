from django.urls import path
from . import views



app_name = 'music'

urlpatterns = [
    # /music/
    path('', views.indexview.as_view(), name='index'),
    path('<int:pk>/', views.detailview.as_view(), name='detail'),
    path('registration_data/', views.UserFormView.as_view(), name='registration'),
    # /music/741/
    #path('<int:pk>/', views.songdetailview.as_view(), name='detail'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('album/add/', views.AlbumCreate.as_view(), name='add-album'),
    path('album/<int:pk>/', views.AlbumUpdate.as_view(), name='update_album'),
    path('album/<int:pk>/delete/', views.AlbumDelete.as_view(), name='delete_album'),
    path('song/<int:pk>/add/', views.SongCreate.as_view(), name='add-song'),



]
