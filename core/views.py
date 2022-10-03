
import asyncio
from urllib.error import URLError
from django.shortcuts import render
from django.views import View
from django.contrib import messages
from core.engine import YoutubeVideo
from core.forms import UserInputForm
import re


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
                    yt = YoutubeVideo(query)
                    context.update({"info":yt.video_info()})
                
                else:
                    results = asyncio.run(YoutubeVideo.search_video(query))
                    context.update({"videos":results,"query":query})
                return render(request,"core/index.html",context=context)
        except(URLError):
            messages.info(request,"Action Not Successful. Try again later")
          
        
              
        return render(request,"core/index.html",context=context)
        
class DownloadVideoView(View):
    def get(self,request,video_url):
        yt = YoutubeVideo(video_url)
        yt.download_video()
        messages.success(request,"Download complete")
        return render(request,"core/index.html")
    

class VideoDetailView(View):
    def get(self,request):
        pass