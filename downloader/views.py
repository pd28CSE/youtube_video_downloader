from django.shortcuts import render
from django.views import View
from django.conf import settings
from django.http import FileResponse, HttpResponseBadRequest
from pathlib import Path

from pytube import YouTube


# Create your views here.


class HomeView(View):
    template_name = 'downloader/home.html'
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    
    def post(self, request, *args, **kwargs):
        
        url = request.POST.get('url')
        # convertion_type = request.POST.get('convertion-type')

        try:
            yt = YouTube(url)
            dc = dict()
            for item in yt.streams.filter(only_audio=True):
                # print(item.abr)
                # print(item.url)
                dc[item.abr.replace('kbps', '')] = item.itag
            maxKbps = max([int(i) for i in dc.keys()])
            bestQualityItag = dc[f'{maxKbps}']
            dc.clear()

            # stream = yt.streams.filter(only_audio=True).first()
            # dire = Path.joinpath(settings.BASE_DIR, 'medias')

            # a = stream.download(dire)
            # with open(a, 'rb') as file:
            #     data = file.read()
        except Exception as e:
            return HttpResponseBadRequest('Please Enter Youtube Video URL.')
        return FileResponse(open(yt.streams.get_by_itag(bestQualityItag).download(), 'rb'), as_attachment=True)