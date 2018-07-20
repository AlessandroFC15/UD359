import pandas as pd
import pprint
import plotly.offline
import plotly.graph_objs as go

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

# list_departments = sorted(percentage_admission_per_department.keys())

women_admissions_per_department = [percentage_admission_per_department[dept]['female_percentage_admission'] for dept in list_departments]
men_admissions_per_department = [percentage_admission_per_department[dept]['male_percentage_admission'] for dept in list_departments]

trace1 = go.Bar(
    x=list_departments,
    y=men_admissions_per_department,
    name='Men',
    marker=dict(color='rgb(38, 144, 201)')
)
trace2 = go.Bar(
    x=list_departments,
    y=women_admissions_per_department,
    name='Women',
    marker=dict(color='rgb(255, 150, 232)')
)

data = [trace1, trace2]
layout = go.Layout(
    title='Admission Percentage per Department',
    barmode='group'
)

fig = go.Figure(data=data, layout=layout)
plotly.offline.plot(fig, filename='grouped-bar')