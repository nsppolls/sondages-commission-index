import marimo

__generated_with = "0.16.2"
app = marimo.App(width="medium")

with app.setup:
    import marimo as mo
    import pandas as pd
    import requests
    import pprint
    import os

    base_url = "https://www.commission-des-sondages.fr"


@app.cell
def _():
    index = pd.read_csv('base.csv')
    return (index,)


@app.cell
def _(index):
    index
    return


@app.function
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


@app.cell
def _():
    save('/notices/medias/fichiers/add/162')
    return


@app.cell
def _():
    files_current = pd.read_csv('files.csv')
    return (files_current,)


@app.cell
def _(files_current):
    files_current
    return


@app.function
def get_files(index):
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
            .join(index[['name']])
        )

    return files


@app.cell
def _(index):
    def get_all():
        files_all = get_files(index)
        files_all.to_csv('files.csv', index=False)
        return files_all
    return


@app.cell
def _():
    #get_all()
    return


@app.cell
def _(files_current, index):
    files_current

    index_new = (
        index
        .query("~name.isin(@files_current.name)")
        #.pipe(get_files)
    )

    if (len(index_new) > 0):
        files_new = index.pipe(get_files)
    else:
        files_new = pd.DataFrame()
    
    files = pd.concat([files_current, files_new])

    files
    return (files,)


@app.cell
def _(files):
    files.to_csv('files.csv', index=False)
    return


if __name__ == "__main__":
    app.run()
