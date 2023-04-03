from django.shortcuts import render
from django.views import View
from django.conf import settings
from pathlib import Path

from pytube import YouTube


# Create your views here.


class HomeView(View):
    template_name = 'downloader/home.html'
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    
    def post(self, request, *args, **kwargs):
        convertion_type = request.POST.get('convertion-type')
        url = request.POST.get('url')
        yt = YouTube(url)

        # for item in yt.streams.filter(only_audio=True):
        #     print(item.abr)
        #     print(item.url)

        stream = yt.streams.filter(only_audio=True).first()
        dire = Path.joinpath(settings.BASE_DIR, 'medias')
        a = stream.download(dire)
    
        with open(a, 'rb') as file:
            data = file.read()

        context = {'url': data}
        return render(request, self.template_name, context)
