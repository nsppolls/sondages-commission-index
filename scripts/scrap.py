import marimo

__generated_with = "0.11.0"
app = marimo.App(width="medium")


@app.cell
def _():
    # import marimo as mo
    import pandas as pd
    import requests
    from bs4 import BeautifulSoup
    from playwright.sync_api import sync_playwright

    from datetime import datetime
    return BeautifulSoup, datetime, pd, requests, sync_playwright


@app.cell
def _(datetime):
    current_year = datetime.now().year
    return (current_year,)


@app.cell
def _():
    return


@app.cell
def _(current_year):
    current_year
    return


@app.cell
def _():
    base = "https://www.commission-des-sondages.fr/notices/medias/dossiers/view"
    return (base,)


@app.cell
def _():
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0',
        # 'Accept': '*/*',
        # "Accept-Encoding": "gzip, deflate, br, zstd"
    }
    return (headers,)


@app.cell
def _(BeautifulSoup, base, headers, requests):
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
    return (list_year,)


@app.cell
def _(list_year):
    list_year(2025)
    return


@app.cell
def _(current_year, list_year, pd):
    index = (
        pd
        .concat([
            pd
            .DataFrame
            .from_records(list_year(year))
            .assign(year=year)
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
    index
    return


@app.cell
def _(index):
    index.to_csv('base.csv', index=False)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
