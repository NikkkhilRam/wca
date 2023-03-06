import re
import pandas as pd
def preprocess(data):
    pattern = '\d{1,2}\/\d{1,2}\/\d{2},\s\d{1,2}:\d{2}\s(?:AM|PM)\s-\s'
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    for i in range(len(dates)):
        dates[i] = dates[i].replace("\u202f", "")

    df = pd.DataFrame({'user_message': messages, 'message_date': dates})
    name = df['user_message'].str.split(':').str[0]
    df['user'] = name
    df['messages'] = df['user_message'].str.split(':').str[1]
    df.drop('user_message', axis=1, inplace=True)
    df["message_date"] = pd.to_datetime(df["message_date"], format="%m/%d/%y, %I:%M%p - ")
    df['year'] = df['message_date'].dt.year
    df['month'] = df['message_date'].dt.month_name()
    df['day'] = df['message_date'].dt.day
    df['hour'] = df['message_date'].dt.hour
    df['minute'] = df['message_date'].dt.minute



    return df