import requests
from bs4 import BeautifulSoup
import os
import json
import csv
from datetime import datetime

def get_all_pages():
    HEADERS = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 YaBrowser/21.8.3.614 Yowser/2.5 Safari/537.36'
    }

    r = requests.get(url = 'https://shop.casio.ru/catalog/g-shock/filter/gender-is-male/apply/')

    #Creating the "data" folder if it's not in the current directory
    if not os.path.isdir("data"):
        os.mkdir("data")
        print('\n' + '#' * 34)
        print('The folder "data" will be created!')
        print('#' * 34 + '\n')
    
    #Saving website page
    with open('data/index.html', 'w', encoding = 'utf-8') as file:
        file.write(r.text)

    with open('data/index.html', encoding = 'utf-8') as file:
        src = file.read()

    soup = BeautifulSoup(src, 'lxml')

    pages_count = int(soup.find('div', class_ = 'bx-pagination-container').find_all('a')[-2].text)
    
    for i in range(1, pages_count + 1):
        url = f'https://shop.casio.ru/catalog/g-shock/filter/gender-is-male/apply/?PAGEN_1={i}'
        
        r = requests.get(url = url, headers = HEADERS)

        #Saving watch pages
        with open(f'data/page_{i}.html', 'w', encoding = 'utf-8') as file:
            file.write(r.text)
    
    return pages_count + 1

def collect_data(pages_count):
    
    cur_date = datetime.now().strftime('%d_%m_%Y')

    #Saving table headers
    with open(f'data_{cur_date}.csv', 'w', newline = '') as file:
        writer = csv.writer(file, delimiter = ';')

        writer.writerow(
            (
                'Article',
                'Price',
                'Link'
            )
        )

    #Deleting an old files to avoid repeating old data
    if os.path.isfile(f'data_{cur_date}.json'):
        os.remove(f'data_{cur_date}.json')
        print('\n' + '#' * 53)
        print(f'The old file "data_{cur_date}.json" has been deleted!\nA new file will be created!')
        print('#' * 53 + '\n')
    else:
        print('\n' + '#' * 48)
        print(f'The file "data_{cur_date}.json" will be created!')
        print('#' * 48 + '\n')

    data = []
    for page in range(1, pages_count):
        with open(f'data/page_{page}.html', encoding = 'utf-8') as file:
            src = file.read()

        soup = BeautifulSoup(src, 'lxml')
        item_cards = soup.find_all('a', class_ = 'product-item__link')

        for item in item_cards:
            product_article = item.find('p', class_ = 'product-item__articul').text.strip()
            product_price = item.find('p', class_ = 'product-item__price').text.lstrip('руб. ')
            product_url = 'https://shop.casio.ru' + item.get('href')

            data.append(
                {
                    'product_article': product_article,
                    'product_price': product_price,
                    'product_url': product_url
                }
            )

            #Saving watches data to a csv format table
            with open(f'data_{cur_date}.csv', 'a', newline = '') as file:
                writer = csv.writer(file, delimiter =';')

                writer.writerow(
                    (
                        product_article,
                        product_price,
                        product_url
                    )
                )

        print(f'Обработана страница: {page}/{pages_count - 1}')
    
    #Saving watches data to a json file
    with open(f'data_{cur_date}.json', 'a', encoding = 'utf-8') as file:
        json.dump(data, file, indent = 4, ensure_ascii = False)

def main():
    pages_count = get_all_pages()
    collect_data(pages_count = pages_count)

if __name__ == '__main__':
    main()