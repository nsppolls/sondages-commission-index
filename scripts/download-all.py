import marimo

__generated_with = "0.17.8"
app = marimo.App(width="medium")

with app.setup:
    import marimo as mo
    import pandas as pd

    from download import (
        save,
        get_files
    )

    base_url = "https://www.commission-des-sondages.fr"


@app.cell
def _():
    index = pd.read_csv('base.csv')
    return (index,)


@app.cell
def _(index):
    index
    return


@app.cell
def _(index):
    def get_all():
        files_all = get_files(index, overwrite=True)
        files_all.to_csv('files.csv', index=False)
        return files_all
    return (get_all,)


@app.cell
def _(get_all):
    files = get_all()
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
