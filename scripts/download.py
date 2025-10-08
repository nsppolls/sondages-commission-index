import marimo

__generated_with = "0.16.2"
app = marimo.App(width="medium")

with app.setup:
    import marimo as mo
    import pandas as pd
    import requests
    from pypdf import PdfReader
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
    last_modified = r.headers['last-modified'] if 'last-modified' in r.headers else None
    creation_date = None

    if not os.path.isfile(path+filename) or overwrite:
        os.makedirs(path, exist_ok=True)
        open(path+filename, "wb").write(r.content)

        try:
            pdf = PdfReader(path+filename)
            creation_date = pdf.metadata.creation_date
        except:
            print("problème avec le pdf : "+path+filename)


    if bar != None:
        bar.update()

    return (url, path, filename, pd.to_datetime(last_modified), pd.to_datetime(creation_date))


@app.cell
def _():
    save('/notices/medias/fichiers/add/162', overwrite=True)
    return


@app.cell
def _():
    files_current = pd.read_csv('files.csv')
    return (files_current,)


@app.cell
def _(files_current):
    files_current
    return


@app.cell
def _(files_current):
    files_current.query('`pdf creation-date`.isna()')
    return


@app.function
def get_files(index, overwrite=False):
    with mo.status.progress_bar(total=len(index)) as bar:
        files = (
            index
            #.iloc[0:10]
            .apply(
                lambda x: save(x.href, bar=bar, overwrite=overwrite),
                axis=1,
                result_type='expand',
            )
            .rename(
                columns = {
                    0: 'url',
                    1: 'path_local',
                    2: 'filename',
                    3: 'http last-modified',
                    4: 'pdf creation-date'
                }
            )
            .join(index[['name']])
        )

    return files


@app.cell
def _(index):
    def get_all():
        files_all = get_files(index, overwrite=True)
        files_all.to_csv('files.csv', index=False)
        return files_all
    return (get_all,)


@app.cell
def _(get_all):
    get_all()
    return


@app.cell
def _(files_current, index):
    files_current

    index_new = (
        index
        .query("~name.isin(@files_current.name)")
        #.pipe(get_files)
    )

    return (index_new,)


@app.cell
def _(index_new):
    index_new
    return


@app.cell
def _(files_current, index_new):
    if (len(index_new) > 0):
        files_new = index_new.pipe(get_files)
    else:
        files_new = pd.DataFrame()

    files = pd.concat([files_current, files_new])

    files
    return (files,)


@app.cell
def _(files):
    files.to_csv('files.csv', index=False)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
