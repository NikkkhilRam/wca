import streamlit as st
import preprocessing
import helper
import matplotlib.pyplot as plt

st.sidebar.title('Whatsapp chat analyzer')
uploaded_file = st.sidebar.file_uploader('Choose a file')
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode('utf-8')
    df = preprocessing.preprocess(data)
    df.dropna(subset=['messages'], inplace=True)
    user_list = df['user'].unique().tolist()
    user_list.sort()
    user_list.insert(0, "Overall")
    selected_user = st.sidebar.selectbox('Show analysis wrt', user_list)
    st.title('Chats Dataframe')
    st.dataframe(df)

    if st.sidebar.button("Show Analysis"):
        num_messages, words, num_media, num_links = helper.fetch_stats(selected_user, df)
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header('Media Shared')
            st.title(num_media)
        with col4:
            st.header('Links Shared')
            st.title(num_links)

        timeline = helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        plt.bar(timeline['time'], timeline['messages'])
        plt.xticks(rotation='vertical')
        plt.show()
        st.pyplot(fig)

        if selected_user == 'Overall':
            st.title('Most Busy Users')
            x = helper.most_busy_users(df)
            fig, ax = plt.subplots()
            col1, col2 = st.columns(2)

        percentage_message = helper.percentage_message(df)

        with col1:
            ax.bar(x.index, x.values, color='red')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col2:
            st.dataframe(percentage_message)

        most_emoji = helper.emoji_count(selected_user, df)
        # most_emoji = most_emoji.astype(float)
        st.title('Most Used Emojis')

        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(most_emoji)
        with col2:
            fig2, bx = plt.subplots()
            bx.pie(most_emoji[1].head(), labels=most_emoji[0].head(), autopct='%0.2f')
            st.pyplot(fig2)
