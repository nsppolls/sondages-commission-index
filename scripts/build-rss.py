import marimo

__generated_with = "0.17.7"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import pandas as pd

    from feedgen.feed import FeedGenerator
    return FeedGenerator, pd


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
def _(fg, pd):
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
            .sort_values("pdf creation-date", ascending=False)
            .query('~url.isna()')
        )

        def entry(row, feed):
            pubdate = pd.to_datetime(row['pdf creation-date'])

            try:
                fe = feed.add_entry()
                fe.id(row.name)
                fe.title(row.name)
                fe.link(href=row['url'])
                fe.published(published=pubdate)
                fe.description(description=f"""
                - date de création du pdf : { row['pdf creation-date'] }
                """)
                return fe
            except:
                print(row["pdf creation-date"])


        feed.entry(entry=[], replace=True)
        df.apply(entry, feed=fg, axis=1)
    
        return df
    return (entries,)


@app.cell
def _(entries, fg, fg_metadata):
    fg_metadata
    fg_entries = entries(fg)

    #fg_entries
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
