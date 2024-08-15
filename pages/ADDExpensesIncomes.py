import streamlit as st
import re,os
from datetime import datetime
import json
from Data.Sl import date_salary
import pandas as pd
#######################################
st.set_page_config(
    page_title="Manage Salary",
    page_icon="static/ico.png",  
)
# Function to write data to JSON file
def write_to_json(file_path, new_data):
    try:
        # Try to read existing data from the JSON file
        with open(file_path, 'r') as json_file:
            existing_data = json.load(json_file)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        # If the file does not exist or is empty, initialize with an empty list
        existing_data = []
    # Append the new value to the existing data
    existing_data.append(new_data)
    # Write the combined data back to the JSON file
    with open(file_path, 'w') as json_file:
        json.dump(existing_data, json_file, indent=2)
def GetLastFileName():
   files = os.listdir('./Data/MonthlyData')
   sorted_files = sorted(files)
   return sorted_files[-1]
def getSumOf(Category,subCategory):
  dataf = pd.read_json(json_file_path)
  if Category in ['Needs','Other']:
     SUM=sum(dataf[dataf['ParentCategory']==Category]['Amount'])
     return SUM
  else:
     SUM=sum(dataf[dataf['SubCategory']==subCategory]['Amount'])
     return SUM
def addData():         
      form_data = {
        "Amount": amount,
        "ParentCategory": parent_category,
        "SubCategory": sub_category,
        "Date": date_input,
        }
      # Write the form data to the JSON file
      write_to_json(json_file_path, form_data)
      # Display the submitted data
      st.write("Submitted Data:")
      st.write(form_data)

def Choice():
    if parent_category =="Needs":
        if amount>0:
         sub_category = st.selectbox("SubCategory", ["Needs"])
         return sub_category
        else:
         sub_category = st.selectbox("SubCategory", ["Housing bill", "Wifi bill", "Water bill", "Electricity bill","Transport for work", "House needs", "Health needs"])
         return sub_category
    elif parent_category =="Saving":
         sub_category = st.selectbox("SubCategory", ["LongTerm Saving", "Short Term Saving", "Emergency Saving"])
         return sub_category
    else:
        if amount>0:
         sub_category = st.selectbox("SubCategory", ["Other"])
         return sub_category
        else:
         sub_category=st.selectbox("SubCategory",["Personal products", "Enjoy", "Family or charity issues"])
         return sub_category
         

#########Function for checking Time format of input Date
def validate_time_format(time_str):
    pattern = re.compile(r'^\d{2}/\d{2}/\d{4}$')
    return bool(pattern.match(time_str))
#####################Main
if len(os.listdir('Data/MonthlyData'))==0:
    st.warning("No Data is existing!!!")
    st.stop()

current_date = datetime.now().strftime("%d/%m/%Y")
# File path for the JSON file Data
json_file_path= f"Data/MonthlyData/{GetLastFileName()}"

# Create a form with 4 fields: Amount, Parent Category, SubCategory, and Date
amount = st.number_input("Amount", step=0.01)

parent_category_options = ["Needs", "Saving", "Other"]
parent_category = st.selectbox("Parent Category", parent_category_options)
sub_category=Choice()

# Use text_input for Date to allow manual entry
date_placeholder = "Enter date in dd/mm/yyyy format"
date_input = st.text_input("Date",value=current_date)

# # Validate and convert date input to a pandas datetime object
# try:
#     date = datetime.strptime(date_input, "%d/%m/%Y").strftime("%d/%m/%Y")
# except (ValueError, TypeError):
#     date = None
if st.button("Submit"):
    # Display a message if the date format is incorrect
    if not validate_time_format(date_input):
     st.warning("Please enter a valid date in dd/mm/yyyy format")
     st.stop
    else:
     if amount==0:
        st.warning("🙏 enter a valid amount either expence (-) or income (+)")
     else:
       if amount<0:
         if getSumOf(parent_category,sub_category)+amount>=0:
          msg='expense'
          addData()
          st.success(f'You added the {msg} ✅')
         else:
           st.warning("You're excedding the expected amount, expense from other Category or SubCategory of Saving!")
       else:
        msg='income'
        addData()
        st.success(f'You added the {msg} ✅')


st.warning("📋If you submit an expense without using a negative number or if you submit your income or growth amount with a negative value, please resubmit the correct amount. For example, if you submitted an expense of 300💰 with a positive number (300), you can correct it by resubmitting the expense with the number -300. The same approach can be used to correct other errors, such as inputting a negative amount instead of a positive one or inputting an amount less than or greater than the expected inputted amount. Don't forget if add a positive amount in category add reverse of this amount to corrspond category That's in case of two different category OK.")
