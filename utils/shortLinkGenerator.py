import requests


def  generate_short_link(link:str=None):
    

    endpoint = 'https://clck.ru/--'

    response = requests.get(
        endpoint,
        params = {'url': link}
    )

    return response.text
    
if __name__ == '__main__':
    a = generate_short_link('https://www.api.com')
    
    print(a)