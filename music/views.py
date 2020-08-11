from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserForm, LoginForm, SongForm
from .models import Album, Song
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.http import Http404
from django.template import loader
from django.views import generic
from django.views.generic import View


"""
def index(request):
    all_albums = Album.objects.all()
    context = {'all_albums': all_albums, }
    return render(request, 'music/index.html', context)


def detail(request, album_id):
    try:
        album = Album.objects.get(id=album_id)
    except Album.DoesNotExist:
        raise Http404('Album does not exist')
    context = {'album': album, }
    return render(request, 'music/detail.html', context)
"""


class indexview(LoginRequiredMixin, generic.ListView):
    login_url = 'login/'
    redirect_field_name = 'redirect_to'
    template_name = 'music/index.html'
    context_object_name = 'all_albums'

    def get_queryset(self):
       # print(self.request.user)
        return Album.objects.all()


class detailview(generic.DetailView):
    model = Album
    template_name = 'music/detail.html'


class songdetailview(generic.ListView):
    template_name = 'music/detail.html'

    context_object_name = 'all_songs'

    def get_queryset(self):
        return Song.objects.all()


class AlbumCreate(CreateView):
    model = Album
    # fields = ['artist', 'album_title', 'genre', 'album_logo']
    fields = '__all__'


class AlbumUpdate(UpdateView):
    model = Album
    fields = ['artist', 'album_title', 'genre', 'album_logo']


class AlbumDelete(DeleteView):
    model = Album
    success_url = reverse_lazy('music:index')


class UserFormView(View):
    form_class = UserForm
    template_name = 'music/registration_data.html'

    # blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    all_albums = Album.objects.filter(user=request.user)
                    # return render(request, 'music:index', {'albums':albums})
                    return redirect('music:index', {'all_albums': all_albums})

        return render(request, self.template_name, {'form': form})


class LoginView(View):
    def get(self, request):
        return render(request, 'music/login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                all_albums = Album.objects.all()
                return render(request, 'music/index.html', {'all_albums': all_albums})
            else:
                return render(request, 'music/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'music/login.html', {'error_message': 'Invalid login'})

class LogoutView(View):
    form_class = UserForm
    template_name = 'music/login.html'
    def get(self,request):
        logout(request)
        form = self.form_class(request.POST or None)
        context ={'form':form}
        return render(request, self.template_name, context)

class SongCreate(CreateView):
    model = Song
    fields = ['song_title', 'song_file']

    def form_valid(self, form):
        album = get_object_or_404(Album, pk=self.kwargs['pk'])
        form.instance.album = album
        return super(SongCreate, self).form_valid(form)

        #object = form.save(commit=False)
        #object.user = self.request.user
        #object.save()
        #return super(SongCreate, self).form_valid(form)

