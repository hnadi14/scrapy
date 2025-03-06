import requests
from bs4 import BeautifulSoup
import re


def convert_to_number(text):
    """
    تبدیل متن قیمت به عدد.
    مثال: "۱,۸۷۰,۰۰۰ تومان" -> 1870000
    """
    # حذف کاراکترهای غیرعددی و جایگزینی کاما با خالی
    text = re.sub(r'[^\d]', '', text)
    try:
        return int(text)
    except ValueError:
        return None


def divar():
    m = 'گل'
    url = f'https://divar.ir/s/tehran?q={m}'
    response = requests.get(url)
    content = BeautifulSoup(response.text, 'html.parser')

    # یافتن تمام article‌ها
    articles = content.find_all('article', class_='kt-post-card kt-post-card--outlined kt-post-card--has-chat kt-post-card')

    for article in articles:
        # استخراج لینک آگهی
        link_element = article.find('a')
        if link_element:
            link = 'https://divar.ir' + link_element.get('href')
        else:
            link = 'Link not found'

        # استخراج عنوان
        title_element = article.find('h2', class_='kt-post-card__title')
        title = title_element.get_text(strip=True) if title_element else 'Title not found'

        location=article.find('span',class_='kt-post-card__bottom-description kt-text-truncate')
        location=location.get_text(strip=True) if location else 'sf'

        # استخراج توضیحات (اولین المان بعد از قیمت)
        description = 'Description not found'

        # استخراج قیمت (اولین المانی که شامل "تومان" است)
        price_element = None
        descriptions = article.find_all('div', class_='kt-post-card__description')
        for desc in descriptions:
            if 'تومان' in desc.get_text(strip=True):
                price_element = desc
                break
            else:
                description=desc.get_text(strip=True)

        if price_element:
            price_text = price_element.get_text(strip=True)
            price = convert_to_number(price_text)
        else:
            price_text = 'Price not found'
            price = None



        # چاپ اطلاعات
        print(f"Title: {title}")
        print(f"Price: {price} Toman ({price_text})")
        print(f"Description: {description}")
        print(f"Link: {link}")
        print(f"location: {location}")
        print("-" * 50)  # خط جدا کننده بین آگهی‌ها


if __name__ == "__main__":
    divar()