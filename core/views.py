

from urllib.error import URLError
from django.shortcuts import render
from django.views import View
from django.contrib import messages
from core.engine import YoutubeVideo
from core.forms import UserInputForm
import re
from pytube import YouTube,Search



class IndexView(View):
    def get(self,request):
        form=UserInputForm()
        return render(request,"core/index.html",context={"form":form})
    
    
    def post(self,request):
        form=UserInputForm(request.POST)
        context = {"form":form}
        URL_PATTERN="^https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)$"

        try:
            if form.is_valid():
                query = form.cleaned_data.get("query")
                
                #check either url or search term submitted
                if re.match(URL_PATTERN,query):
                    yt = YouTube(query)
                    video  = yt.streams.get_highest_resolution()
                    info_dict={"title":video.title,
                                "size":video.filesize,
                                "duration":video.length,
                                "description":video.description,
                                "thumbnail":video.thumbnail_url,
                                "id":video.video_id,
                   }
                    
                    context.update({"info":info_dict})
                
                else:
                    search =Search(query)
                    
                    results = list({ "title":result.title,
                                     "duration":result.length,
                                     "url":result.watch_url,
                                     "thumbnail":result.thumbnail_url,
                                     "publish_date":result.publish_date,
                                    "description":result.description,
                                     "id":result.video_id,} for result in search.results
                             )
                    
                    context.update({"videos":results,"query":query})
                  
                return render(request,"core/index.html",context=context)
        except(URLError):
            messages.info(request,"Action Not Successful. Try again later")
          
        
        return render(request,"core/index.html",context=context)
        
class DownloadVideoView(View):
    def get(self,request,video_id):
        video_url = f"http://youtu.be/{video_id}"
        yt = YouTube(video_url)
        video = yt.streams.get_highest_resolution()
        video.download()
        messages.success(request,"Download complete")
        return render(request,"core/index.html")
    

class VideoDetailView(View):
    def get(self,request):
        pass