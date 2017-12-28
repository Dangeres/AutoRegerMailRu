import requests
import json
from PIL import Image

def inputData(name):
    print('Введи %s:'%name)
    return input()

#файл откуда берется база логинов почт и паролей для реги
f = open('newitog.txt','r',encoding='utf-8')

for line in f:
    #нужно для разбиения твоей строки на имя почты и пароль для последующего использования в регистрации почты
    myemail = line.split(';')[0]
    mypass = line.split(';')[1][:-1]

    print(myemail+' с паролем '+mypass+'.')
    #myemail = inputData('имя почтового ящика')
    #mypass = inputData('пароль')

    link = 'https://account.mail.ru/api/v1/user/signup'
    datas = {'name':'{"first":"NAME","last":"FAMILY"}', 'from':'main', 'sex':'male', 'birthday':'{"day":24,"month":8,"year":1990}',
            'context':'signup',
            'browser':'{"screen":{"availWidth":"1600","availHeight":"860","width":"1600","height":"900","colorDepth":"24","pixelDepth":"24","availLeft":"0","availTop":"0"},"navigator":{"vendorSub":"","productSub":"20030107","vendor":"Google Inc.","maxTouchPoints":"0","hardwareConcurrency":"4","cookieEnabled":"true","appCodeName":"Mozilla","appName":"Netscape","appVersion":"5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36","platform":"Win32","product":"Gecko","userAgent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36","language":"ru","onLine":"true","doNotTrack":"inaccessible","deviceMemory":"4"},"flash":{"version":"inaccessible"}}',
            'device':'{"os":"","os_version":"","dtid":"","viewType":"0"}',
            'login':myemail,
            'domain':'mail.ru',
            'password':mypass,
            'htmlencoded':'false'}

    myreq = requests.Session()

    text = json.loads(myreq.post(link, data = datas).text)['body']

    print('Данные заполнены, воощем то.')

    urlcapcha = 'https://c.mail.ru/6?r=0.71848591092699836'
    mycapcha = myreq.get(urlcapcha)

    with open("img.jpg", 'wb') as f:
        f.write(mycapcha.content)

    img = Image.open('img.jpg')
    img.show()

    next = myreq.post('https://account.mail.ru/api/v1/user/signup/confirm', data= {'email':'%s@mail.ru'%myemail,
                                                                                      'from':'main',
                                                                                      'reg_anketa':('{"id":"%s","capcha":"%s"}' %(text, inputData('капчу'))),
                                                                                      'redirect_uri':'https://e.mail.ru/messages/inbox?newreg=1&signup_b=1&sms_reg=1&features=1',
                                                                                      'htmlencoded':'false'})

    print(next.text)
#print('usaly body id :' + text)
