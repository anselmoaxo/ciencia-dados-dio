# -*- coding: utf-8 -*-
"""SantanderDevWeek2023.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1NzrfLoyAlUjgCssMBhOWOJfArE-PCUf9

**`Extração dos Dados SDW2023 `**
"""

import pandas as pd
import openai

df = pd.read_csv('sdw2023.csv')
user_ids = df['UserID'].tolist()
print(user_ids)

import requests
import json



def get_user(id):
  api_url = "https://sdw-2023-prd.up.railway.app"
  response = requests.get(f'{api_url}/users/{id}')
  return response.json() if response.status_code == 200 else None

users = [user for id in user_ids if (user := get_user(id)) is not None]
print(json.dumps(users, indent=2))


"""**Tranformação dos Dados SDW2023**

Utilizando API do OpenAI , gerando um mesnagem de Marketing
"""
openai_api_key = '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'
openai.api_key = openai_api_key

def generate_ai_news(user):
  completion = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
      {
          "role": "system",
          "content": "Você é um especialista em markting bancário."
      },
      {
          "role": "user",
          "content": f"Crie uma mensagem para {user['name']} sobre a importância dos investimentos (máximo de 100 caracteres)"
      }
    ]
  )
  return completion.choices[0].message.content.strip('\"')

for user in users:
  news = generate_ai_news(user)
  print(news)
  user['news'].append({
      "icon": "https://digitalinnovationone.github.io/santander-dev-week-2023-api/icons/credit.svg",
      "description": news
  })



"""**LOAD dos Dados SDW2023**"""

def update_user(user):
  response = requests.put(f"{api_url}/users/{user['id']}", json=user)
  return True if response.status_code == 200 else False

for user in users:
  success = update_user(user)
  print(f"User {user['name']} updated? {success}!")