import schedule
import time
import subprocess

def job():
    try:
        subprocess.run(["scrapy", "runspider", "wikiSpider/spiders/newsmergeSpid.py", "-O", "news.json"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error ejecutando Scrapy: {e}")

# Ejecutar cada 2 días a la medianoche
schedule.every(2).days.at("09:45").do(job)

# test
# schedule.every(20).seconds.do(job)
print(schedule.jobs)
while True:
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    schedule.run_pending()
    time.sleep(1)