Road safety data for various countries in the european union for the year 2018.
Data including various key metrics for drawing various relationships between figures.

## Data

The data on European Union Road Safety Facts and Figures which is extracted to

* Data - `data/eu_road_safety.csv` - the actual data

### Sources

[Wikipedia]: https://en.wikipedia.org/wiki/Road_safety_in_Europe



## Preparation

This repository uses [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) to parse the data.

You first need to install the dependencies:

```bash
pip install -r requirements.txt
```

Then run the following scripts:

```bash
python scripts/process.py
```

[![Python 3.9](https://img.shields.io/badge/python-3.9-blue.svg)](https://www.python.org/downloads/release/python-390/)


## Visualization

Visualization of the correlations between various labels for the European union road safety data can be found 
[here](https://desolate-sea-00472.herokuapp.com/).