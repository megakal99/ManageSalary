import streamlit as st
import re
from datetime import datetime
from Data.Sl import date_salary
import json
import pandas as pd
import os
#############################""
st.set_page_config(
    page_title="Manage Salary",
    page_icon="static/ico.png",  
)
created=False
#########Time format input validate 
def validate_time_format(time_str):
    pattern = re.compile(r'^\d{2}-\d{2}-\d{4}$')
    return bool(pattern.match(time_str))
######Create json file to store data of the month
def modify_json_files():
    # Create the filename with the time_input
    filename = f"./Data/MonthlyData/{current_date}.json"
    # Check if the file is not exists
    if not os.path.exists(filename):
        CreateInitialData(filename)
        update_date_forLastofMonth()
    else:
        os.remove(filename)
        CreateInitialData(filename)
        update_date_forLastofMonth()
        


def write_to_json(file_path, new_data):
    try:
        # Read existing data from the JSON file
        with open(file_path, 'r') as json_file:
            existing_data = json.load(json_file)
    except FileNotFoundError:
        # If the file does not exist, initialize with an empty list
        existing_data = []

    # Append the new data to the existing data
    existing_data.append(new_data)

    # Write the combined data back to the JSON file
    with open(file_path, 'w') as json_file:
        json.dump(existing_data, json_file, indent=2)
    
def update_date_forLastofMonth():
     # Get a list of files in the specified folder
    jsonFile=''
    try:
        files = os.listdir('./Data/MonthlyData')
        # Sort the files
        
        sorted_files = sorted(files)
        # Calculate the number of JSON files
        num_json_files = len(files)
        if num_json_files>1:
            jsonFile= f"./Data/MonthlyData/{sorted_files[-2]}"
            current_date = datetime.now()
            date_string = current_date.strftime("%d/%m/%Y")
            df = pd.read_json(f'{jsonFile}')
            needs=sum(df[df['ParentCategory']=='Needs']['Amount'])
            shortTermSaving=sum(df[df['SubCategory']=='Short Term Saving']['Amount'])
            if  shortTermSaving>0:
                summerPlan=0.7*(shortTermSaving)
                longSaving=0.3*(shortTermSaving)
                form_data1 = {
                "Amount": summerPlan,
                "ParentCategory":'SummerPlan',
                "SubCategory":'SummerPlan',
                "Date": date_string,}
                form_data2 = {
                "Amount": longSaving,
                "ParentCategory":'Saving',
                "SubCategory":'LongTerm Saving',
                "Date": date_string,}
                form_data1_ = {
                "Amount": -summerPlan,
                "ParentCategory":'Saving',
                "SubCategory":'Short Term Saving',
                "Date": date_string,}
                form_data2_ = {
                "Amount": -longSaving,
                "ParentCategory":'Saving',
                "SubCategory":'Short Term Saving',
                "Date": date_string,}
                write_to_json(jsonFile, form_data1)
                write_to_json(jsonFile, form_data2)
                write_to_json(jsonFile, form_data1_)
                write_to_json(jsonFile, form_data2_)
            if needs>0:
                summerPlan=0.7*(needs)
                longSaving=0.3*(needs)
                _form_data1 = {
                "Amount": summerPlan,
                "ParentCategory":'SummerPlan',
                "SubCategory":'SummerPlan',
                "Date": date_string,}
                _form_data2 = {
                "Amount": longSaving,
                "ParentCategory":'Saving',
                "SubCategory":'LongTerm Saving',
                "Date": date_string,}
                _form_data1_ = {
                "Amount": -summerPlan,
                "ParentCategory":'Needs',
                "SubCategory":'SummerNeeds',
                "Date": date_string,}
                _form_data2_ = {
                "Amount": -longSaving,
                "Parent Category":'Needs',
                "SubCategory":'LongSavingNeeds',
                "Date": date_string,}
                write_to_json(jsonFile, _form_data1)
                write_to_json(jsonFile, _form_data2)
                write_to_json(jsonFile, _form_data1_)
                write_to_json(jsonFile, _form_data2_)
        else:
           pass
    except FileNotFoundError as e:
        print(f"Error: The folder 'Data/MonthlyData' does not exist. {e}")
    

def CreateInitialData(JsonFile):
    dateTime, sal = list(date_salary.items())[-1]
    dateTime=dateTime.replace("-", "/")
    d1={
        "Amount":round(sal*.35, 2),
        "ParentCategory":'Needs',
        "SubCategory":'Needs',
        "Date": dateTime,}
    d2={
        "Amount": round(sal*0.3,2),
        "ParentCategory":'Saving',
        "SubCategory":'LongTerm Saving',
        "Date": dateTime,}
    d3={
        "Amount": round(sal*0.1,2),
        "ParentCategory":'Saving',
        "SubCategory":'Short Term Saving',
        "Date": dateTime,}
    d4={
        "Amount": round(sal*0.1,2),
        "ParentCategory":'Saving',
        "SubCategory":'Emergency Saving',
        "Date": dateTime,}
    d5={
        "Amount": round(sal*0.15,2),
        "ParentCategory":'Other',
        "SubCategory":'Other',
        "Date": dateTime,}
    
    write_to_json(JsonFile, d1)
    write_to_json(JsonFile, d2)
    write_to_json(JsonFile, d3)
    write_to_json(JsonFile, d4)
    write_to_json(JsonFile, d5) 
##########################################
st.title("User Guide: How to Use This App💡")
st.write("""Here, you will find the complete guide on how to use this app to manage your expenses and bring your plans to fruition. """)
st.markdown(
    """
    ### 💾 The Guide:
    **SubCategory**|**Description**|**ParentCategory**
    -----|-----|-----
    |Housing bill|House rent Invoice|Needs
    |Wifi bill|Wifi Invoice|Needs
    |Water bill|Water Invoice|Needs
    |Electricity bill|Electrecity Invoice|Needs
    |Transport for work|Expenses relate to go to work|Needs
    |SummerNeeds|Expense relate to summer holiday if the rest amount of needs is greather than 0 |Needs
    |LongSavingNeeds|Expenses relate to LongTermSavings if the rest amount of needs is greather than 0|Needs
    |House needs|anything related to house needs(Gaz+dishwashing detergent+Wash clothes products+washing,etc)|Needs
    |Health needs|Medecines,Teeth products,Analysis, Doctor's consultation|Needs
    |LongTerm Saving|Savings associate to LongTerm gools|Saving
    |Short Term Saving|Savings associate to shortTerm gools|Saving
    |Emergency Saving|Savings associate to emergency issues such as complete cost of health needs|Saving
    |Personal products|Cost of buying clothes and personal products|Other
    |Enjoy|Eating outside, short Traveling, anything related to enjoy|Other
    |Family or charity issues|Anything related to family charity etc|Other
    |Summer|Savings for summer|SummerPlan
    |Needs|Income to add for needs|Needs
    """
)
st.text("")
st.text("Used Equation to divide monthly salary")
st.markdown("""
        ### 📋 Divide Planing:
         - 35% of salary for Needs. If the spent amount of Needs exceeds this percent, Red flag will appear!
         - 50% of salary for Saving (30% for LongTerm Savings,10% for ShortTerm Savings,10% for emergencySavings). If the spent amount of Saving exceeds this percent, Red flag will appear!
         - 15% of salary for Other. If the spent amount of Other exceeds this percent, Red flag will appear!
         - For Summer Plan at most we take the 70% from the rest of shortTerm and Needs amount and 30% will be sent to LongTermSavings!
        ### ⚠️ Warning:
            - In every beginning of any month add your salary and time to take it, ok!
            - In add expenses or incoming amounts form - and + are identify type of actions (expenses or income)!
        """)
st.text("")
salary_input = st.number_input("Salary")
current_date=datetime.now().strftime("%d-%m-%Y")
if st.button("Submit"):
    # if validate_time_format(current_date):
    #   pass
    # else:
    #   st.error("Please insert a valid format for the time field (dd-mm-yyyy)")
    #   st.stop()
    if salary_input>0:
        created=True
        date_salary.update({current_date:salary_input})
        with open('Data/Sl.py', 'w') as file:
            file.write(f'date_salary = {date_salary}\n')
        modify_json_files()
        st.success("Your Salary has been added successfully ✔️")
    else:
       st.warning("Please Add a real salary or fill time field! ❌")

st.warning("⚠️: If you input a faulty salary, please retype your true salary and submit again. Also, don't forget to add the expenses that you entered before with the wrong salary.")
  
