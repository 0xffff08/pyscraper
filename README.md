# 🐍 pyscraper

A lightweight Python scraper that collects tweets using [Nitter](https://nitter.net) and stores them in structured `.csv` files.  
Powered by [Scrapfly](https://scrapfly.io), this project allows you to automate tweet collection with search terms, date filters, and pagination support.

---

## 📦 Features

- ✅ Collect tweets from **Nitter** (a free and private front-end for Twitter)
- ✅ Save tweets incrementally (`tweets_raw.csv`) and without duplicates (`tweets.csv`)
- ✅ Supports **pagination** through the "Load more" button
- ✅ Fully asynchronous for speed and efficiency
- ✅ Customize search with `since:` and `until:` date filters
- ✅ It is also possible to customize the number of pages loaded through "Load more", by changing the function call parameter, in the line: `await scrape_load_more(url, all_tweets, max_load_more=<num_pages>)`. The default value is 50 pages.

---

## ⚙️ Requirements

- Python 3.7+
- Scrapfly API Key (get yours at https://scrapfly.io)

---

## 🚀 Installation

```bash
# Clone the repository
git clone https://github.com/0xffff08/pyscraper.git
cd pyscraper

# (Optional) Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # For Linux/macOS
venv\Scripts\activate     # For Windows

# Install dependencies
pip install -r requirements.txt
```

---

## 🔑 Scrapfly Setup

1. Create a free account at: https://scrapfly.io  
2. Copy your API key  
3. Open the `pyscraper.py` file and update the line:

```python
SCRAPFLY = ScrapflyClient(key="API_KEY_HERE")
```

Replace `"API_KEY_HERE"` with your actual key.

---

## 🧪 How to Use

```bash
# Edit the search term at the bottom of pyscraper.py:
# Example:
termo_de_busca = "INSS Lula since:2025-04-23 until:2025-04-30"

# Then run the script
python pyscraper.py
```

After execution, two files will be generated:

- `tweets_raw.csv`: all tweets, including duplicates
- `tweets.csv`: filtered tweets with duplicates removed

---

## 📁 CSV Output Format

| nome_usuario | mensagem            | data                 |
|--------------|---------------------|----------------------|
| ex: fulano   | conteúdo do tweet…  | 25 abr. 2025 13:47   |

---

## ⚠️ Warnings

- ⚠️ **Scrapfly may occasionally become unavailable during searches.** If this happens, try again — Requests may fail silently or raise exceptions.
- 🟡 Nitter instances may go down or become unstable. If that happens, try changing the `BASE_URL` to another mirror listed [here](https://github.com/zedeus/nitter/wiki/Instances).

---


## ✉️ Contact

Feel free to open an issue or fork the project on GitHub:  
https://github.com/0xffff08/pyscraper

---

