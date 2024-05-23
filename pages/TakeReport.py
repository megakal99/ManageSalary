import streamlit as st
import os,json
import pandas as pd
from Data.Sl import date_salary
from datetime import datetime
import time
###############################""
st.set_page_config(
    page_title="Manage Salary",
    page_icon="static/ico.png",  
)
###################################
# Function to write data to JSON file
def write_to_json(file_path, new_data):
    try:
        # Try to read existing data from the JSON file
        with open(f"Data/MonthlyData/{file_path}", 'r') as json_file:
            existing_data = json.load(json_file)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        # If the file does not exist or is empty, initialize with an empty list
        existing_data = []
    # Append the new value to the existing data
    existing_data.append(new_data)
    # Write the combined data back to the JSON file
    with open(f"Data/MonthlyData/{file_path}", 'w') as json_file:
        json.dump(existing_data, json_file, indent=2)

def GetLastFileName():
   files = os.listdir('Data/MonthlyData')
   sorted_files = sorted(files)
   return sorted_files[-1]

def HandleSummerPlan():
  global SummerAmount
  st.warning("⚠️:If you have completed your summer holiday and spent an amount less than what is shown below for the Summer Plan savings, please enter the correct spent amount as a negative number, then click the button below. Pay close attention to avoid entering an amount less than what you actually spent! In case of a mistake (submitting an expense less than the actual spent amount), you can correct the transaction by adding an expense for the 'Long-Term Saving' subcategory with an amount equal to -(abs(what you already spent) - abs(wrongly submitted amount)).")
  # try:
  # spentAmount = st.number_input("Enter a negative number:", min_value={-SummerAmount}, max_value=0.0, step=0.01)
  # print(SummerAmount,spentAmount)
  # except:
  #   spentAmount = st.number_input("Enter a negative number:", min_value=0.0, max_value=0.0, step=0.01)
  if SummerAmount>0:
    spentAmount = st.number_input("Enter a negative number:")
  else:
    SummerAmount=round(SummerAmount)
    spentAmount = st.number_input("Enter a negative number:")
  if st.button("Click"):
    if (-SummerAmount<=spentAmount and spentAmount<0) or spentAmount== 0: 
      if spentAmount==0:
        st.warning("You submit 0 as expense of Summer/Holiday Plan!!! resubmit a valid expense")
        pass
      else:
        RestAmountAfterSummerHoliday=SummerAmount+spentAmount
        if RestAmountAfterSummerHoliday>=0:
          fileName=GetLastFileName()
          date=datetime.now().strftime("%d/%m/%Y")
          data1={
          "Amount":-SummerAmount,
          "ParentCategory": "SummerPlan",
          "SubCategory": "SummerPlan",
          "Date": date,
          }
          data2={
          "Amount":RestAmountAfterSummerHoliday,
          "ParentCategory": "Saving",
          "SubCategory": "LongTerm Saving",
          "Date": date,
          }
          write_to_json(fileName,data1)
          write_to_json(fileName,data2)
          st.success("Successfully added Data!")
          time.sleep(2)
          st.experimental_rerun()
        else:
          st.warning("Enter a valid expense!")     
    else:
      st.warning("Enter a valid expense!")
def getTotalIncrement():
  global ExpectedLongTermSavingAmount,LongTermSavingAmount,SummerAmount,EmergencyFundAmount
  files = os.listdir('Data/MonthlyData')
  ExpectedLongTermSavingAmount=0
  if len(files)==0:
    st.warning("No Data is existing!!!")
    st.stop()
  elif len(files)==1:
    file=files[-1]
    result_df=pd.read_json(f'Data/MonthlyData/{file}')
    file=file[:-5]
    ExpectedLongTermSavingAmount+=0.3*date_salary[file]
    LongTermSavingAmount=sum(result_df[result_df['SubCategory']=='LongTerm Saving']['Amount'])
    SummerAmount=sum(result_df[result_df['ParentCategory']=='SummerPlan']['Amount'])
    EmergencyFundAmount=sum(result_df[result_df['SubCategory']=='Emergency Saving']['Amount'])
  else:
   result_df=pd.read_json(f'Data/MonthlyData/{files[-1]}')
   for file in files[:-1]:
    df = pd.read_json(f'Data/MonthlyData/{file}')
    ExpectedLongTermSavingAmount+=0.3*date_salary[file[:-5]]
    result_df = pd.concat([result_df, df], ignore_index=True)
   LongTermSavingAmount=sum(result_df[result_df['SubCategory']=='LongTerm Saving']['Amount'])
   SummerAmount=sum(result_df[result_df['ParentCategory']=='SummerPlan']['Amount'])
   EmergencyFundAmount=sum(result_df[result_df['SubCategory']=='Emergency Saving']['Amount'])

def check():
  if LongTermSavingAmount>=ExpectedLongTermSavingAmount:
    return "✅"
  else:
    return "⛔"
def main():
    getTotalIncrement()
    HandleSummerPlan()
    st.markdown(f"""
        ### View of Incremental Savings from your all data:
        {check()} Actually You save {LongTermSavingAmount} instead of {ExpectedLongTermSavingAmount} for Long Term Savings
        - Actually You save {EmergencyFundAmount} for Emergency fund
        - Actually You save {SummerAmount} for your Summer Plan
        ### 
        """)
    

        
#########################################################
RestAmountAfterSummerHoliday=0
main()