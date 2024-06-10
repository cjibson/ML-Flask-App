import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

pd.set_option('display.max_columns', None)
filepath = 'C:\\Users\\jibso\\OneDrive\\Desktop\\ml-flask-app\\ML-Flask-App\\app\\ml_scripts\\lung_cancer_statistics\\lung_cancer_data.csv'

def load_data(filepath):
    #Read in file
    df = pd.read_csv(filepath)
    return df

def preprocess_data(df):
    #Drop unnecessary columns and rows
    df = df.drop(['Performance_Status', 'Insurance_Type', 'Patient_ID'], axis=1)
    df = df.dropna()

    #Separate data into categories: patient/demographic data, comorbidity data, and bloodwork data
    pt_df = df[['Age', 'Gender', 'Smoking_History', 'Tumor_Size_mm', 'Tumor_Location', 
                    'Treatment', 'Ethnicity', 'Family_History', 'Smoking_Pack_Years']]

    cm_df = df[['Survival_Months', 'Comorbidity_Diabetes', 'Comorbidity_Hypertension', 
                'Comorbidity_Heart_Disease', 'Comorbidity_Chronic_Lung_Disease', 
                'Comorbidity_Kidney_Disease', 'Comorbidity_Autoimmune_Disease', 'Comorbidity_Other']]

    bw_df = df[['Stage', 'Blood_Pressure_Systolic', 'Blood_Pressure_Diastolic', 'Blood_Pressure_Pulse',
                'Hemoglobin_Level', 'White_Blood_Cell_Count', 'Platelet_Count', 'Albumin_Level',
                'Alkaline_Phosphatase_Level', 'Alanine_Aminotransferase_Level',
                'Aspartate_Aminotransferase_Level', 'Creatinine_Level', 'LDH_Level', 'Calcium_Level',
                'Phosphorus_Level', 'Glucose_Level', 'Potassium_Level', 'Sodium_Level']]

    #Get dummy variables for necessary columns in comorbidity data
    cm_df = pd.get_dummies(cm_df, columns=['Comorbidity_Diabetes', 'Comorbidity_Hypertension', 
                                           'Comorbidity_Heart_Disease', 'Comorbidity_Chronic_Lung_Disease',
                                           'Comorbidity_Kidney_Disease', 'Comorbidity_Autoimmune_Disease',
                                           'Comorbidity_Other'])
    cm_df = cm_df.astype(int)
    
    return pt_df, cm_df, bw_df

def analyze_pt_data(pt_df):
    #Analyze patient data
    print("Descriptive statistics for numerical patient data:\n")
    print(pt_df.describe())

    #List for categorical variables
    categorical_variables = ['Gender', 'Smoking_History', 'Tumor_Location', 'Treatment', 'Ethnicity', 
                             'Family_History']
    
    print("\nValue Counts for categorical variables:")
    #Print value counts for categorical variables
    for variable in categorical_variables:
        print('-----------------------------')
        print(pt_df.value_counts(variable))
    print('-----------------------------')

#Call functions
df = load_data(filepath)
pt_df, cm_df, bw_df = preprocess_data(df)
analyze_pt_data(pt_df)

# print('Data frame:')
# print(pt_df)