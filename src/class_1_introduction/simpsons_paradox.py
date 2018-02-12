import csv

data = []

with open('Berkeley.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='|')

    # Ignore the header
    next(reader)

    for row in reader:
        result_application = row[0]
        gender = row[1]
        department = row[2]
        number_of_people = int(row[3])

        for i in range(0, number_of_people):
            person_data = {
                'gender': gender,
                'department': department,
                'admitted': result_application == "Admitted"
            }

            data.append(person_data)

departments = list(set([person['department'] for person in data]))
departments.sort()

genders = set([person['gender'] for person in data])

for department in departments:
    print('Department ' + department)

    for gender in genders:
        list_people_that_applied = list(filter(lambda person: person['gender'] == gender and person['department'] == department, data))
        list_people_admitted = list(filter(lambda person: person['admitted'], list_people_that_applied))

        percentage_admitted = (len(list_people_admitted) / len(list_people_that_applied)) * 100

        print(">> {} | Percentage admitted: {} %".format(gender, percentage_admitted))

    print('--------------')