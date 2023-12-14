import re ,os, pytube ,urllib, tempfile

def search_youtube(query):
    query = query.replace(' ', '+')
    html = urllib.request.urlopen(f"https://www.youtube.com/results?search_query={query}")
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
    url = f"https://www.youtube.com/watch?v={video_ids[0]}"
    return url

class Video(object):
    def __init__(self,url): self.url = url

    def download_url(self):
        temp_file = tempfile.NamedTemporaryFile()
        yt = pytube.YouTube(self.url)
        audio = yt.streams.filter(only_audio=True).first()
        temp_file.write(audio.download().encode('utf-8'))
        temp_file.seek(0)
        self.temp_file =  temp_file.read()#audio.get_file_path(name) + '.mp4'

    def play_Url(self):
        if self.temp_file:
            from os import startfile
            startfile(self.temp_file)
        else:
            print('Something went wrong!\nCouldn`t find file {0}'.format(self.temp_file))

    def delete_file(self):
        if self.temp_file:
            os.remove(self.temp_file)

def main():
    inp = input('Search for a Video:')
    url = search_youtube(inp)
    print('You searched {0} and got: {1}'.format(inp,url))
    play = input('Want to play?(y/n)')
    if play == 'y':
        video = Video(url)
        video.download_url()
        video.play_Url()
        delet = input('Want to delete the file(y/n)')
        if delet == 'y':
            video.delete_file()

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print('Error: {0}'.format(e))
