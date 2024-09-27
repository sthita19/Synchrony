import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense

import pickle

# Load the dataset
df = pd.read_csv("data/realistic_credit_card_recommendation_dataset.csv")

# Handling ordinal variables
ordinal_mapping = {
    'Risk_Appetite': {'Low': 0, 'Medium': 1, 'High': 2},
    'Bill_Payment_Timeliness': {'On Time': 0, 'Late': 1},
    'Financial_Literacy_Level': {'Low': 0, 'Medium': 1, 'High': 2}
}

for col, mapping in ordinal_mapping.items():
    df[col] = df[col].map(mapping)

# One-Hot Encoding for nominal variables
nominal_columns = ['Home_Ownership', 'Loan_Intent', 'Loan_Status', 
                   'Preferred_Payment_Method', 'Insurance_Coverage', 
                   'Savings_Habits']
df = pd.get_dummies(df, columns=nominal_columns, drop_first=True)

# Feature selection
features = [ 'Preferred_Payment_Method_Credit Card',
    'Frequency_of_Card_Usage',
    'Home_Ownership_Rent',
    'Loan_Intent_Home',
    'CIBIL_Score',
    'Annual_Income',
    'Age',
    'Average_Monthly_Expenditure',
    'Loan_Intent_Credit Card',
    'Loan_Intent_Personal',
    'Loan_Intent_Education',
    'Loan_Amount',
    'ATM_Withdrawal_Frequency',
    'Risk_Appetite',
    'Savings_Habits_Poor',
    'Number_of_Credit_Cards_Owned',
    'Preferred_Payment_Method_Debit Card',
    'Employment_Length',
    'Financial_Literacy_Level',
    'Bill_Payment_Timeliness',
    'Number_of_Bank_Accounts',
    'Outstanding_Debts',
    'Loan_Status_Paid',
    'Number_of_Missed_Payments',
    'Late_Payment_Penalties',
    'Savings_Habits_Good',
    'Insurance_Coverage_1',
    'Preferred_Payment_Method_UPI' ]  # Your feature list

# Standardizing features
scaler = StandardScaler()
df_scaled = scaler.fit_transform(df[features])

# Build Autoencoder
input_dim = df_scaled.shape[1]
encoding_dim = 6
input_layer = Input(shape=(input_dim,))
encoded = Dense(encoding_dim, activation='relu')(input_layer)
decoded = Dense(input_dim, activation='sigmoid')(encoded)
autoencoder = Model(inputs=input_layer, outputs=decoded)
autoencoder.compile(optimizer='adam', loss='mse')

# Train Autoencoder
autoencoder.fit(df_scaled, df_scaled, epochs=50, batch_size=256, shuffle=True, verbose=1)

# Extract the encoder
encoder = Model(inputs=input_layer, outputs=encoded)
df_compressed = encoder.predict(df_scaled)

# K-Means Clustering
n_clusters = 8
kmeans = KMeans(n_clusters=n_clusters, random_state=42)
df['Cluster'] = kmeans.fit_predict(df_compressed)

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
}  # Your mapping here

# Assign credit cards
df['Assigned_Credit_Card'] = df['Cluster'].map(cluster_card_mapping)
df.loc[df['CIBIL_Score'] < 600, 'Assigned_Credit_Card'] = None

# Save models
with open('kmeans_model.pkl', 'wb') as f:
    pickle.dump(kmeans, f)

with open('scaler.pkl', 'wb') as f:
    pickle.dump(scaler, f)

with open('encoder.pkl', 'wb') as f:
    pickle.dump(encoder, f)

print("Models saved.")
