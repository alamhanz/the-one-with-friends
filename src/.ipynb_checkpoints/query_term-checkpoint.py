import pandas as pd
print('getting the data ..')
dta=pd.read_csv('../data/friends_all_dialogue.csv')
while True:
    text_check=input(' Query term : ')
    print(dta[dta['dialogue'].str.contains(text_check.lower())][['eps','character','dialogue']])