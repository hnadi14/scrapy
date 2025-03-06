import sqlite3

class SQLitePipeline:
    def open_spider(self, spider):
        self.connection = sqlite3.connect('aparat.db')
        self.cursor = self.connection.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS videos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                views TEXT,
                upload_date TEXT,
                video_url TEXT
            )
        ''')
        self.connection.commit()

    def process_item(self, item, spider):
        self.cursor.execute('''
            INSERT INTO videos (title, views, upload_date, video_url)
            VALUES (?, ?, ?, ?)
        ''', (
            item['title'],
            item['views'],
            item['upload_date'],
            item['video_url']
        ))
        self.connection.commit()
        return item

    def close_spider(self, spider):
        self.connection.close()