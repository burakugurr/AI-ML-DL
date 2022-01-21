from copyreg import pickle
from matplotlib.pyplot import title
import streamlit as st
import pandas as pd
import plotly.express as px
import pandas as pd
from torch import special
import reader
import pickle
import time
from pathlib import Path

df = pd.read_csv(filepath_or_buffer =  "https://raw.githubusercontent.com/burakugurr/AI-ML-DL/master/CampusRec_Streamlit/Placement_Data_Full_Class.csv")

st.set_page_config(
     page_title="Campus Recruitment App",
     page_icon="🧊",
     layout="wide",
     initial_sidebar_state="auto",
     menu_items={
         'Get Help': 'https://github.com/burakugurr',
         'Report a bug': "https://github.com/burakugurr",
         'About': "# Campus Recruitment App created by Burak Uğur",
     }
 )

# Statistics Chart Functions

def genderchart(data):
    fig = px.pie(data,title='Stundent Gender' ,values=data['gender'].value_counts(), names=['Famle','Male'],color_discrete_sequence=px.colors.sequential.Viridis)
    return fig

def ssc_pchart(data):
    fig = px.bar(data, x=data['ssc_b'].unique(), y=data['ssc_b'].value_counts())
    return fig

def ssc_p_piechart(data):
    fig = px.pie(data, names=data['ssc_b'].unique(), values=data['ssc_b'].value_counts(),color_discrete_sequence = px.colors.sequential.Viridis)
    return fig

def degree_chart(data):
    fig = px.pie(data, names=data['degree_t'].unique(), values=data['degree_t'].value_counts()
    ,color_discrete_sequence=px.colors.sequential.Plasma)
    return fig
def hsc_pchart(data):
    fig = px.pie(data, names=data['hsc_s'].unique(), values=data['hsc_s'].value_counts()
,color_discrete_sequence=px.colors.sequential.Electric,hole = 0.2,)
    return fig

def status_chart(data):
    fig = px.pie(data, names=data['status'].unique(), values=data['status'].value_counts()
,color_discrete_sequence=px.colors.sequential.Turbo,hole = 0.2,)
    return fig

def salary_histogram(data):
    fig = px.histogram(data, x="salary", nbins=15, title="Salary Distribution", color_discrete_sequence=px.colors.sequential.Tealgrn )
    return fig

def salary_scatter(data):
    fig = px.scatter(data, x=data['salary'].index, y="salary",title='Salary Distribution of Students Gender'
,color ='gender')
    return fig

def sscb_bar(data):
    fig = px.histogram(data, x="ssc_p",  nbins=20, text_auto=True,color_discrete_sequence=px.colors.qualitative.Prism,title='Secondary Education percentage')
    return fig
def hsc_p_bar(data):
    fig = px.histogram(data, x="hsc_p",  nbins=20, text_auto=True,color_discrete_sequence=px.colors.qualitative.Prism,
    title='Higher Secondary Education percentage')
    return fig
def degree_p_bar(data):
    fig = px.histogram(data, x="degree_p",  nbins=20, text_auto=True,color_discrete_sequence=px.colors.qualitative.Prism,
    title='Degree Percentage')
    return fig
def etest_p_bar(data):
    fig = px.histogram(data, x="etest_p",  nbins=20, text_auto=True,color_discrete_sequence=px.colors.qualitative.Prism,
    title='Employability test percentage ( conducted by college)')
    return fig

# Chart Functions



def show_statistics():
    st.subheader('Statistics')
    st.plotly_chart(genderchart(df))
    
    st.subheader('SSC Percentage')
    col1, col2 = st.columns(2)
    with st.container():
        col1.plotly_chart(ssc_pchart(df))
    with st.container(): 
        col2.plotly_chart(ssc_p_piechart(df))
    st.subheader('Degree Type')
    st.plotly_chart(degree_chart(df))
    st.subheader('HSC Percentage')
    st.plotly_chart(hsc_pchart(df))
    st.subheader('Status')
    st.plotly_chart(status_chart(df))
    st.subheader('Salary Distribution')
    st.plotly_chart(salary_histogram(df))
    st.plotly_chart(salary_scatter(df))
    st.subheader('Education Percentage')
    st.plotly_chart(sscb_bar(df))
    st.plotly_chart(hsc_p_bar(df))
    st.plotly_chart(degree_p_bar(df))
    st.plotly_chart(etest_p_bar(df))






def show_predict():
    st.header('Your Answer')
    gender = st.selectbox('Select Gender',('Male','Famle'))
    ssc_p = st.number_input('Insert a Secondary Education percentage- 10th Grade', min_value=0, max_value=100, value=0)
    ssc_b = st.selectbox('Select Board of Education- Central/ Others', ('Central', 'Others'))  
    
    hsc_p = st.number_input('Insert a Higher Secondary Education percentage- 12th Grade', min_value=0, max_value=100, value=0)
    hsc_b = st.selectbox('Select Board of Education- Central/ Others ',('Central', 'Others'))
    hsc_s = st.selectbox('Select Specialization in Higher Secondary Education- Arts/ Science/ Commerce',('Arts', 'Science', 'Commerce'))
    
    degree = st.number_input('Insert a Degree Percentage', min_value=0, max_value=100, value=0)
    degree_t = st.selectbox('Select Under Graduation(Degree type)- Field of degree education',('Sci&Tech', 'Comm&Mgmt', 'Others'))
    workex = st.selectbox('Select Work experiment',('Yes', 'No'))
    etest = st.number_input('Insert a Employability test percentage ( conducted by college)', min_value=0, max_value=100, value=0)
    special = st.selectbox('Select Post Graduation(MBA)- Specialization',('Mkt&Fin', 'Mkt&HR'))
    mba = st.number_input('Insert a MBA percentage', min_value=0, max_value=100, value=0)
    salary = st.slider('What is your Salary?', 0, 1000000, 1)

    if st.button('Get Predict'):
        df_new = reader.create_df(gender,ssc_p,ssc_b,hsc_p,hsc_b,hsc_s,degree,degree_t,workex,etest,special,mba,salary)
        model = pickle.load(open('classifier.pkl', 'rb'))
        prediction = model.predict(df_new)
        with st.spinner('Wait for it...'):
            time.sleep(5)
            if prediction == 1:
                st.success('You are placement for the campus')
                st.balloons()
            else:
                st.error('You are not placement for the campus')

    else:
        st.info('Plase fill all the fields and click on the Get Predict button')



def mainpage():

    st.image('https://images.unsplash.com/photo-1530099486328-e021101a494a?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1247&q=80')
    with st.container():
        st.write("This data set consists of Placement data of students in a XYZ campus. It includes secondary and higher secondary school percentage and specialization. It also includes degree specialization, type and Work experience and salary offers to the placed students")
        st.write("https://www.kaggle.com/benroshan/factors-affecting-campus-placement")





# Main Function


st.title("Survey of Placed University Students")


app_mode = st.sidebar.selectbox("Choose the app mode",
        ["Home Page","Show Statistics", "Predict the own results"],
        )


if app_mode == "Show Statistics":
    show_statistics()
elif app_mode == "Predict the own results":
    show_predict()
elif app_mode =='Home Page':
    mainpage()
