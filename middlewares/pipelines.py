import sqlite3

class SQLitePipeline:
    def open_spider(self, spider):
        self.connection = sqlite3.connect('aparat.db')
        self.cursor = self.connection.cursor()
        # ایجاد جدول با محدودیت UNIQUE برای video_url
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS videos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                chanel TEXT,
                views TEXT,
                upload_date TEXT,
                video_url TEXT UNIQUE,
                duration TEXT
            )
        ''')
        self.connection.commit()

    def process_item(self, item, spider):
        try:
            # استفاده از INSERT OR IGNORE برای جلوگیری از تکرار
            self.cursor.execute('''
                INSERT OR IGNORE INTO videos (title, chanel, views, upload_date, video_url, duration)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                item.get('title', 'N/A'),
                item.get('chanel', 'N/A'),
                item.get('views', 'N/A'),
                item.get('upload_date', 'N/A'),
                item.get('video_url', 'N/A'),
                item.get('duration', 'N/A'),
            ))
            self.connection.commit()


        except Exception as e:
            spider.logger.error(f"Database error: {e}")
        return item

    def close_spider(self, spider):
        self.connection.close()