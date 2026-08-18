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
        feed_path = next(iter(spider.settings['FEEDS']))

        results_dir = Path(feed_path).parent
        results_dir.mkdir(parents=True, exist_ok=True)
        filename = (
            'status_summary_'
            f'{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.csv'
        )
        filepath = results_dir / filename
        with open(filepath, 'w', encoding='utf-8', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Статус', 'Количество'])
            rows = [
                [status, count]
                for status, count in sorted(self.statuses.items())
            ]
            rows.append(["Total", self.total])
            writer.writerows(rows)
