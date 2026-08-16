# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import csv
from collections import Counter
from datetime import datetime
from pathlib import Path


class PepParsePipeline:
    def open_spider(self, spider):
        self.statuses = Counter()
        self.total = 0

    def process_item(self, item, spider):
        self.statuses[item['status']] += 1
        self.total += 1
        return item

    def close_spider(self, spider):
        filename = (
            f'results/status_summary_'
            f'{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.csv'
        )

        with open(filename, 'w', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Статус', 'Количество'])
            for status, count in sorted(self.statuses.items()):
                writer.writerow([status, count])
            writer.writerow(['Total', self.total])
