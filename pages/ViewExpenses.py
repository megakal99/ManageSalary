import streamlit as st
import pandas as pd
from Data.Sl import date_salary
import matplotlib.pyplot as plt
import os

st.set_page_config(
    page_title="Manage Salary",
    page_icon="static/ico.png",  
)
### Draw Graphs
def draw_pie_chart(category):
    if category=='Needs':
      df = filtered_data[filtered_data['ParentCategory'] == category].loc[filtered_data['SubCategory']!='Needs',['SubCategory','Amount']]
    else:
      df = filtered_data[filtered_data['ParentCategory'] == category].loc[filtered_data['SubCategory']!='Other',['SubCategory','Amount']]
    aggregated = abs(df.groupby('SubCategory').sum()).reset_index()
    values = list(aggregated['Amount'])

    labels = list(aggregated['SubCategory'])
    # Creating autocpt arguments
    def func(pct, allvalues):
     absolute = pct/100.*sum(allvalues)
     return "{:.2f}%\n({:.2f}Dh)".format(pct, absolute)
    fig, ax = plt.subplots()
    ax.pie(values,autopct=lambda pct: func(pct,values),pctdistance=1.1,startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures the pie chart is circular.
    ax.set_title(f'Partition of Expenses for {category} Category')
    # Add legend to the right of the pie chart
    ax.legend(labels, loc='center left', bbox_to_anchor=(1, 0.5))
    return fig

def draw_bar_plot(category):
    if category=='Needs':
      df = filtered_data[filtered_data['ParentCategory'] == category].loc[filtered_data['SubCategory']!='Needs',['SubCategory','Amount']]
    else:
      df = filtered_data[filtered_data['ParentCategory'] == category].loc[filtered_data['SubCategory']!='Other',['SubCategory','Amount']]
    aggregated = abs(df.groupby('SubCategory').sum()).reset_index()
    values = list(aggregated['Amount'])
    subcategories= list(aggregated['SubCategory'])


    fig, ax = plt.subplots()
    ax.bar(subcategories, values)
    # ax.set_xlabel('SubCategory')
    # ax.set_ylabel('Expenses')
    ax.set_title(f'Expenses for {category} Category')

    return fig

# Load data from the JSON file
def load_data(fileName):
     try:
      df = pd.read_json(f'Data/MonthlyData/{fileName}')
      FileTime=fileName[:-5]
      return FileTime,df
     except FileNotFoundError:
       print(f"Error: The file does not exist.")
       return None
        
#Condition of exceeding 
def EmojCondition(Categ):
    if Categ=='Needs':
      if abs(needs-sal*.35) > sal * 0.35:
        return "🚩"
      else:
        return "✅"
    elif Categ=="Other":
      if abs(other-sal * 0.15) > sal * 0.15:
        return "🚩"
      else:
        return "✅"
    elif Categ=='short':
      if abs(shortTermSaving-sal*0.1) > sal*0.1:
        return "🚩"
      else:
        return "✅"
    elif Categ=='long':
      if longTermSaving < sal*0.3:
        return "🚩"
      else:
        return "✅"
    else:
      pass
# Load the data
files = os.listdir('Data/MonthlyData')
if len(files)==0:
    st.warning("No Data is existing!!!")
    st.stop()
selected_file = st.selectbox("Select a data file to show fully report:", list(reversed(files)))
TimeOfselectedFile,data = load_data(selected_file)
data['Date'] = data['Date'].apply(lambda x: pd.to_datetime(x).date())
# Sidebar with time range slicer
st.sidebar.title("Time Range Slicer")
start_date = st.sidebar.date_input("Start Date", min_value=data['Date'].min(), max_value=data['Date'].max(), value=data['Date'].min())
end_date = st.sidebar.date_input("End Date", min_value=data['Date'].min(), max_value=data['Date'].max(), value=data['Date'].max())
# Filter data based on the selected time range
filtered_data = data[(data['Date'] >= start_date) & (data['Date'] <= end_date)]
# Display the filtered data as an interactive table
st.table(filtered_data)
# Flash report
needs=sum(filtered_data[filtered_data['ParentCategory']=='Needs']['Amount'])
emergencyFunds=sum(filtered_data[filtered_data['SubCategory']=='Emergency Saving']['Amount'])
shortTermSaving=sum(filtered_data[filtered_data['SubCategory']=='Short Term Saving']['Amount'])
longTermSaving=sum(filtered_data[filtered_data['SubCategory']=='LongTerm Saving']['Amount'])
other=sum(filtered_data[filtered_data['ParentCategory']=='Other']['Amount'])
summerPlan=sum(filtered_data[filtered_data['ParentCategory']=='SummerPlan']['Amount'])
sal = date_salary[TimeOfselectedFile]
st.write("")
# st.markdown(
#         f"""
#         ### 📋 Flash Report 
#         **Category**|**ExpectedExpences/Grow**|**ActualRestedAmount**
#         -----|-----|-----|-----
#         |Needs|{sal*0.35:.2f}|{needs:.2f} {EmojCondition('Needs')}
#         |Other|{sal*0.15:.2f}|{other:.2f} {EmojCondition('Other')}
#         |ShortInvest|{sal*0.1:.2f}|{shortTermSaving:.2f} {EmojCondition('short')}
#         |EmergencyFund|{sal*0.1:.2f}|{emergencyFunds:.2f}
#         |LongInvest|{sal*0.3:.2f}|{longTermSaving:.2f} {EmojCondition('long')}
#         |SummerPlan|☀️|{summerPlan:.2f}☀️
#         """
# )
st.markdown(""" ### 📋 Flash Report """)
flashReport = {
    'Category': ['Needs', 'Other', 'ShortInvest', 'EmergencyFund', 'LongInvest', 'SummerPlan'],
    'ExpectedExpences/Grow': [f'{sal * 0.35:.2f}', f'{sal * 0.15:.2f}', f'{sal * 0.1:.2f}', f'{sal * 0.1:.2f}', f'{sal * 0.3:.2f}', f'{summerPlan:.2f} ☀️'],
    'ActualRestedAmount': [f'{needs:.2f}', f'{other:.2f}', f'{shortTermSaving:.2f}', f'{emergencyFunds:.2f}', f'{longTermSaving:.2f}', f'{summerPlan:.2f} ☀️'],
}

st.table(pd.DataFrame(flashReport))
st.write("")
# Select category
selected_category = st.radio("Select Category for visualizing:", ['Needs', 'Other'])
st.subheader(f'Visualization of your expenses')
# Draw Pie Chart and Bar Plot horizontally
# Create two columns
col1, col2 = st.columns(2)
# Draw Pie Chart in the first column
with col1:
 fig1 = draw_pie_chart(selected_category)
 st.pyplot(fig1)
# Draw Bar Plot in the second column
with col2:
 fig2 = draw_bar_plot(selected_category)
 st.pyplot(fig2)
