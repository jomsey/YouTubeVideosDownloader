from pytube import YouTube,Search
import os
import math

     
class YoutubeVideo:
    def __init__(self,url):
        self.url = url
        
    def get_video(self):
        """
        Gets video with the highest resolution
        Returns:
            stream with highest resolution
        """
        yt_video =  YouTube(self.url).streams.get_highest_resolution()
        return yt_video
    
    def __video_time_formatted(self,video_length:int):
        hr = "" if video_length//3600 == 0 else str(video_length//3600)+":" 
        min_ = math.floor((video_length%3600)/60)
        sec=video_length%60
        formatted_time = f"{hr}{min_}:{sec}"
        return formatted_time
        
    def _get_video_duration(self):
        time = YouTube(self.url).length
        return self.__video_time_formatted(time)
     
        
    def video_info(self):
        video =self.get_video()
        video_size = math.floor(video.filesize/1049600)
        title= video.title
        description = YouTube(self.url).description
        video_id  = self.url.split('/')[-1]
        
        info_dict={"title":title,
                   "size":video_size,
                   "duration":self._get_video_duration(),
                   "description":description,
                   "thumbnail":YouTube(self.url).thumbnail_url,
                   "id":video_id,
                   }
        
        return  info_dict
                 
    def download_video(self):
        video=self.get_video()
        directory = self.download_directory("videos")
        video.download(max_retries=30,output_path=directory)
        self.download_complete()
       
    def download_audio(self):
        """
         get audio formats from the youtube video downloads
        """
      
        audio= YouTube(self.url).streams.get_audio_only()
        directory = self.download_directory("audio")
        audio.download(max_retries=3,output_path=directory)
        
        os.chdir(directory)  # directory where the downloaded is located
        self.rename_to_mp3(audio)
    
    @classmethod   
    def search_video(cls,query):
        """
        search youtube video and return search video url for the selected
        """
        search =  Search(query)
        return list({"title":result.title,
                     "duration":cls.__video_time_formatted(cls,result.length),
                     "url":result.watch_url,
                     "thumbnail":result.thumbnail_url,
                     "publish_date":result.publish_date,
                     "description":result.description} for result in search.results)
    
   
    @classmethod         
    def rename_to_mp3(self,file):
        """
        Replaces mp4 video extension on the downloaded audio file to mp3.
        Removes undesired naming on the video like "official video "
        """
    
        new_audio_name = file.default_filename.removesuffix('.mp4')+".mp3"
        
        try:
            # rename download when complete
            os.rename(file.default_filename,new_audio_name)
        except FileExistsError:
           pass
        
                 
    def download_directory(self,sub_folder=None):
        """
        if directory doesn't exit creates  it to the current folder,
        where downloaded file is stored
        Returns:
            str: directory
        """
        BASE_DIR =os.environ.get("HOMEPATH")
        
        path=f'{BASE_DIR}\Desktop\downloads'
        directory=os.path.join(path,"YTDownloader")
        if sub_folder:
            directory+=f"\{sub_folder}"

        if not os.path.exists(directory):
            os.makedirs(directory)  
             
        return directory
    
    