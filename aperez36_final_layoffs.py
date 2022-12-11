import csv
import streamlit as st 
import altair as alt 
import numpy as np
import pandas as pd 
from datetime import datetime
import plotly.express as px

#title 
st.title('2022 layoff Data')

#read the layoffs csv file create dateframe called df 
df= pd.read_csv('layoffs.csv')

#clean data drop any zero or null values 
df = df.dropna(axis = 0) 

#display dataframe 
# st.dataframe(df) 

#Tabs 
tab1, tab2, tab3= st.tabs(["Top Layoffs", "Country Data", "Data"])

#list for country 
clist = df['country'].unique()
x = any(clist)

#list for Company 
comlist = df['company'].unique()
list = any(comlist)



with tab1:
   st.markdown('The data presented is from Global 2022 Layoff Data')
   st.image("https://mondo.com/wp-content/uploads/2022/06/mass-layoffs-in-2022-whats-next-for-employees.jpg", width=400)
   dis= df.describe().T.style.background_gradient(axis=0)
   
   
 

#Tab 2
with tab2:
    st.header("Country")

if x != " ":
    
    country = tab2.selectbox("Select a country:",clist)


    df_country = df[df['country']== country]

#Number of layoffs by compnay 
    com_Chart = alt.Chart(df_country).mark_line().encode(
        alt.X('company'), 
        alt.Y('total_laid_off', title= "Total Layoffs")
    ).properties(
    title='Number of Layoffs by Compnay '
    ).interactive()

    tab2.altair_chart(com_Chart, use_container_width=True)
    
#Layoffs by Industry 
    indy = df_country.groupby(by=['industry','total_laid_off', 'date']).size().reset_index(name='count')
    industry= alt.Chart(indy).mark_bar().encode(
         alt.X('date:T'),
         alt.Y('count'),
         color='industry'
    ).properties(
    title='Number of Layoffs by Industry'
    ).interactive()

    tab2.altair_chart(industry, use_container_width=True)
    
    tab2.markdown('The figure above illustrates the the number of layoff during each month for a specific company and the amount of lay offs per industry..')

#Tab 1 

#top 10 number of layoff
    top_sort = df.sort_values('total_laid_off', ascending=False).head(10)

#top number of lay offs by company 
    topcom=alt.Chart(top_sort).mark_bar().encode(
        alt.X('company:N', sort='-y'),
        alt.Y('total_laid_off:Q',title= "Total Layoffs"),
        color=alt.Color('company')
    ).properties(
    title='Top Layoffs By Company'
    ).interactive()


    y = alt.Chart(top_sort).mark_bar(
        cornerRadiusTopLeft=3,
        cornerRadiusTopRight=3
    ).encode(
        alt.X('month(date):O'), 
        alt.Y('count():Q'),
        color='company:N'
    ).properties(
    title='Top Layoffs by Month & Company'
    ).interactive()

    tab1.altair_chart(topcom | y, use_container_width=True)

    tab1.write(dis)
    tab1.markdown('This figure illustrates the the distrubition of total laid off, percentage of laid offs, and funds raised.')

#Group by Countries

    countries = df.groupby(by ='country')['total_laid_off'].sum().reset_index(
        name='Count').sort_values(['Count'], ascending=False).head(10)

    chart_countries= alt.Chart(countries).mark_bar().encode(
         alt.X('country:N', sort='-y', title='Country'),
         alt.Y('Count', title='Number of Layoffs'), 
         color=alt.Color('country')
    ).properties(
        title='Top 10 Sector Layoff'   
    ).interactive()
    tab1.altair_chart(chart_countries , use_container_width=True)

#Group by industry 
    i = df.groupby(by ='industry')['total_laid_off'].sum().reset_index(
        name='Count').sort_values(['Count'],ascending=False).head(10)
    
    view=alt.Chart(i).mark_bar().encode(
        alt.X('industry:N', sort='-y'),
        alt.Y('Count:Q'),
        color=alt.Color('industry')
    ).properties(
        title='Top 10 Sector Layoff'
    ).interactive()
    tab1.altair_chart(view , use_container_width=True)
    


with tab3:

    st.write(df)



    
