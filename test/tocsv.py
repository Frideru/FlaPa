import csv

# пишем
with open('flat_club.csv', 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=' ', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    spamwriter.writerow(['Улица'] + ['№ Дома'] + ['Год 123'] + ['Ссылка'] + ['Этаж'] + ['Этажей'] + ['Общая'] + ['Кухня'] + ['Комната'] + ['с\узел'] + ['Потолок'] + ['Лоджия'] + ['Ремонт'] + ['Стоимость'] + ['Телефон'] + ['Имя'])
    spamwriter.writerow(['Spam', 'Lovely Spam', 'Wonderful Spam'])

# читаем что получилось
with open('flat_club.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in spamreader:
        print(', '.join(row))