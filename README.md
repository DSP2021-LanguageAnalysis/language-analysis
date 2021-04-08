# Data Science Project: Analysis of language variation and change

Data Science Master's Programme, University of Helsinki

### Table of Contents
- Backlog
- Description
- Installation
- Usage
- Theory
- Credits and Licence

### Backlog

https://github.com/orgs/DSP2021-LanguageAnalysis/projects/1

### Description
General description

### Newest online version
Go to http://193.166.25.206:8050/app/postags

### Installation / How to get the app working locally

1. Clone the repository
2. Create a virtual environment with `python3 -m venv venv`
3. Activate virtual environment with `source venv/bin/activate`
4. Run `pip install -r requirements.txt`
5. Add data folder `TCEECE` to local project root, this is ignored by GIT to avoid spreading the data (see `.gitignore` file)
6. Start app with `python index.py`
7. Visit `http://127.0.0.1:8050/app/postags` or `http://127.0.0.1:8050/app/topicmodel` in your browser

## Usage
### POS Visualisation
#### Scatter:
- Scatterplot with wordcount of each letter on corpus
  -	Each dot represents one letter
  -	y-axis shows how many words that letter have
  -	x-axis year the letter was written
#### Bar:
- Compare male and female tags
  -	X-axis: year of letter with both female and male writers if any
  -	Y-axis: percentage of the POS-tag(s) chosen
- Dynamically grouping years
  - **values incorrect**
  -	X-axis: YearGroup based of chosen number of groups
  -	Y-axis: percentage of NN1-tagged words
- Compare selected attributes
  - **values incorrect**
  -	Select number of year groups
  -	Select an attribute (SenderSex or SenderRank)
  -	X-axis: year groups
  -	Y-axis: percentage of NN1-tags
#### Line:
- Percentage of POS
  -	X-axis: time in years
  -	Y-axis: Percentage of chosen tag(s)
- Groups and compare
  -	Build two groups of tags and compare
  -	X-axis: Percentage of chosen groups of tags

### Topic model

## Theory
### POS Visualisation
#### Scatter:
•	Word count of each letter
#### Bar:
•	Word count / time / senderSex
•	Year grouped
•	Selected attribute
#### Line:
•	Percentage of POS
•	Groups and compare

### Topic model

### Credits and Licence

