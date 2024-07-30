import requests
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()

token = os.getenv('GITHUB_TOKEN')

if not token:
    raise ValueError("Token do GitHub não encontrado. Certifique-se de que o arquivo .env está configurado corretamente.")

url = 'https://api.github.com/user/repos'

params = {
    'visibility': 'all',  
    'affiliation': 'owner', 
    'per_page': 100 
}


headers = {
    'Authorization': f'token {token}'
}

response = requests.get(url, headers=headers, params=params)

repos_data = []

if response.status_code == 200:
    repos = response.json()
    for repo in repos:
        name = repo['name']
        size_kb = repo['size']
        size_mb = size_kb / 1024 
        private = repo['private']
        repos_data.append({
            'Repository': name,
            'Size (MB)': size_mb,
            'Private': private
        })
else:
    print(f'Failed to retrieve repositories: {response.status_code}')

df = pd.DataFrame(repos_data)

excel_file = 'github_data.xlsx'
df.to_excel(excel_file, index=False)

print(f'Dados exportados para {excel_file}')
