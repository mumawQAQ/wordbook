import requests


class Pronounce(object):
    def __init__(self):
        self.url = 'https://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob'
        self.header = {
            'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
            'referer':'https://www.google.com/'
        }

    def get_audio(self,word):
        word = word
        para = {
            'q':word,
            'tl':'en',
            'total':'1',
            'idx':'0',
            'textlen': len(word)
        }
        res = requests.get(self.url,params=para,headers=self.header)
        with open('./audio/'+word+".mp3",'wb') as f:
            f.write(res.content)

if __name__ == '__main__':
    p = Pronounce()
    p.get_audio("hello")