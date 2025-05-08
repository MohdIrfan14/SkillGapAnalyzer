import streamlit as st
from pyresparser import ResumeParser
import json

st.title('Skill Gap Analyzer')  # Use st.title for the main heading
st.write('This is a colaborated project which involves droppping ur resume in this dropdown box and let this site analyze the gaps between the current world skills and yours')
st.header('Add Your File here.. ')
uploaded_file = st.file_uploader("Drop Your Files in this section", type=["pdf", "docx", "doc"], accept_multiple_files=False)
#backened

def extracting_skills(uploaded_file):
    if uploaded_file is not None:
        try:
            data = ResumeParser(uploaded_file).get_extracted_data()  # Pass the BytesIO object
            
            st.header("Extracted Data:") # use st.header or st.subheader
            user_skills = st.dataframe(data)
        #print(dict_data)  # Use st.json for pretty printing
        except Exception as e:
            st.error(f"Error processing file: {e}")
    else:
        st.info("Please upload a resume file to analyze.") # info message
extracting_skills(uploaded_file)

def toggle_option():
    with st.sidebar :
        st.link_button('DSA Cheatsheet','https://www.geeksforgeeks.org/dsa-tutorial-learn-data-structures-and-algorithms/') 
        #st.link_button()
        #st.page
toggle_option() 