import re ,os, pytube ,urllib

def search_youtube(query):
    query = query.replace(' ', '+')
    html = urllib.request.urlopen(f"https://www.youtube.com/results?search_query={query}")
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
    url = f"https://www.youtube.com/watch?v={video_ids[0]}"
    return url

class Video(object):
    def __init__(self,url): self.url = url

    def download_url(self):
        yt = pytube.YouTube(self.url)
        audio = yt.streams.filter(only_audio=True).first()
        name = audio.title
        audio.download('./')
        self.file_url =  audio.get_file_path(name) + '.mp4'

    def play_Url(self):
        if os.path.exists(self.file_url):
            from os import startfile
            startfile(self.file_url)
        else:
            print('Something went wrong!\nCouldn`t find file {0}'.format(self.file_url))

    def delete_file(self):
        if os.path.exists(self.file_url):
            os.remove(self.file_url)

    def file_already_exsistent(self):
        yt = pytube.YouTube(self.url)
        audio = yt.streams.filter(only_audio=True).first()
        name = audio.title
        if os.path.isfile('./'+name+'.mp4'):
            self.file_url =  audio.get_file_path(name) + '.mp4'
            return True
        else:
            return False
def main():
    inp = input('Search for a Video:')
    url = search_youtube(inp)
    print('You searched {0} and got: {1}'.format(inp,url))
    play = input('Want to play?(y/n)')
    if play == 'y':
        video = Video(url)
        if not video.file_already_exsistent():
            video.download_url()
        video.play_Url()
    delet = input('Want to delete the file(y/n)')
    if delet == 'y':
        video.delete_file()

if __name__ == '__main__':
    main()