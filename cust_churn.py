import streamlit as st
import streamlit.components.v1 as stc
import pickle

with open('model_lr.pkl', 'rb') as file:
    model_lr = pickle.load(file)

html_temp = """<div style="backgrond-color:000;padding:10px;border-radius:10px">
                <h1 style="color:#fff;text-align:center">Customer Churn Prediction App</h1>
                <h1 style=:color:#fff;text-align:center:>Customer Churn Prediction</h1>
                """

desc_temp = """ ### This app is used by Credit Team for predicting customer churn 
                This app is created by Aisyah Ajibah Rahmah 
                
                ### Data Source
                Kaggle: Link <https://www.kaggle.com/datasets/blastchar/telco-customer-churn>
                """

def main():
    stc.html(html_temp)
    menu = ["Home", "Machine Learning App"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        st.subheader("Home")
        st.markdown(desc_temp, unsafe_allow_html=True)
    elif choice == "Machine Learning App":
        run_ml_app()

def run_ml_app():
    design = """<div style="padding:15px;">
                    <h1 style="color:#fff">Customer Churn Prediction</h1>
                </div
             """
    st.markdown(design, unsafe_allow_html=True)
    left, right = st.columns((2,2))
    gender = left.selectbox('Gender', ('Male', 'Female'))
    SeniorCitizen = right.selectbox('Senior Citizen', ('Yes', 'No'))
    Partner = left.selectbox('Partner',('Yes','No'))
    Dependents = right.selectbox('Dependents', ('Yes', 'No'))
    PhoneService = left.selectbox('Phone Service',('Yes','No'))
    MultipleLines = right.selectbox('Multiple Lines',('No phone service','Yes', 'No'))
    InternetService = left.selectbox('Internet Service',('DSL','Fiber optic','No'))
    OnlineSecurity = right.selectbox('Online Security', ('Yes', 'No'))
    OnlineBackup = left.selectbox('Online Backup',('No phone service','Yes', 'No'))
    DeviceProtection = right.selectbox('Device Protection',('No phone service','Yes', 'No'))
    TechSupport = left.selectbox('Tech Support',('No phone service','Yes', 'No'))
    StreamingTV = right.selectbox('Streaming TV',('No phone service','Yes', 'No'))
    StreamingMovies = left.selectbox('Streaming Movie',('No phone service','Yes', 'No'))
    Contract = right.selectbox('Contract',('Month-to-month','One year', 'Two year'))
    PaperlessBilling = left.selectbox('Paperless Billing',('Yes', 'No'))
    PaymentMethod = right.selectbox('Payment Method',('Electronic check','Mailed check', 'Bank transfer (automatic)','Credit card (automatic)'))
    MonthlyCharges = left.number_input('Monthly Charges')
    TotalCharges = right.number_input('Total Charges')
    tenure = left.number_input('Tenure')
    button = st.button("Predict")

    #If button is clilcked
    if button:
        result = predict(gender, SeniorCitizen, Partner, Dependents, PhoneService, MultipleLines, InternetService,
                         OnlineSecurity, OnlineBackup, DeviceProtection, TechSupport, StreamingTV, StreamingMovies,
                         Contract, PaperlessBilling, PaymentMethod, MonthlyCharges,TotalCharges,tenure)

        if result == 'Churn':
            st.warning(f'This customer is likely to {result}')
        else:
            st.success(f'This customer is {result}')

def predict(gender, SeniorCitizen, Partner, Dependents, PhoneService, MultipleLines, InternetService,
                         OnlineSecurity, OnlineBackup, DeviceProtection, TechSupport, StreamingTV, StreamingMovies,
                         Contract, PaperlessBilling, PaymentMethod, MonthlyCharges,TotalCharges,tenure):
    #Process user input
    gen = 0 if gender == 'Female' else 1
    sen = 0 if SeniorCitizen == 'No' else 1
    par = 0 if Partner == 'No' else 1
    dep = 0 if Dependents == 'No' else 1
    pho = 0 if PhoneService == 'No' else 1
    mul = float(0 if MultipleLines == "No" else 1 if MultipleLines == "No phone service" else 2)
    net = float(0 if InternetService == "No" else 1 if InternetService == "No phone service" else 2)
    ose = float(0 if OnlineSecurity == "No" else 1 if OnlineSecurity == "No phone service" else 2)
    oba = float(0 if OnlineBackup == "No" else 1 if OnlineBackup == "No phone service" else 2)
    dev = float(0 if DeviceProtection == "No" else 1 if DeviceProtection == "No phone service" else 2) 
    tec = float(0 if TechSupport == "No" else 1 if TechSupport == "No phone service" else 2)
    stv = float(0 if StreamingTV == "No" else 1 if StreamingTV == "No phone service" else 2)
    mov = float(0 if StreamingMovies == "No" else 1 if StreamingMovies == "No phone service" else 2)
    con = float(0 if Contract == "Month-to-month" else 1 if Contract == "One year" else 2)
    pap = 0 if PaperlessBilling == 'No' else 1
    pay = float(0 if PaymentMethod == "Bank transfer(automatic)" else 1 if PaymentMethod == "Credit card(autometic)" else 2 if PaymentMethod == "Electronic Check" else 3)  


    #Making prediction
    prediction = model_lr.predict([[gen, sen, par, dep, pho, mul, net, ose, oba, 
                                                     dev, tec, stv, mov, con, pap, pay, MonthlyCharges, TotalCharges, tenure]])
    result = 'Churn' if prediction == 0 else 'Not Churn'
    return result

if __name__ == "__main__":
    main()
