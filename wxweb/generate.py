from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import os

code='utf-8'

def sanitize_filename(filename):
    import re
    illegal_chars = r'[\\/:*?"<>|\x00-\x1f]'
    sanitized = re.sub(illegal_chars, '', filename)
    return sanitized.strip().strip('.')

def get_current_date():
  import datetime
  today_date = datetime.date.today()
  now = datetime.datetime.now()
  formatted_date = now.strftime("%Y-%m-%d")
  return formatted_date 


def timestamp_string_to_datetime(date):
    import datetime
    return datetime.datetime.fromtimestamp(int(date))

def get_md5(string):
  import hashlib
  md5_object = hashlib.md5()
  md5_object.update(string.encode(code))  # 确保字符串以字节形式传入
  return md5_object.hexdigest()

def change_sort_to_latest(driver):
    """将搜索结果排序改为'最新'"""
    try:
        # 点击排序下拉菜单
        sort_dropdown = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "select"))
        )
        sort_dropdown.click()

        ## 选择"最新"排序选项
        latest_option = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//li[text()='最新']"))
        )
        latest_option.click()

        # 等待排序完成
        time.sleep(3)
        print("已按'最新'排序")
        return True
    except Exception as e:
        print(f"排序失败: {e}")
        return False

def extract_article_content(driver, url):
    # 打开文章页面
    driver.get(url)

    is_timeout = False
    try:
      WebDriverWait(driver, 5).until(
          EC.presence_of_element_located((By.ID, "js_content"))
      )
    except:
      print("timeout")
      is_timeout = True

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    if is_timeout:
      time.sleep(5)
      wanning_msg = soup.find('div', class_='weui-msg__title warn')
      if wanning_msg is not None:
        print("has wanning:",wanning_msg.get_text(strip=True)
        return None
      else:
        import time
        time.sleep(10)
        return -1

    title = soup.find('h1', class_='rich_media_title').get_text(strip=True)

    content_div = soup.find('div', id='js_content')
    content = ""
    import re
    for p in content_div.find_all(name=re.compile('p|span')):
        text = p.get_text(strip=True)
        if text:
            content += text + "\n\n"
    for img in content_div.find_all('img', class_='rich_pages'):
        if 'data-src' in img.attrs:
            content += f"[图片: {img['data-src']}]\n\n"

    article_info = {}
    account_info = {}

    return {
        "title": title,
        "content": content,
    }


def get_links(driver, account_name):
    driver.get("https://weixin.sogou.com/")
    search_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "query"))
    )
    search_input.send_keys(f"\"{account_name}\"")  # 替换为目标公众号
    article = driver.find_element(By.XPATH, "//input[@value='搜文章']").click()  # 点击“搜文章”

    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, "news-list"))
    )
    #change_sort_to_latest(driver)

    links = []
    for page in range(10):
      articles = driver.find_elements(By.XPATH, "//li[contains(@id, 'sogou_vr_11002601_box')]")
      if len(articles) == 0:
        i = 0
        articles = []
        while True:
          a = driver.find_elements(By.XPATH, f"//li[contains(@id, 'sogou_vr_11002601_box_{i}')]")
          if a is None or len(a) == 0:
            break
          i=i+1
          articles = articles + a
      #print(f"article {len(articles)}")
      import sys
      sys.stdout.flush()
      for article in articles:
          title = article.find_element(By.XPATH, ".//h3/a").text
          author = article.find_element(By.XPATH, ".//div[@class='s-p']/span[1]").text
          date = article.find_element(By.XPATH, ".//div[@class='s-p']/span[@class='s2']/script").get_attribute("innerHTML")
       
          date=date.split("timeConvert")[1][2:-3]
          publish_date = timestamp_string_to_datetime(date)
          if author != account_name:
            #print(f"author {author} need {account_name}")
            continue
          link = article.find_element(By.XPATH, ".//h3/a").get_attribute("href")
          print(f"标题: {title}\n作者: {author}\n链接: {link}\n")
          links.append((title, link, str(publish_date).split()[0]))
      # 翻页到下一页
      try:
          next_btn = driver.find_element(By.ID, "sogou_next")
          if next_btn.is_enabled():
              next_btn.click()
              print("正在翻页...")
              # 等待页面刷新
              WebDriverWait(driver, 15).until(
                  EC.staleness_of(articles[0])
              )
              # 等待新页面加载
              WebDriverWait(driver, 15).until(
                  EC.presence_of_element_located((By.CLASS_NAME, "news-list"))
              )
      except Exception as e:
          print(f"翻页失败: {str(e)}")
          break 
    return links


def read_links(account):
  import json
  import os
  import time
  dir_name = f"{account}/文章"
  ret = 0
  if not os.path.exists(dir_name):
    os.makedirs(dir_name)
  driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

  try:
    while True:
      links = get_links(driver, account)
      #print("get links:",len(links))
      if len(links) == 0:
        time.sleep(5)
        driver.quit()
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        continue
      break

    for title, url, date in links:
      today = date
      title = sanitize_filename(title)
      file_name = f"./{account}/文章/{account}_{today}_{title}.txt"
      print("file name:",file_name)
      if os.path.exists(file_name):
        print(f"{file_name} exist")
        continue
      res = extract_article_content(driver, url)
      if res is None:
        continue
      with open(file_name, "w", encoding='utf-8') as f:
        json.dump(res, f, ensure_ascii=False, indent=4)
      #print(f"{url}, res:{res}")
  except Exception as e:
    print("error:",e)
    ret = -1
  finally:
    driver.quit()
    pass

  return ret

def get_summary(account):
  import json
  import summary
  for file in os.listdir(f"{account}/文章"):
    summary_dir = f"{account}/概括"
    file_name = f"{account}/文章/{file}"
    summary_file_name = f"{summary_dir}/{file}"

    if not os.path.exists(summary_dir):
      os.makedirs(summary_dir)

    with open(file_name,"r", encoding='utf-8') as f:
      js = json.load(f)
      title = js["title"]
      content =  js["content"]
      reduced_content = ""
      for p in content.split("\n"):
        if p.find("https") >=0:
          pass
        else:
          if len(p) > 5:
            reduced_content += p + "\n" 
      #print("reduced:",reduced_content)
      content_summary = summary.textrank_summary(reduced_content, 10)
      #print(f"summary {content_summary}")
      with open(summary_file_name,"w", encoding='utf-8') as f:
        f.write("title:"+title+"\n"+"\n")
        f.write(content_summary)

if __name__ == '__main__':
  with open("account_name.txt", "r", encoding='gbk') as f:
    for account in f.readlines():
      account = account.strip()
      if(len(account) == 0):
        continue
      print("read account:",account)
      while True:
        res = read_links(account)
        print("read link res:",res)
        if res != 0:
          import time
          time.sleep(10)
        else:
          break
      get_summary(account)
