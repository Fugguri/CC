import requests


def  generate_short_link(link:str=None):
    

    url = 'https://goo.su/api/links/create'
    
    headers = {'x-goo-api-token': 'rdkMdWoSHbWx3DNQoaWMBqxF7qLiNWQ4XkBT1jwGP9EXiRIGcvvM4CWdHNRf',
               'content-type': 'application/json'}
    data ={
        'url':link
        }
    result = requests.post(url=url,headers=headers,data=data)
    result = requests.get(url="https://goo.su/api/links",headers=headers,data=data)

    return result
if __name__ == '__main__':
    a = generate_short_link('https://www.api.com')
    
    print(a)