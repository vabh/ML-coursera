dataset = 'breast_cancer.data'

data_array = []
rows = 0
with open(dataset, 'r') as f_in:
    for line in f_in:
        rows += 1
        data = line.split()
        data_array.append(data)

for i in range(1, len(data_array[0])):  # leave the first col, class label

    max = float(data_array[0][i])
    for j in range(rows):
        if data_array[j][i] == '?':
            data_array[j][i] = 0.0
        if float(data_array[j][i]) > max:
            max = float(data_array[j][i])

    print max
    if max != 0:
        for j in range(rows):
            data_array[j][i] = float(data_array[j][i]) / max

with open(dataset + 'norm', 'a') as f_out:
    for i in range(rows):
        f_out.write(' '.join(str(e) for e in data_array[i]))
        f_out.write('\n')
