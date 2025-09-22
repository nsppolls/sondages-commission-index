import marimo

__generated_with = "0.11.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import requests
    import pprint
    import os
    return mo, os, pd, pprint, requests


@app.cell
def _(pd):
    index = pd.read_csv('base.csv')
    return (index,)


@app.cell
def _(index):
    index
    return


@app.cell
def _():
    base_url = "https://www.commission-des-sondages.fr"
    return (base_url,)


@app.cell
def _():
    return


@app.cell
def _(base_url, os, requests):
    def save(href, bar=None, overwrite=False):
        r = requests.get(f"{base_url}{href}", allow_redirects=True)

        url = r.url
        path = "archives/"+"/".join(url.split('/')[6:-1])+"/"
        filename = url.split('/')[-1]

        if not os.path.isfile(path+filename) or overwrite:
            os.makedirs(path, exist_ok=True)
            open(path+filename, "wb").write(r.content)


        if bar != None:
            bar.update()

        return (url, path, filename)
    return (save,)


@app.cell
def _(save):
    save('/notices/medias/fichiers/add/162')
    return


@app.cell
def _(index, mo, save):
    with mo.status.progress_bar(total=len(index)) as bar:
        files = (
            index
            #.iloc[0:10]
            .apply(
                lambda x: save(x.href, bar=bar),
                axis=1,
                result_type='expand',
            )
            .rename(
                columns = {
                    0: 'url',
                    1: 'path_local',
                    2: 'filename'
                }
            )
        )
    return bar, files


@app.cell
def _(files):
    files.to_csv('files.csv', index=False)
    return


if __name__ == "__main__":
    app.run()
