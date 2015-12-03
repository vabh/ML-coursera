import sys

dataset = sys.argv[1]
print dataset

rows = []
with open(dataset, 'r') as f_in:
    for line in f_in:
        rows.append(line.split())


for row in rows:
    row_data = []
    row_data.append(row[0])
    for i in range(1, len(row)):
        if row[i] != '0' and row[i] != '0.0':
            row_data.append(str(i) + ':' + row[i])
    with open(dataset + '_svm', 'a') as f_out:
        f_out.write(' '.join(row_data))
        f_out.write('\n')
