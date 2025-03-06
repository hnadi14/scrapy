from selenium import webdriver
from selenium.webdriver.edge.service import Service
from bs4 import BeautifulSoup
import time

# تنظیمات مرورگر Edge
service = Service(executable_path=r"C:\Users\hn\Downloads\msgd\msedgedriver.exe")
driver = webdriver.Edge(service=service)

try:
    # باز کردن صفحه وب
    driver.get("https://www.aparat.com/")

    # انتظار تا صفحه کاملاً بارگذاری شود
    driver.implicitly_wait(10)


    # تابع برای اسکرول کردن صفحه
    def scroll_page(times):
        for _ in range(times):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # اسکرول به پایین صفحه
            time.sleep(2)  # انتظار برای بارگذاری محتوای جدید


    # اسکرول کردن صفحه سه بار
    scroll_page(20)

    # دریافت محتوای HTML صفحه پس از اسکرول
    page_source = driver.page_source

    # استفاده از BeautifulSoup برای پردازش HTML
    soup = BeautifulSoup(page_source, 'html.parser')

    # یافتن تمام ویدیوهای موجود در صفحه
    videos = soup.find_all('div', class_='grid-item')

    # لیستی برای ذخیره اطلاعات ویدیوها
    video_data = []

    # استخراج اطلاعات هر ویدیو
    for video_item in videos:
        # استخراج عنوان ویدیو

        title = video_item.find('span', class_='sc-jUosCB kCRgLS label-text').get_text(strip=True) if video_item.find(
            'span', class_='sc-jUosCB kCRgLS label-text') else "عنوان نامشخص"

        # استخراج تعداد بازدید
        views = video_item.find('span', class_='sc-hOGkXu dfjQYi caption meta-item').get_text(
            strip=True) if video_item.find('span',
                                           class_='sc-hOGkXu dfjQYi caption meta-item') else "تعداد بازدید نامشخص"

        # استخراج تاریخ آپلود (دومین عنصر با کلاس meta-item)
        upload_date = video_item.find_all('span', class_='sc-hOGkXu dfjQYi caption meta-item')[1].get_text(
            strip=True) if len(
            video_item.find_all('span', class_='sc-hOGkXu dfjQYi caption meta-item')) > 1 else "تاریخ آپلود نامشخص"

        # استخراج لینک ویدیو
        video_url = video_item.find('a', class_='link thumb video default')['href'] if video_item.find('a',
                                                                                                       class_='link thumb video default') else "لینک نامشخص"
        video_url = f"https://www.aparat.com{video_url}"  # اتصال لینک به URL پایه

        # ذخیره اطلاعات ویدیو در لیست
        video_data.append({
            'عنوان': title,
            'تعداد بازدید': views,
            'تاریخ آپلود': upload_date,
            'لینک ویدیو': video_url
        })

    # چاپ اطلاعات ویدیوها
    for idx, video in enumerate(video_data, start=1):
        print(f"ویدیو {idx}:")
        print(f"عنوان: {video['عنوان']}")
        print(f"تعداد بازدید: {video['تعداد بازدید']}")
        print(f"تاریخ آپلود: {video['تاریخ آپلود']}")
        print(f"لینک ویدیو: {video['لینک ویدیو']}")
        print("-" * 50)

finally:
    # بستن مرورگر
    driver.quit()