import marimo

__generated_with = "0.17.8"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import numpy as np

    from feedgen.feed import FeedGenerator
    return FeedGenerator, mo, pd


@app.cell
def _(FeedGenerator):
    fg = FeedGenerator()
    return (fg,)


@app.cell
def _(fg):
    def metadata(feed):
        fg.title('Les derniers sondages · NSPPolls')
        fg.description("hello")
        fg.link( href='https://codeberg.org/nsppolls', rel='alternate' )

        return feed
    return (metadata,)


@app.cell
def _(fg, metadata):
    fg_metadata = metadata(fg)
    return (fg_metadata,)


@app.cell
def _(fg, mo, pd):
    def entries(feed):
        df = (
            pd
            .read_csv('base.csv')
            .set_index('name')
            .join(
                pd
                .read_csv('files.csv')
                .set_index('name')
            )
            # .sort_values("pdf creation-date")
            # .query('~url.isna()')
            # .query('~`pdf creation-date`.isna()')
            .sort_values("http last-modified")
            .query('~url.isna()')
            .query('~`http last-modified`.isna()')
        )

        def entry(row, feed):
            published = pd.to_datetime(row['pdf creation-date'])
            updated = pd.to_datetime(row['http last-modified'], utc=True)

            try:
                fe = feed.add_entry()
                fe.id(row.name)
                fe.title(row.name)
                fe.link(href=row['url'])
                if (published != pd.NaT): fe.published(published=updated)
                #fe.updated(updated=updated)
                fe.description(description=mo.md(f"""
    - date de création du fichier pdf : { row['pdf creation-date'] }
    - date d'upload du fichier pdf : { row['http last-modified'] }
                """).text)
                return fe
            except Exception as e:
                print(row.name)
                print(published)
                print(updated)

                print(e)


        feed.entry(entry=[], replace=True)
        df.apply(entry, feed=fg, axis=1)

        return df
    return (entries,)


@app.cell
def _(entries, fg, fg_metadata):
    fg_metadata
    fg_entries = entries(fg)

    fg_entries
    return (fg_entries,)


@app.function
def write(feed):
    #feed.atom_file('polls.atom.xml') # Write the ATOM feed to a file
    feed.rss_file('polls.rss.xml', pretty=True) # Write the RSS feed to a file

    return feed


@app.cell
def _(fg, fg_entries):
    fg_entries
    write(fg)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
