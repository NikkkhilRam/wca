import pandas as pd
import emoji
from urlextract import URLExtract
from collections import Counter

extract = URLExtract()


def fetch_stats(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    num_message = df.shape[0]
    words = []
    links = []
    for message in df['messages']:
        words.extend(message.split())
    for message in df['messages']:
        links.extend(extract.find_urls(message))

    num_media = df[df['messages'] == ' <Media omitted>\n'].shape[0]

    return num_message, len(words), num_media, len(links)


def most_busy_users(df):
    x = df['user'].value_counts().head()
    return x


def percentage_message(df):
    new_df = round(df['user'].value_counts() / df.shape[0] * 100, 2).reset_index().rename(
        columns={'index': 'Name', 'user': 'Percentage'})
    return new_df


def emoji_count(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    emojis = []
    for message in df['messages']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

    emojis_count = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emojis_count


def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    timeline = df.groupby(['year', 'month']).count()['messages'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append((timeline['month'][i]) + "-" + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline

# def timeline(df):
#     new_df = df.groupby(['year', 'month']).count()['messages'].reset_index()
#     time = []
#     for i in range(new_df.shape[0]):
#         time.append(new_df['month'][i] + "-" + str(new_df['year'][i]))
#     new_df['months_time'] = time
#     return new_df
