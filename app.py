import streamlit as st
import pickle
import time

# Load models
with open('kmeans_model.pkl', 'rb') as f:
    kmeans = pickle.load(f)

with open('scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)

with open('encoder.pkl', 'rb') as f:
    encoder = pickle.load(f)

# Credit card mapping
cluster_card_mapping = { 
    0: 'Synchrony Premier World Mastercard',
    1: 'CareCredit Credit Card',
    2: 'PayPal Cashback World Mastercard',
    3: 'Venmo Visa Credit Card',
    4: 'Synchrony HOME Credit Card',
    5: 'Ashley Advantage Credit Card',
    6: 'Synchrony Car Care Credit Card',
    7: 'Verizon Visa Card'
}

# Custom CSS for footer
st.markdown("""
    <style>
    .main {
        min-height: 100vh;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    footer {
        text-align: center;
        margin-top: auto;
        padding: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

# Add the logo at the top center
st.image("image.png", width=250)  # Replace with your logo URL or local path

# Function to display the form and process inputs
def show_form():
    st.title('Credit Card Recommendation System')
    st.write('Find the perfect credit card based on your financial profile and habits.')

    # Create two wide columns for the first set of input fields
    col1, col2 = st.columns(2)

    with col1:
        age = st.number_input('Age', min_value=18, max_value=100, step=1)
        annual_income = st.number_input('Annual Income', min_value=0.0, step=1000.0)
        cibil_score = st.number_input('CIBIL Score', min_value=0, max_value=900)
        preferred_payment_method = st.selectbox('Preferred Payment Method', ['Credit Card', 'Debit Card', 'UPI'])
        frequency_of_card_usage = st.number_input('Frequency of Card Usage (per month)', min_value=0, step=1)
        loan_intent = st.selectbox('Loan Intent', ['Home', 'Personal', 'Education', 'Credit Card'])
        number_of_credit_cards_owned = st.number_input('Number of Credit Cards Owned', min_value=0)
        employment_length = st.number_input('Employment Length (in years)', min_value=0)
        financial_literacy_level = st.selectbox('Financial Literacy Level', ['Low', 'Medium', 'High'])
        bill_payment_timeliness = st.selectbox('Bill Payment Timeliness', ['On Time', 'Late'])
        insurance_coverage = st.selectbox('Insurance Coverage', ['Yes', 'No'])

    with col2:
        home_ownership = st.selectbox('Home Ownership', ['Own', 'Rent'])
        average_monthly_expenditure = st.number_input('Average Monthly Expenditure', min_value=0.0)
        atm_withdrawal_frequency = st.number_input('ATM Withdrawal Frequency (per month)', min_value=0)
        risk_appetite = st.selectbox('Risk Appetite', ['Low', 'Medium', 'High'])
        savings_habits = st.selectbox('Savings Habits', ['Poor', 'Good'])
        loan_amount = st.number_input('Loan Amount', min_value=0)
        number_of_bank_accounts = st.number_input('Number of Bank Accounts', min_value=0)
        outstanding_debts = st.number_input('Outstanding Debts', min_value=0)
        loan_status = st.selectbox('Loan Status', ['Paid', 'Unpaid'])
        number_of_missed_payments = st.number_input('Number of Missed Payments', min_value=0)
        late_payment_penalty = st.selectbox('Late Payment Penalty', ['Yes', 'No'])

    # Button to process inputs and display the recommendation
    if st.button('Get Recommendations'):
        # Store the inputs in session state
        st.session_state['inputs'] = {
            'age': age,
            'annual_income': annual_income,
            'cibil_score': cibil_score,
            'preferred_payment_method': preferred_payment_method,
            'frequency_of_card_usage': frequency_of_card_usage,
            'loan_intent': loan_intent,
            'number_of_credit_cards_owned': number_of_credit_cards_owned,
            'employment_length': employment_length,
            'financial_literacy_level': financial_literacy_level,
            'bill_payment_timeliness': bill_payment_timeliness,
            'insurance_coverage': insurance_coverage,
            'home_ownership': home_ownership,
            'average_monthly_expenditure': average_monthly_expenditure,
            'atm_withdrawal_frequency': atm_withdrawal_frequency,
            'risk_appetite': risk_appetite,
            'savings_habits': savings_habits,
            'loan_amount': loan_amount,
            'number_of_bank_accounts': number_of_bank_accounts,
            'outstanding_debts': outstanding_debts,
            'loan_status': loan_status,
            'number_of_missed_payments': number_of_missed_payments,
            'late_payment_penalty': late_payment_penalty
        }

        # Set flag to show recommendation and hide the form
        st.session_state['show_recommendation'] = True

# Function to display the recommendation based on user inputs
def show_recommendation():
    inputs = st.session_state['inputs']
    cibil_score = inputs['cibil_score']
    
    # Display the recommendation
    st.title('Your Recommendation')
    if cibil_score >= 650:
        st.success(f"Based on your profile, we recommend: {cluster_card_mapping[3]}")
    else:
        st.error("Your CIBIL score is too low for a credit card recommendation.")

# Show form or recommendation based on session state
if 'show_recommendation' in st.session_state and st.session_state['show_recommendation']:
    show_recommendation()
else:
    show_form()

# Footer
st.markdown('<footer>© 2024 Team Mutex Inc.</footer>', unsafe_allow_html=True)
