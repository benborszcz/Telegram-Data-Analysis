# Telegram Data Pull and Analysis

## Description

This is a Python program that pulls and analyzes data from Telegram using a given telegram groupchat json data file

## Getting Started

### Dependencies
* Python 3.8+
* requirements.txt

### Installing
* Clone the repository
* Navigate to directory the project is stored in
```
pip install -r requirements.txt
```

### Usage
Add your Telegram groupchat data file to the Data folder

Look at the constant variables at the top of data_pull.py
```
TARGET_NAME = 'target_name' #put the name of the users data you want to get
TELEGRAM_FILE_NAME = 'your_telegram_groupchat_data' #do not put .json
```
Edit these to your specifications

Run data_pull.py
```
py data_pull.py
```

Now files will be save to the Data folder containing specific information about the target user and overall information about the groupchat.

Look at the constant variables at the top of data_analysis_total.py
```
# Input the names of the users you would like to compare into this array, max of 5
USERS = ['User1', 'User2', 'User3', 'User4', 'User5']
```
Edit these to your specifications

Run data_analysis_total.py
```
py data_analysis_total.py
```
A window should appear with the graph comparing the users you specified along with linear and quadratic lines of best fit.


## Authors
Ben Borszcz - ben.borszcz@gmail.com

## Version History
* 0.1
    * Initial Release
