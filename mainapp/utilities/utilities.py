import os, base64, requests

token = '';
def get_sound_file_name(word_object):
    soundFileName = word_object.universalsounds_set.all().first().soundfile
    soundsDir = os.path.dirname(os.path.dirname(__file__)) + '/static/mainapp/sounds/'

    if soundFileName != '':
        if not os.path.exists(soundsDir + soundFileName):
            # Запрос на получение файла
            global token
            if token == '':
                token = requests.post('https://developers.lingvolive.com/api/v1.1/authenticate', headers = {"Authorization": "Basic ZTc1ZDY2MmMtZjkxZi00NTNlLWExY2MtNjA3Y2RlNjJhMDYyOjQzOGZlNzcxNTAxODQzODI4OTA3OWI4MjQ2ZmExZTI1"}, verify = False).text
        
            response = requests.get('https://developers.lingvolive.com/api/v1/Sound/', headers = {"Authorization": "Bearer " + token}, params = {"dictionaryName": 'Universal (Es-Ru)', "fileName": soundFileName}, verify = False)
            fileDecoded = base64.b64decode(response.text)
            of = open(soundsDir + soundFileName, 'wb')
            of.write(fileDecoded)
            of.close()
        
        soundFileName = '/static/mainapp/sounds/' + soundFileName

    return soundFileName