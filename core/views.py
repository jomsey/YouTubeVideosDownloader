from urllib.error import URLError
from django.shortcuts import render
from django.views import View
from django.contrib import messages
from core.forms import UserInputForm
from pytube import YouTube,Search
from django.http import FileResponse
from io import BytesIO
import re,math,os


class IndexView(View):
    def get(self,request):
        form=UserInputForm()
        return render(request,"core/index.html",context={"form":form})
    
    def video_time_formatted(self,video_length:int):
        hr = "" if video_length//3600 == 0 else str(video_length//3600)+":" 
        min_ = math.floor((video_length%3600)/60)
        sec=video_length%60
        formatted_time = f"{hr}{min_}:{sec}"
        return formatted_time
    
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
                                "duration":self.video_time_formatted(video.length),
                                "description":video.description,
                                "thumbnail":video.thumbnail_url,
                                "id":video.video_id,
                   }
                    
                    context.update({"info":info_dict})
                
                else:
                    search =Search(query)
                    
                    results = list({ "title":result.title,
                                     "duration":self.video_time_formatted(result.length),
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
        stream = yt.streams.get_highest_resolution()
        
        _data = stream.download()
        path = os.path.normpath(_data)
        
        with open (path,"rb") as video_file:
            data = video_file.read()
            
        os.remove(_data)
        messages.success(request,"Download complete")
        return  FileResponse(BytesIO(data,file_name=f'{yt.title}.mp4',as_attachment=True,content_type="application/video/mp4"))
    

class VideoDetailView(View):
    def get(self,request):
        pass