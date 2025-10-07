import marimo

__generated_with = "0.16.2"
app = marimo.App(width="medium")

with app.setup:
    import marimo as mo
    import pandas as pd
    import requests
    from bs4 import BeautifulSoup
    #from playwright.sync_api import sync_playwright

    from datetime import datetime

    base = "https://www.commission-des-sondages.fr/notices/medias/dossiers/view"

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0',
        # 'Accept': '*/*',
        # "Accept-Encoding": "gzip, deflate, br, zstd"
    }


@app.cell
def _():
    current_year = datetime.now().year
    return (current_year,)


@app.cell
def _(current_year):
    current_year
    return


@app.function
def list_year(year):
    url = f"{base}/{year}"

    s = requests.Session()
    s.get("https://www.commission-des-sondages.fr/notices/")
    #url = "https://www.commission-des-sondages.fr/notices/medias/dossiers/view/2025" #.replace("2016", "2025")
    page = s.get(url, headers=headers)
    # print(url)
    # print(page)
    # print(page.text)
    html = BeautifulSoup(page.text, "html.parser")

    # with sync_playwright() as p:
    #     browser = p.firefox.launch(headless=True)  # Change to True for headless mode
    #     page = browser.new_page()
    #     page.goto("https://www.commission-des-sondages.fr/notices/")
    #     page.wait_for_timeout(1000)
    #     page.goto(url)
    #     #page.wait_for_timeout(10000)
    #     html = BeautifulSoup(page.content(), "html.parser")
    #     #print(html)
    #     browser.close()

    pdf = html.find_all("a", {"class": "pdf_download"})

    #print([ { "name": a.text, "url": a['href'] } for a in pdf ])

    return ([
        {
            "name": a.text,
            "href": a['href']
        }
        for a in pdf
    ])


@app.cell
def _():
    list_year(2025)
    return


@app.cell
def _(current_year):
    index = (
        pd
        .concat([
            
            pd
            .DataFrame
            .from_records(list_year(year))
            .assign(year=year)
            .iloc[::-1]

            for year in range(2016, current_year+1)
        ])
    )
    return (index,)


@app.cell
def _(index):
    print(len(index))
    return


@app.cell
def _(index):
    index_sorted = (
        index
        .assign(
            id = lambda df: (
                df.name
                .str.strip()
                .str.replace(" ", "-")
                .str.split("-")
                .apply(lambda x: x[0])
                #.astype('int')
            )
        )
        .sort_values('id')
    )
    return (index_sorted,)


@app.cell
def _(index_sorted):
    index_sorted
    return


@app.cell
def _(index_sorted):
    index_sorted.query("id.duplicated()")
    return


@app.cell
def _(index_sorted):
    index_sorted.query("id.str.contains('-')")
    return


@app.cell
def _(index):
    index.to_csv('base.csv', index=False)
    return


if __name__ == "__main__":
    app.run()
