import subprocess
import random
import os
import sys

algo = './' + sys.argv[1]
dataset = sys.argv[2]

print algo + ', ' + dataset

param_file = 'params'
train_algo = algo + '-learn'
test_algo = algo + '-test'

line_count = 0
dataset_lines = []
with open(dataset, 'r') as f_in:
    for line in f_in:
        line_count += 1
        dataset_lines.append(line)

train_size = (int)(0.7 * line_count)
test_size = (int)(0.3 * line_count)

# K-fold partitions
K = 10
k_fold_train_size = (int)(0.9 * train_size)
k_fold_test_size = (int)(0.1 * train_size)
k_fold_data = []

random.shuffle(dataset_lines)
fold = -1
for i in range(0, train_size):

    if i % k_fold_test_size == 0 or fold == -1:
        fold += 1
        k_fold_data.append([])

    # print dataset_lines[i]
    k_fold_data[fold].append(dataset_lines[i])

margin = [0.1, 0, 1, 10, 100, 200]
for m in margin:
    # making the folds
    test_error = 0.0
    for FOLD in range(0, K):
        current_train_file = 'train' + str(FOLD)
        current_test_file = 'test' + str(FOLD)

        with open(current_train_file, 'w') as f_out:
            for j in range(0, K):
                if j == FOLD:
                    continue
                else:
                    for e in k_fold_data[j]:
                        # print e, '\n'
                        f_out.write(e)

        with open(current_test_file, 'w') as f_out:
            for e in k_fold_data[FOLD]:
                f_out.write(e)

        # Train
        cmd = train_algo + " -c " + str(m) + " " + current_train_file + " " + param_file
        train_result = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        current_error = train_result.stdout.readlines()#[3].split()[3]

        # Test
        cmd = test_algo + " " + current_test_file + " " + param_file
        test_result = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        current_error = test_result.stdout.readlines()[3].split()[4]
        # print current_error
        test_error += float(current_error[:current_error.index('%')])

        os.remove(current_train_file)
        os.remove(current_test_file)
    print m, test_error / K
