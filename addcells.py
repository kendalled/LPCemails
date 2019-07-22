import unicodecsv as csv

reader = csv.reader(open('merged.csv', 'rb'))
writer = csv.writer(open('output.csv', 'w'))
headers = reader.next()
headers.append("City", "State")
writer.write(headers)
for row in reader:
    row.append(new data for my new header)
    writer.writerow(row)
