import requests
from bs4 import BeautifulSoup
import json
import csv


class ShahreKhabarScraper:
    def __init__(self, subject, start_page=1, end_page=1, save_option=''):
        """
        ایجاد یک ابزار برای استخراج اخبار از سایت شاهر خبر.
        :param subject: موضوع خبر (مثال: 'اقتصاد')
        :param start_page: شماره صفحه شروع (پیش‌فرض: 1)
        :param end_page: شماره صفحه پایان (پیش‌فرض: 1)
        """
        self.subject = subject
        self.start_page = start_page
        self.end_page = end_page
        self.news_content = []
        self.save_option=save_option

    def start(self):
        # ایجاد نمونه از کلاس
        # scraper = ShahreKhabarScraper(self.subject, self.start_page, self.end_page)
        # استخراج اخبار
        self.fetch_news()
        # نمایش اخبار
        self.display_news()

        # ذخیره اطلاعات
        if self.save_option.lower() == 'json':
            self.save_to_json()
        elif self.save_option.lower() == 'csv':
            self.save_to_csv()

    def fetch_news(self):
        """
        استخراج اخبار از صفحات مشخص‌شده.
        """
        for page_number in range(self.start_page, self.end_page + 1):
            try:
                # ساخت URL صفحه فعلی
                url = f'https://www.shahrekhabar.com/tag/{self.subject}?page={page_number}'
                print(url)
                print(f"در حال دریافت صفحه {page_number}...")

                # دریافت صفحه وب
                response = requests.get(url, timeout=10)  # Timeout برای جلوگیری از توقف برنامه
                response.raise_for_status()  # بررسی وضعیت درخواست

                # پردازش HTML
                content = BeautifulSoup(response.text, 'html.parser')
                self.parse_news(content)

            except requests.exceptions.RequestException as e:
                print(f"خطای دریافت صفحه {page_number}: {e}")
                continue

    def parse_news(self, content):
        """
        پردازش محتوای HTML و استخراج اطلاعات اخبار.

        :param content: محتوای HTML پارس‌شده
        """
        news_list = content.select('ul.news-list-items')
        if not news_list:
            print("هیچ لیست خبری پیدا نشد.")
            return

        for ul in news_list:
            for li in ul.find_all('li'):
                try:
                    title = li.find('a').text.strip().replace('\u200c', ' ').replace('\u200d', '') if li.find(
                        'a') else "عنوان نامشخص"
                    link = li.find('a').get('href') if li.find('a') else "#"
                    source = li.find('span').getText(strip=True),
                    time = li.find('span').find_next_sibling('span').getText(strip=True),

                    # اضافه کردن اطلاعات خبر به لیست
                    news_item = {
                        'عنوان': title,
                        'لینک': link,
                        'منبع': source,
                        'زمان': time,
                    }
                    self.news_content.append(news_item)

                except Exception as e:
                    print(f"خطای پردازش خبر: {e}")
                    continue

    def save_to_json(self, file_name='shahrekhabar_data.json'):
        """
        ذخیره اطلاعات استخراج‌شده در فایل JSON.
        :param file_name: نام فایل JSON (پیش‌فرض: 'shahrekhabar_data.json')
        """
        if not self.news_content:
            print("هیچ خبری استخراج نشده است.")
            return

        try:
            with open(file_name, 'w', encoding='utf-8') as json_file:
                json.dump(self.news_content, json_file, ensure_ascii=False, indent=4)
            print(f"اطلاعات در فایل {file_name} ذخیره شد.")
        except Exception as e:
            print(f"خطای ذخیره در فایل JSON: {e}")

    def save_to_csv(self, file_name='shahrekhabar_data.csv'):
        """
        ذخیره اطلاعات استخراج‌شده در فایل CSV.

        :param file_name: نام فایل CSV (پیش‌فرض: 'shahrekhabar_data.csv')
        """
        if not self.news_content:
            print("هیچ خبری استخراج نشده است.")
            return

        try:
            headers = list(self.news_content[0].keys())  # استخراج سربرگ‌ها از اولین خبر
            with open(file_name, 'w', newline='', encoding='utf-8') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=headers)
                writer.writeheader()
                writer.writerows(self.news_content)
            print(f"اطلاعات در فایل {file_name} ذخیره شد.")
        except Exception as e:
            print(f"خطای ذخیره در فایل CSV: {e}")

    def display_news(self):
        """
        نمایش اخبار استخراج‌شده در کنسول.
        """
        if not self.news_content:
            print("هیچ خبری استخراج نشده است.")
            return

        print("\n=== اخبار استخTRACT‌شده ===")
        for idx, item in enumerate(self.news_content, 1):
            print(f"\nخبر {idx}:")
            print(f"عنوان: {item['عنوان']}")
            print(f"لینک: {item['لینک']}")
            print(f"منبع: {item['منبع']}")
            print(f"زمان: {item['زمان']}")

    def get_full_news(self, url):
        """
        استخراج متن کامل خبر از لینک داده‌شده.

        :param url: آدرس خبر
        :return: متن کامل خبر
        """
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            full_text = soup.select_one('div.news-content').text.strip() if soup.select_one(
                'div.news-content') else "متن خبر ناموجود است."
            return full_text[:100] + "..." if len(full_text) > 100 else full_text
        except Exception as e:
            print(f"خطای استخراج متن خبر: {e}")
            return "خطای استخراج متن"
