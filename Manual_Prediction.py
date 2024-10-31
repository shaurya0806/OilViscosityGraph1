# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 00:54:29 2024

in-production
"""

import streamlit as st
import joblib

st.set_page_config(
        page_title = "Techenomics-AI/Homepage",
        page_icon = "", 
    )

def main():
    

    
    html_temp = """
    <div style= "background-color:blue; padding:12px; border: 3px solid white; border-radius: 10px">
    <h2 style = "color:white; text-align:center; font-family: 'Arial', sans-serif">Predicting Viscosity Status, Percentage, Test Result</h2> 
    </div>
    """
    st.markdown(html_temp, unsafe_allow_html=True)
    
    
    model = joblib.load('OilViscosity1ModelNew_rf_100_40.joblib') 
    
    Eqmt = st.selectbox('Select Equipment Name you want to Predict for:' ,options =['UT006', 'UE007'])
    
    if Eqmt == 'UT006':
        Compt = st.selectbox('Select Compartment Name you want to Predict for:' ,options =['ENGINE'])
    else:
        Compt = st.selectbox('Select Compartment Name you want to Predict for:' ,options =['DIFFERENTIAL FRONT'])
    
    Visc_temp = st.selectbox('Select Viscosity Temperature you want to Predict on:' ,options =['40°C', '100°C'])
        
    p2 = st.selectbox('Select the Year you want to Predict (Possible for past and future as well):' ,options =[2021, 2022, 2023, 2024, 2025])
    
    p3 = st.slider("Select the month you want to Predict:",1,12)
    
    p4 = st.number_input("Select the Date you want to Predict:", step=1, format="%d", value = 1, max_value=31)
    
    
    if Eqmt =='UT006':
        Eqmt_Id = 14507
    else:
        Eqmt_Id = 121767
        
        
    if Compt =='ENGINE':
        Comp_Id = 117
    else:
        Comp_Id = 385
        
   
    
    if Visc_temp == '100°C':
        p1 = 100
    else:
        p1 = 40
    
    
    if p1 == 100:
        OilStandard = 15.3
    else:
        OilStandard = 115
    
    
    pred = model.predict([[p1,Eqmt_Id,Comp_Id,p2,p3,p4]])
    pred_value = round(pred[0], 2)
    
    Viscosity = ((pred_value / OilStandard) - 1) * 100
    ViscosityPct = round(Viscosity, 2)
        
    if st.button("Predict"):
        
        # Determine the status based on the prediction value 
        if -10 <= ViscosityPct <=10:
            status = 'Normal'
        elif -30 <= ViscosityPct <= 30:
            status = 'Warning'
        else:
            status = 'Problem'
        
        st.success(f'Predicted Value of Oil Viscosity% on {p4}/{p3}/{p2} will be : {ViscosityPct}%')
        
                   
        st.success(f'Predicted Status of Oil Viscosity on {p4}/{p3}/{p2} will be : {status} ')
        
        st.success(f'Predicted Result of Oil Viscosity on {p4}/{p3}/{p2} will be : {pred_value} ')

        
        st.info("""
                   - Warning Range : -10% to +10%
                   - Danger Range : -30% to +30%
                   
                   """)
        
        
    



 
if __name__ == '__main__':
    main()