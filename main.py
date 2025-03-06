import sqlite3
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
import os
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



# تابع برای جستجوی ویدئو در پایگاه داده
def search_videos(keyword):
    connection = sqlite3.connect('aparat.db')
    cursor = connection.cursor()
    cursor.execute("SELECT id, title, chanel, video_url FROM videos WHERE title LIKE ? OR chanel LIKE ?", ('%' + keyword + '%', '%' + keyword + '%'))
    results = cursor.fetchall()
    connection.close()
    return results

# تابع برای دانلود ویدئو
def download_video(video_url):
    edge_options = Options()
    edge_options.use_chromium = True
    # edge_options.add_argument("--headless")
    edge_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    edgedriver_path = r"C:\Users\hn\Downloads\msgd\msedgedriver.exe"  # مسیر EdgeDriver
    service = Service(executable_path=edgedriver_path)
    driver = webdriver.Edge(service=service, options=edge_options)

    try:
        # اضافه کردن کوکی AuthV1 به مرورگر
        auth_cookie = {
            "name": "AuthV1",
            "value": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE3Mzg3Nzk3NDcsImFmY24iOiIxNzM2ODUwNDE2Njg0ODkiLCJzdWIiOiJCN0UyQkIzNi1EQjAxLTNFNDQtM0M3QS0yQUYxMzFGNjQ5NkYiLCJ0b2tlbiI6IjMwMDZmYTMxOGFiOWI5MDE3NzdmNzUwOWRkMGY0NTc3In0.iObbbcQqvE0Gt5HcorMfAyPBxlav1XBPKb4XGew7D2k",
            "domain": ".aparat.com",
            "path": "/",
            "secure": True,
            "httpOnly": True,
            "sameSite": "Lax",
            "expiry": 1778137352  # تاریخ انقضا به ثانیه تبدیل شده
        }
        driver.get(video_url)
        print(video_url)
        # ست کردن کوکی
        driver.add_cookie(auth_cookie)
        # باز کردن صفحه مجدد برای اعمال کوکی
        driver.refresh()
        time.sleep(5)

        print('a')
        # انتظار برای بارگذاری لیست کیفیت‌ها
        wait = WebDriverWait(driver, 60)
        # چاپ محتوای HTML صفحه
        print("Page Source:")
        print(driver.page_source)
        print('fffff')
        with open("page_source.html", "w", encoding="utf-8") as file:
            file.write(driver.page_source)
        print("Page source saved to 'page_source.html'")

        quality_list = wait.until(EC.presence_of_all_elements_located(
            (By.XPATH, '//*[@id="primary"]/div[2]/div[2]/div[2]/div[3]/div/div/div/li')))
        print(quality_list)


        # استخراج لیست کیفیت‌ها
        quality_items = driver.find_elements("xpath",
                                             '//*[@id="primary"]/div[2]/div[2]/div[2]/div[3]/div/div/div')

        print(quality_items)
        qualities = {}
        for item in quality_items:
            quality = item.find_element("css selector", 'span.label-text').text.strip()
            url = item.find_element("css selector", 'a.link').get_attribute('href')
            qualities[quality] = url

        if qualities:
            print("\nSelect a quality to download:")
            for i, quality in enumerate(qualities.keys(), 1):
                print(f"{i}. {quality}")

            choice = int(input("Enter the number of your choice: "))
            if 1 <= choice <= len(qualities):
                selected_quality = list(qualities.keys())[choice - 1]
                download_link = qualities[selected_quality]
                print(f"Downloading {selected_quality} version of the video...")
                os.system(f"start {download_link}")  # باز کردن لینک در مرورگر
            else:
                print("Invalid choice.")
        else:
            print("No download links found.")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.quit()

# اجرای سپایدر
def run_spider():
    process = CrawlerProcess(get_project_settings())
    process.crawl('aparat')  # نام سپایدر
    process.start()  # اجرای سپایدر

# اصلی
if __name__ == "__main__":
    # print("Starting Aparat Spider...")
    # run_spider()  # اجرای سپایدر

    # پس از اتمام سپایدر، دریافت ورودی از کاربر
    keyword = input("\nEnter a keyword to search for videos (title or channel): ").strip()
    videos = search_videos(keyword)

    if videos:
        print("\nSearch Results:")
        for i, video in enumerate(videos, 1):
            print(f"{i}. Title: {video[1]}, Channel: {video[2]}")

        choice = int(input("\nEnter the number of the video you want to download: "))
        if 1 <= choice <= len(videos):
            selected_video = videos[choice - 1]
            video_url = "https://www.aparat.com" + selected_video[3]
            download_video(video_url)
        else:
            print("Invalid choice.")
    else:
        print("No videos found matching your keyword.")