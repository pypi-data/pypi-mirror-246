import re
import requests
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def generate_api_url(query, searchToken):
    base_url = "https://www.sciencedirect.com/search/api"
    params = {
        'qs': query,
        't': searchToken,
        'hostname': "www.sciencedirect.com"
    }
    return requests.Request('GET', base_url, params=params).prepare().url

def fetch_publication_data(query):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        }

        with requests.get('https://www.sciencedirect.com/search?qs=', headers=headers) as response:
            searchToken = re.search(r'"searchToken":"(.*?)"', response.content.decode()).group(1)


        url = generate_api_url(query, searchToken)

        with requests.get(url, headers=headers) as response:
            if response.status_code == 200:
                data = response.json()

                publication_counts = {year['key']: year['value'] for year in data['facets']['years']}

                return dict(sorted(publication_counts.items()))
    except:
        raise Exception("Failed to request to ScienceDirect API")


def plot_publication_trends(query, file_path, title):
    publication_counts = fetch_publication_data(query)
    years = list(publication_counts.keys())
    counts = list(publication_counts.values())

    normalized_counts = (counts - np.min(counts)) / (np.max(counts) - np.min(counts))

    sns.set_style("whitegrid")

    plt.figure(figsize=(12, 6))
    bars = plt.bar(years, counts)

    for bar, norm_value in zip(bars, normalized_counts):
        bar.set_color(plt.cm.viridis(norm_value))

    plt.xlabel('Year', fontsize=12)
    plt.ylabel('Number of Publications', fontsize=12)
    plt.title(title, fontsize=14)
    plt.xticks(rotation=45, fontsize=10)
    plt.yticks(fontsize=10)
    plt.tight_layout()

    plt.savefig(file_path)
    plt.close()