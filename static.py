import requests
from bs4 import BeautifulSoup
import json
url = "https://www.ptt.cc/bbs/nba/index.html"

# 'User-Agent'
# 模仿 使用者
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

# 找出 ptt nba 裡面的 人氣、日期、文章標題
articles = soup.find_all("div", class_="r-ent")

# 儲存資料的位置
datalist = []
# 使用 for loop 避免掉被刪除的文章
for a in articles:
  data = {}
  scope = a.find("div", class_="title")
  if scope and scope.a: # 檢查是否有標題
    scope = scope.a.text
  else:
    scope = "No Content!"
  data["scope"] = scope

# 找出人氣
  popularity = a.find("div", class_="nrec")
  if popularity and popularity.span:
    popularity = popularity.span.text
  else:
    popularity = "N/A"
  data["popularity"] = popularity

  # 找出日期
  establish_date = a.find("div", class_="date")
  if establish_date:
    establish_date = establish_date.text
  else:
    establish_date = "N/A"
  data["establish_date"] = establish_date

  # 儲存資料
  datalist.append(data)
with open("static.json","w", encoding = "utf-8") as file:
  json.dump(datalist, file, ensure_ascii=False, indent=4)
print("Saved Successfully!")