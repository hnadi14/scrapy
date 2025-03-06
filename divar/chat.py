from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
from bs4 import BeautifulSoup
import requests
import re


def convert_to_number(text):
    """
    تبدیل متن قیمت به عدد.
    مثال: "۱,۸۷۰,۰۰۰ تومان" -> 1870000
    """
    text = re.sub(r'[^\d]', '', text)
    try:
        return int(text)
    except ValueError:
        return None


def divar():
    m = 'گوشی'
    url = f'https://divar.ir/s/tehran?q={m}'
    response = requests.get(url)
    content = BeautifulSoup(response.text, 'html.parser')
    articles = content.find_all('article',
                                class_='kt-post-card kt-post-card--outlined kt-post-card--has-chat kt-post-card')

    # ذخیره اطلاعات آگهی‌ها
    listings = []
    for article in articles:
        link_element = article.find('a')
        if link_element:
            link = 'https://divar.ir' + link_element.get('href')
        else:
            link = 'Link not found'

        title_element = article.find('h2', class_='kt-post-card__title')
        title = title_element.get_text(strip=True) if title_element else 'Title not found'

        location = article.find('span', class_='kt-post-card__bottom-description kt-text-truncate')
        location = location.get_text(strip=True) if location else 'Location not found'

        price_element = None
        descriptions = article.find_all('div', class_='kt-post-card__description')
        for desc in descriptions:
            if 'تومان' in desc.get_text(strip=True):
                price_element = desc
                break

        if price_element:
            price_text = price_element.get_text(strip=True)
            price = convert_to_number(price_text)
        else:
            price_text = 'Price not found'
            price = None

        listings.append({
            'title': title,
            'price': price,
            'price_text': price_text,
            'link': link,
            'location': location
        })

    # نمایش لیست آگهی‌ها برای کاربر
    print("لیست آگهی‌ها:")
    for idx, listing in enumerate(listings):
        print(
            f"{idx + 1}. Title: {listing['title']}, Price: {listing['price']} Toman ({listing['price_text']}), Location: {listing['location']}")

    # انتخاب آگهی توسط کاربر
    choice = int(input("لطفاً شماره آگهی مورد نظر خود را وارد کنید: ")) - 1
    if 0 <= choice < len(listings):
        selected_listing = listings[choice]
        print(f"آگهی انتخابی: {selected_listing['title']}")
        print(f"باز کردن لینک: {selected_listing['link']}")

        # تنظیمات Selenium برای Edge
        edge_options = Options()
        edge_options.add_argument("--start-maximized")  # باز کردن مرورگر به حالت پرصفحه
        service = Service(executable_path="C:/Users/hn/Downloads/msgd/msedgedriver.exe")  # مسیر msedgedriver.exe
        driver = webdriver.Edge(service=service, options=edge_options)

        try:
            # باز کردن صفحه اصلی Divar (برای اضافه کردن کوکی)
            driver.get("https://divar.ir")
            time.sleep(2)  # انتظار برای بارگذاری صفحه

            # لیست کوکی‌ها
            cookies = [
                {
                    'name': 'token',
                    'value': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzaWQiOiIyMWQyZTk2Ny02MWVmLTQ1ZGMtYTcyNS03OWMzOWM4YTQ1YmIiLCJ1aWQiOiIzOTk3Yzc5MS00NWY2LTRjODQtOTZmNi1iYjMzMDI4NDhkOWIiLCJ1c2VyIjoiMDkzMzY2MzA1OTIiLCJ2ZXJpZmllZF90aW1lIjoxNzM5ODcxODkyLCJpc3MiOiJhdXRoIiwidXNlci10eXBlIjoicGVyc29uYWwiLCJ1c2VyLXR5cGUtZmEiOiLZvtmG2YQg2LTYrti124wiLCJleHAiOjE3NDI0NjM4OTIsImlhdCI6MTczOTg3MTg5Mn0.ZojUbvQNk7BJdbTSJYlR4GYUFvzQocJFydtKNBM8OKU',
                    'domain': '.divar.ir',
                    'path': '/',
                    'secure': True
                },
                {
                    'name': 'csid',
                    'value': '34184dbe03cf92dca5',
                    'domain': '.divar.ir',
                    'path': '/',
                    'secure': True
                },
                {
                    'name': 'did',
                    'value': '0c8ea058-701d-42f7-a4e1-c92e7193004f',
                    'domain': '.divar.ir',
                    'path': '/',
                    'secure': True
                }
            ]

            # اضافه کردن کوکی‌ها به مرورگر
            for cookie in cookies:
                driver.add_cookie(cookie)
            time.sleep(1)  # انتظار برای ثبت کوکی

            # بروزرسانی صفحه بعد از اضافه کردن کوکی‌ها
            driver.refresh()
            time.sleep(2)  # انتظار برای بارگذاری مجدد صفحه

            # باز کردن لینک انتخابی
            driver.get(selected_listing['link'])
            time.sleep(3)  # انتظار برای بارگذاری صفحه

            # یافتن دکمه و کلیک کردن روی آن
            button = driver.find_element(By.CSS_SELECTOR,
                                         "button.kt-button.kt-button--outlined.start-chat-button-e813e.start-chat-button--has-margin-a14e0")
            ActionChains(driver).move_to_element(button).click().perform()
            time.sleep(2)  # انتظار برای نمایش نتیجه

            print("چت با موفقیت شروع شد.")

            # یافتن textarea و نوشتن متن
            textarea = driver.find_element(By.CSS_SELECTOR, "textarea.kt-chat-input__input.kt-body--stable")

            off = selected_listing['price']*0.60
            textarea.send_keys(f"سلام و عرض ادب \n امکان دارد  {off}")  # متن را وارد کنید
            time.sleep(1)  # انتظار برای ثبت متن

            # یافتن دکمه ارسال و کلیک کردن روی آن
            send_button = driver.find_element(By.CSS_SELECTOR,
                                              "button.kt-button.kt-button--primary.kt-button--circular.kt-chat-input__button")
            send_button.click()
            time.sleep(2)  # انتظار برای ارسال پیام

            print("پیام با موفقیت ارسال شد.")
        except Exception as e:
            print(f"خطا: {e}")
        finally:
            driver.quit()  # بستن مرورگر
    else:
        print("شماره وارد شده معتبر نیست.")


if __name__ == "__main__":
    divar()
