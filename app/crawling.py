from bs4 import BeautifulSoup
import requests, re

from items.models import Item, Category

col_ga_id = []
col_company = []
col_item_name = []
col_sales_price = []
col_origin_price = []
col_discounts = []

col_page = []

p_company = re.compile(r'\[(?P<company>.*)\](?P<item_name>.*)')
p_price = re.compile(r'\d.*\d')

col_category = [
    # 밑반찬
    '46010000',
    # 메인반찬
    '46030000',
    # 국찌개탕
    '46060000',
    # 아이반찬
    '46070000',
    # 육류
    '46100000',
    # 김치장아찌
    '46020000',
    # 세계음식
    '46040000',
    # 밥죽면
    '46050000',
    # 샐러드
    '46080000',
    # 간식
    '46120000',
    # 정기식단
    '46110000',
]

col_url = [
    'https://www.baeminchan.com/sidedish/list.php',
    'https://www.baeminchan.com/maindish/list.php',
    'https://www.baeminchan.com/soups/list.php',
    'https://www.baeminchan.com/forkids/list.php',
    'https://www.baeminchan.com/meat/list.php',
    'https://www.baeminchan.com/pickles/list.php',
    'https://www.baeminchan.com/foreign/list.php',
    'https://www.baeminchan.com/rice-noodle/list.php',
    'https://www.baeminchan.com/salad/list.php',
    'https://www.baeminchan.com/snack/list.php',
    'https://www.baeminchan.com/mealplan/list.php',
]

for col in col_url:
    response = requests.get(col)
    soup = BeautifulSoup(response.text, 'lxml')
    try:
        soup.find('div', 'pagination').findAll('a')
    except:
        col_page.append(0)
    else:
        col_page.append(len(soup.find('div', 'pagination').findAll('a')) - 1)

cnt = 0

for cnt in range(0, 11):
    col_url_page = []

    if col_page[cnt] == 0:
        col_url_page.append(col_url[cnt])
    else:
        for num in range(1, col_page[cnt] + 1):
            col_url_page.append(col_url[cnt] + '?' + 'cno=' + str(col_category[cnt]) + '&' + 'page=' + str(num))

    for url in col_url_page:
        print(url)
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        soup_products = soup.find('ul', id='products')
        col_products = []
        col_products = soup_products.findAll('li')
        col_imgthumb = []
        col_imgthumb = soup_products.find_all("div", "imgthumb")

        for col in col_products:
            col_ga_id.append(col.select('a')[0].get('ga_id'))
            col_company.append(p_company.search(col.select('a')[0].get('ga_name')).group('company'))
            col_item_name.append(p_company.search(col.select('a')[0].get('ga_name')).group('item_name').lstrip())

        for col in col_products:
            try:
                p_price.search(col.select('p')[0].get_text()).group()
            except:
                col_sales_price.append(0)
            else:
                col_sales_price.append(int(p_price.search(col.select('p')[0].get_text()).group().replace(',', '')))

        for col in col_products:
            try:
                p_price.search(col.select('p')[1].get_text()).group()
            except IndexError:
                try:
                    p_price.search(col.select('p')[0].get_text()).group().replace(',', '')
                except:
                    col_origin_price.append(0)
                else:
                    col_origin_price.append(p_price.search(col.select('p')[0].get_text()).group().replace(',', ''))
            else:
                col_origin_price.append(p_price.search(col.select('p')[1].get_text()).group().replace(',', ''))

        for col in col_imgthumb:
            try:
                col.select('span')[0].get_text()
            except IndexError:
                col_discounts.append(float(0))
            else:
                col_discounts.append(float(col.select('span')[0].get_text()) * 0.01)

Item.objects.all().delete()

item_cnt = 1

for item_cnt in range(item_cnt, len(col_item_name)):
    try:
        Item.objects.create(pk=item_cnt, item_name=col_item_name[item_cnt - 1], company=col_company[item_cnt - 1],
                            origin_price=col_origin_price[item_cnt - 1], sale_price=col_sales_price[item_cnt - 1],
                            discount_rate=col_discounts[item_cnt - 1], ga_id=col_ga_id[item_cnt - 1])
    except:
        pass

col_category = [
    'https://www.baeminchan.com/sidedish/list.php?cno=46010000',
    'https://www.baeminchan.com/sidedish/list.php?cno=46010100',
    'https://www.baeminchan.com/sidedish/list.php?cno=46010200',
    'https://www.baeminchan.com/sidedish/list.php?cno=46010300',
    'https://www.baeminchan.com/sidedish/list.php?cno=46010400',
    'https://www.baeminchan.com/sidedish/list.php?cno=46010600',
    'https://www.baeminchan.com/sidedish/list.php?cno=46010700',
    'https://www.baeminchan.com/maindish/list.php?cno=46030000',
    'https://www.baeminchan.com/maindish/list.php?cno=46030100',
    'https://www.baeminchan.com/maindish/list.php?cno=46030200',
    'https://www.baeminchan.com/maindish/list.php?cno=46030300',
    'https://www.baeminchan.com/maindish/list.php?cno=46030400',
    'https://www.baeminchan.com/maindish/list.php?cno=46030500',
    'https://www.baeminchan.com/maindish/list.php?cno=46030600',
    'https://www.baeminchan.com/soups/list.php?cno=46060000',
    'https://www.baeminchan.com/soups/list.php?cno=46060100',
    'https://www.baeminchan.com/soups/list.php?cno=46060200',
    'https://www.baeminchan.com/soups/list.php?cno=46060300',
    'https://www.baeminchan.com/soups/list.php?cno=46060400',
    'https://www.baeminchan.com/soups/list.php?cno=46060500',
    'https://www.baeminchan.com/forkids/list.php?cno=46070000',
    'https://www.baeminchan.com/forkids/list.php?cno=46070100',
    'https://www.baeminchan.com/forkids/list.php?cno=46070200',
    'https://www.baeminchan.com/forkids/list.php?cno=46070300',
    'https://www.baeminchan.com/forkids/list.php?cno=46070400',
    'https://www.baeminchan.com/meat/list.php?cno=46100000',
    'https://www.baeminchan.com/meat/list.php?cno=46100100',
    'https://www.baeminchan.com/meat/list.php?cno=46100200',
    'https://www.baeminchan.com/meat/list.php?cno=46100300',
    'https://www.baeminchan.com/meat/list.php?cno=46100400',
    'https://www.baeminchan.com/meat/list.php?cno=46100700',
    'https://www.baeminchan.com/meat/list.php?cno=46100500',
    'https://www.baeminchan.com/pickles/list.php?cno=46020000',
    'https://www.baeminchan.com/pickles/list.php?cno=46020100',
    'https://www.baeminchan.com/pickles/list.php?cno=46020200',
    'https://www.baeminchan.com/foreign/list.php?cno=46040000',
    'https://www.baeminchan.com/foreign/list.php?cno=46040100',
    'https://www.baeminchan.com/foreign/list.php?cno=46040200',
    'https://www.baeminchan.com/rice-noodle/list.php?cno=46050000',
    'https://www.baeminchan.com/rice-noodle/list.php?cno=46050100',
    'https://www.baeminchan.com/rice-noodle/list.php?cno=46050200',
    'https://www.baeminchan.com/rice-noodle/list.php?cno=46050300',
    'https://www.baeminchan.com/salad/list.php?cno=46080000',
    'https://www.baeminchan.com/salad/list.php?cno=46080100',
    'https://www.baeminchan.com/salad/list.php?cno=46080200',
    'https://www.baeminchan.com/snack/list.php?cno=46120000',
    'https://www.baeminchan.com/snack/list.php?cno=46120100',
    'https://www.baeminchan.com/snack/list.php?cno=46120200',
    'https://www.baeminchan.com/snack/list.php?cno=46120300',
    'https://www.baeminchan.com/snack/list.php?cno=46120400',
    'https://www.baeminchan.com/snack/list.php?cno=46120500',
    'https://www.baeminchan.com/snack/list.php?cno=46120600',
    'https://www.baeminchan.com/mealplan/list.php?cno=46110000',
    'https://www.baeminchan.com/mealplan/list.php?cno=46110100',
    'https://www.baeminchan.com/mealplan/list.php?cno=46110200',
    'https://www.baeminchan.com/mealplan/list.php?cno=46110300',
]

item_cnt = 1

for item_cnt in range(item_cnt, len(col_item_name)):
    try:
        Item.objects.create(pk=item_cnt, item_name=col_item_name[item_cnt - 1], company=col_company[item_cnt - 1],
                            origin_price=col_origin_price[item_cnt - 1], sale_price=col_sales_price[item_cnt - 1],
                            discount_rate=col_discounts[item_cnt - 1], ga_id=col_ga_id[item_cnt - 1])
    except:
        pass

col_page_category = []
col_category_ga_id = []
category_cnt = 1

for col in col_category:
    response = requests.get(col)
    soup = BeautifulSoup(response.text, 'lxml')

    max_page = 0

    try:
        soup.find('div', 'pagination').findAll('a')
    except:
        max_page = 0
    else:
        max_page = len(soup.find('div', 'pagination').findAll('a')) - 1

    col_url_page = []

    if max_page == 0:
        col_url_page.append(col)
    else:
        for num in range(1, max_page + 1):
            col_url_page.append(col + '&' + 'page=' + str(num))

    for url in col_url_page:
        print(url)
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        soup_products = soup.find('ul', id='products')
        col_products = []
        col_products = soup_products.findAll('li')

        for col in col_products:
            ga_id = col.select('a')[0].get('ga_id')
            try:
                Item.objects.get(ga_id=ga_id).categories.add(Category.objects.get(pk=category_cnt))
            except:
                pass

    print('----------------------------' + str(category_cnt) + '----------------------------------')
    category_cnt += 1
