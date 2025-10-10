# NSPPolls · commission des sondages

Ce dépôt contient :

 - le code sous forme de notebooks marimo pour produire des données à partir du site de [la commission des sondages].
- les données

L'actualité des sondages n'étant pas actuellement suractive, les scripts sont éxécutés tous les matins à `06:00 UTC` (Paris : `08:00` heure d'été, `07:00` d'hiver).

Le dépôt vit principalement sur [codeberg] mais est également dupliqué automatiquement sur [github]. Toutes les interactions sur github seront poliment ignorées, venez sur codeberg ☺️.

[la commission des sondages]: https://www.commission-des-sondages.fr/
[codeberg]: https://codeberg.org/nsppolls/sondages-commission-index
[github]: https://github.com/nsppolls/sondages-commission-index


## données et flux

|         fichier           |  contenu                  |
|--------------------|--------------------|
|         [`base.csv`]           |  liste des sondages référencés sur le site de la commission                   |
|         [`files.csv`]           | liste des fichiers `pdf` correspondant aux sondages avec quelques métadonnées au passage.                   |
| [`sondages-commission-index.rss`]| tous les changements sur ce dépôt en attendant un fil `rss` comme il faut|

[`base.csv`]: https://codeberg.org/nsppolls/sondages-commission-index/src/branch/main/base.csv
[`files.csv`]: https://codeberg.org/nsppolls/sondages-commission-index/src/branch/main/files.csv
[`sondages-commission-index.rss`]: https://codeberg.org/nsppolls/sondages-commission-index.rss

## scripts

|          script          |  contenu                  |
|--------------------|--------------------|
| [`scripts/scrap.py`]                   |     produit le fichier `base.csv`               |
| [`scripts/download.py`]                   |  produit le fichier `files.csv` de façon incrémental en récupérant seulement fichiers `pdf` manquants                  |

[`scripts/scrap.py`]: https://codeberg.org/nsppolls/sondages-commission-index/src/branch/main/scripts/scrap.py
[`scripts/download.py`]: https://codeberg.org/nsppolls/sondages-commission-index/src/branch/main/scripts/download.py

## automatisation

|  action                  |          récurrence          | description |
|--------------------|--------------------|---|
| [scrap-index.yaml]                   |  tous les matins à `06:00 UTC`                  | scrape l'index, fait le téléchargement au passage et commit les nouveautés |

[scrap-index.yaml]: https://codeberg.org/nsppolls/sondages-commission-index/actions?workflow=scrap-index.yaml

## voir aussi
