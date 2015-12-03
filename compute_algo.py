import subprocess
import random
import os
import sys

algo = './'+sys.argv[1]
dataset = sys.argv[2]

print algo + ', ' + dataset
#dataset = 'ionosphere' + '.data'
#dataset = 'breast_cancer' + '.data'
#dataset = 'spambase' + '.data'
# dataset = 'letter-recog' + '.data'

train_file = dataset + '-train'
test_file = dataset + '-test'

param_file = 'params'

# algo = './LogisticRegression'
# algo = './perceptron'
#algo = './adaline'
#algo = './AdaBoost'

test_error = 0.0
train_error = 0.0

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


for iters in range(0, 20):
    num = str(iters)

    current_train_file = train_file + '-' + num
    current_test_file = test_file + '-' + num

    random.shuffle(dataset_lines)

    with open(current_train_file, 'w') as f_out:
        for i in range(0, train_size):
            f_out.write(dataset_lines[i])

    with open(current_test_file, 'w') as f_out:
        for i in range(train_size, train_size + test_size):
            f_out.write(dataset_lines[i])

    # train_result = subprocess.call(
        # [train_algo, "-a", "0.000001", current_train_file, param_file])
    # test_result = subprocess.check_output([test_algo, current_test_file,
    # param_file], shell=True)

    # train
    cmd = train_algo + " -r 5 " + current_train_file + " " + param_file
    train_result = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)

    current_error = train_result.stdout.readlines()#[3].split()[3]
    # print current_error
    # train_error += float(current_error[current_error.index('=') + 1:])

    # test
    cmd = test_algo + " " + current_test_file + " " + param_file
    test_result = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)

    current_error = test_result.stdout.readlines()[1].split()[3]
    test_error += float(current_error[current_error.index('=') + 1:])
    print current_error
    print

    os.remove(current_train_file)
    os.remove(current_test_file)

print
print "Train error:", train_error / 20
print "Test error:", test_error / 20
