#Importation of needed libraries
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import io

#Style setting for web interface and eventual visualisations/plots
plt.style.use('ggplot')

st.set_page_config(page_title='UR CRISTIANO RONALDO (CR7) - Extensive EDA & Analytics', layout = 'wide')

st.sidebar.title('📊 UR Cristiano (CR7) Analytics')

st.sidebar.image(r'C:\Users\kccha\OneDrive\Desktop\Programming\CR7\CR7\cristiano-ronaldo-8002334_1280.png', use_column_width=True)

sections = [
    "Introduction", 
    "Basic Exploration", 
    "Goals per Competition", 
    "Goals per Season", 
    "Goals per Club", 
    "Goals per Playing Position", 
    "Goals per Game Minute", 
    "Goals per Type", 
    "Scoreline After Goals",
    "Opponents", 
    "Favorite Opponents", 
    "Assists", 
    "Goals per Venue"
    ]

selections = st.sidebar.radio('Navigate to', sections)

#A fuction to contain the dataset and loading the dataset
def load_data():
    df = pd.read_csv(r'C:\Users\kccha\OneDrive\Desktop\Programming\CR7\CR7\data.csv')
    return df

#loading the data set
df = load_data()

#Let's fill in what will be shown when the different sections are clicked on the site/dashboard/frontend
if selections == 'Introduction':
    st.title('⚽ CR7 - Extensive EDA & Analytics')
    st.subheader('UR Cristiano Ronaldo - All club goals statistics')

    st.write("""
    **Cristiano Ronaldo dos Santos Aveiro** is a Portuguese professional footballer who plays as a forward for Al-Nassr and captains the Portugal national team.
    
    - **Current team**: Al-Nassr (#7 / Forward)
    - **Born**: February 5, 1985 (age 39 years), Funchal, Portugal
    - **Height**: 1.87 m
    - **Partner**: Georgina Rodríguez (2017–)
    - **Salary**: 26.52 million GBP (2022)
    - **Children**: Cristiano Ronaldo Jr., Alana Martina, Eva Maria, Mateo Ronaldo
    """)

elif selections == "Basic Exploration":
    st.subheader('🔍 Basic exploration')
    st.write('### Data snapshot')
    st.dataframe(df.head())
    st.write('### Data Info')

    # Capture and display DataFrame info
    buffer = io.StringIO()
    df.info(buf = buffer)
    s = buffer.getvalue()
    st.text(s)

    st.write('### Unique Values in each Column')
    st.dataframe(pd.DataFrame(df.apply(lambda col:len(col.unique())), columns = ['Unique Values Count']))
    st.write('### Summary Statistics for Categorical Columns')
    st.dataframe(df.describe(include=['object']).T)

elif selections == "Goals per Competition":
    st.subheader("🏆 Goals per Competition")
    fig = px.histogram(df, x = 'Competition', color = 'Club', title='Goals per Competition',
                 height=500, hover_name='Club', hover_data=['Competition', 'Club'])
    st.plotly_chart(fig)
    st.write('### Competition Goal counts')
    st.dataframe(df.Competition.value_counts())

elif selections == "Goals per Season":
    st.subheader("📅Goals per Season")
    fig = px.histogram(df, x = 'Season', color = 'Club', title='Goals per Season',
                 height=500, hover_name='Club', hover_data=['Season', 'Club'])
    st.plotly_chart(fig)
    st.write('### Season Goal counts')
    st.dataframe(df.Season.value_counts())

elif selections == "Goals per Club":
    st.subheader('🏅 Goals per Club')
    fig1 = px.histogram(df, x = 'Club', color = 'Season', title='Goals per Club - Season',
                 height=500, hover_name='Season', hover_data=['Competition', 'Season', 'Club'])
    fig2 = px.histogram(df, x = 'Competition', color = 'Competition', title='Goals per Club - Competition',
                 height=500, hover_name='Competition', hover_data=['Competition', 'Season', 'Club'])
    st.plotly_chart(fig1)
    st.plotly_chart(fig2)

elif selections == "Goals per Playing Position":
    st.subheader("⚽ Goals per Playing Position")
    fig = px.histogram(df, x = 'Playing_Position', color = 'Club', title='Goals per Playing Position',
                 height=500, hover_name='Club', hover_data=['Playing_Position', 'Competition', 'Season', 'Club'])
    st.plotly_chart(fig)

elif selections == "Goals per Game Minute":
    st.subheader("⏰ Goals per Game Minute")
    df['Minute'] = df['Minute'].str.extract('(\d+)', expand=False).fillna(0).astype(int)
    bins = [0, 15, 30, 45, 60, 75, 90, 105, 120]
    labels = ['0-15', '15-30', '30-45', '45-60', '60-75', '75-90', '90-105', '105-120']
    df['Minute_Bin'] = pd.cut(df['Minute'], bins = bins, labels = labels, right = False)
    fig = px.histogram(df, x = 'Minute_Bin', title='Goals per Game Minute', color = 'Club', height = 500)
    st.plotly_chart(fig)

elif selections == "Goals per Type":
    st.subheader("🏹 Goals per Type")
    fig = px.histogram(df, x = 'Type', title='Goals per Type', color = 'Club', height = 500)
    st.plotly_chart(fig)

elif selections == "Scoreline After Goals":
    st.subheader("🔢 Scoreline After Goals")
    top_20_scores = df['At_score'].value_counts().nlargest(20).index
    df_top_20 = df[df['At_score'].isin(top_20_scores)]

    fig, ax = plt.subplots(figsize=[15,7])
    sns.countplot(x='At_score', data = df_top_20, order = top_20_scores, ax = ax)
    ax.set_title('Top 20 Scoresheets after scoring', fontsize = 20)
    st.pyplot(fig)

elif selections == "Opponents":
    st.subheader("🆚 Opponents")
    fig, ax = plt.subplots(figsize = (30,10))
    sns.countplot(x = 'Opponent', data = df, order = df['Opponent'].value_counts().index, ax=ax)
    ax.set_title('Goal per Opponents', fontsize = 20)
    plt.xticks(rotation=90)
    st.pyplot(fig)

# Top 20 opponents
# elif selections == "Opponents":
#     st.subheader("🆚 Opponents")

#     top_20_opponents = df['Opponent'].value_counts().nlargest(20).index
#     df_top_20 = df[df['Opponent'].isin(top_20_opponents)]

#     fig, ax = plt.subplots(figsize = (30,10))
#     sns.countplot(x = 'Opponent', data = df_top_20, order = top_20_opponents, ax=ax)
#     ax.set_title('Goal per Opponents', fontsize = 20)
#     plt.xticks(rotation=90)
#     st.pyplot(fig)

elif selections == "Favorite Opponents":
    st.subheader("❤️ Favorite Opponents")
    fig, ax = plt.subplots(figsize = (15,7))
    fav_opponents_df = df['Opponent'].value_counts()[df['Opponent'].value_counts()>15]
    sns.countplot(x = 'Opponent', data = df[df['Opponent'].isin(fav_opponents_df.index)], order = fav_opponents_df.index, ax=ax)
    ax.set_title('Favorite Opponents', fontsize = 20)
    plt.xticks(rotation=90)
    st.pyplot(fig)

elif selections == "Assists":
    st.subheader("🤝 Assists")

    top_10_assists = df['Goal_assist'].value_counts().nlargest(10).index

    df_top_10 = df[df['Goal_assist'].isin(top_10_assists)]
    
    fig, ax = plt.subplots(figsize=(15,7))
    sns.countplot(x = 'Goal_assist', data = df_top_10, order = top_10_assists, ax = ax)
    ax.set_title('Top 10 Assists', fontsize = 20)
    st.pyplot(fig)

elif selections == "Goals per Venue":
    st.subheader("🏟️ Goals per Venue")
    
    fig, ax = plt.subplots(figsize=(15,7))
    sns.countplot(x = 'Venue', data = df, order = df['Venue'].value_counts().index, ax = ax)
    ax.set_title('Goals Per Venue', fontsize = 20)
    st.pyplot(fig)