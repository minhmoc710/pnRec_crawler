import os
import time
try:
    while True:
        os.system("scrapy crawl update_periodically")
        time.sleep(600)
except KeyboardInterrupt:
    print("Crawler stopped becaused of Keyboard Interuption")
