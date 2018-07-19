import pandas as pd
import pprint

df = pd.read_csv('Berkeley.csv')

# print(df)

percentage_admission_per_department = {}

list_departments = df['Dept'].unique()

for dept in list_departments:
    males_department = df[(df['Dept'] == dept) & (df['Gender'] == 'Male')]

    number_males_admitted = males_department[males_department['Admit'] == 'Admitted']['Freq'].values[0]
    number_males_rejected = males_department[males_department['Admit'] == 'Rejected']['Freq'].values[0]

    females_department = df[(df['Dept'] == dept) & (df['Gender'] == 'Female')]

    number_females_admitted = females_department[females_department['Admit'] == 'Admitted']['Freq'].values[0]
    number_females_rejected = females_department[females_department['Admit'] == 'Rejected']['Freq'].values[0]

    percentage_admission_per_department[dept] = {
        'male_percentage_admission': (number_males_admitted / (number_males_admitted + number_males_rejected)) * 100,
        'female_percentage_admission': (number_females_admitted / (number_females_admitted + number_females_rejected)) * 100,
    }



pp = pprint.PrettyPrinter(indent=4)

pp.pprint(percentage_admission_per_department)
