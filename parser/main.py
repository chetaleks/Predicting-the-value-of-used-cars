import requests, json
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from config import DICT_HEADERS, MARKS, PARAMS, URL, PARSED_MARKS
import os
import time
import random


def get_models_for_mark(response):
    response.encoding = 'utf-8'

    html = response.text
    soup = BeautifulSoup(html, 'lxml') 
    items = soup.find_all('div', class_='ListingPopularMMM__item')
    result = [] 

    for item in items:
      link = item.find('a', class_='ListingPopularMMM__itemName')
      if link:
          url_path = urlparse(link['href']).path
          model_url = url_path.split('/')[4]
          
          model_name = link.text.strip()

          count = item.find('div', class_='ListingPopularMMM__itemCount').text.strip() 
          count = int(count) if count else 0

          result.append({
              'url_model': model_url,
              'model_name': model_name,
              'url': link['href'],
              'count': count
          }) 
    return  result     

def get_data_for_model(mark, model=None):
    mark_upper = mark.upper()
    PARAMS["catalog_filter"] = {"mark": mark_upper}
    model_name = mark_upper

    if model is not None:
        url_model = model["url_model"].upper() # название из ссылки
        model_name = model["model_name"].upper()
        model_count = model["count"]
        PARAMS["catalog_filter"]["model"] = url_model

    directory = os.path.join("data", mark_upper, model_name)
    os.makedirs(directory, exist_ok=True)

    page_count = 0

    time.sleep(random.uniform(1, 3))
    try:
      response = requests.post(URL, json=PARAMS, headers = DICT_HEADERS)
      response.raise_for_status()
    except requests.exceptions.HTTPError as http_err:
        print("HTTP ошибка:", http_err)
    except requests.exceptions.ConnectionError as conn_err:
        print("Ошибка соединения:", conn_err)
    except requests.exceptions.Timeout as timeout_err:
        print("Ошибка таймаута:", timeout_err)
    except requests.exceptions.RequestException as req_err:
        print("Произошла непредвиденная ошибка:", req_err)
    else:
        print("Запрос выполнен успешно")

    print(response.status_code)
    print(mark_upper)
    print(model_name)
    
    page_count = response.json()["pagination"]["total_page_count"]
    index = 1
    for p in range(1, page_count + 1):
      PARAMS["page"] = p
      time.sleep(random.uniform(1, 2))
      try:
        response = requests.post(URL, json=PARAMS, headers = DICT_HEADERS)
        response.raise_for_status()
      except requests.exceptions.HTTPError as http_err:
          print("HTTP ошибка:", http_err)
      except requests.exceptions.ConnectionError as conn_err:
          print("Ошибка соединения:", conn_err)
      except requests.exceptions.Timeout as timeout_err:
          print("Ошибка таймаута:", timeout_err)
      except requests.exceptions.RequestException as req_err:
          print("Произошла непредвиденная ошибка:", req_err)
      else:
          print("Запрос выполнен успешно")
          
      print(response.status_code)
      print(mark_upper)
      print(model_name)

      offers = response.json()["offers"]
    

      for offer in offers:
        file_path = os.path.join(directory, f"offer_{index}.json")
        with open(file_path, "w", encoding="utf-8") as file:
              json.dump(offer, file, ensure_ascii=False, indent=4)
        index += 1      



for mark in MARKS:
    
    if mark in PARSED_MARKS:
       continue
    
    mark_url = f"https://auto.ru/rossiya/cars/{mark}/all/"

    time.sleep(random.uniform(1, 2))

    mark_response = requests.get(mark_url)
    models = get_models_for_mark(mark_response)

    if not models:
      get_data_for_model(mark)
      continue

    for model in models:
        get_data_for_model(mark, model)