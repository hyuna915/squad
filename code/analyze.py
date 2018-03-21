import os


def count_answers(filename):
    map = {}
    count = 0
    with open(filename) as fin:
        for line in fin:
            words = line.split(' ')
            start = int(words[0])
            end = int(words[1])
            len = end - start + 1
            count += 1
            if len in map:
                map[len] += 1
            else:
                map[len] = 1
    return map, count


def print_map(map, count):
    account = 0
    for k, v in map.iteritems():
        account += v
        print k, v, account * 1.0 / count


def count_answer_len():
    map, count = count_answers('/Users/hyuna915/Desktop/2018-CS224N/squad/data/train.span')
    print_map(map, count)


def count_context_length(filename):
    map = {}
    count = 0
    with open(filename) as fin:
        for line in fin:
            words = line.split(' ')
            length = len(words)
            count += 1
            if length in map:
                map[length] += 1
            else:
                map[length] = 1
    return map, count

def print_context_length(map, count):
    account = 0
    for k, v in map.iteritems():
        account += v
        print k, v, account * 1.0 / count

def count_context_len():
    map, count = count_context_length('/Users/hyuna915/Desktop/2018-CS224N/squad/data/train.context')
    print_context_length(map, count)

def filter_result_out():
    with open(args.dataset_file) as dataset_file:
        dataset_json = json.load(dataset_file)
        dataset = dataset_json['data']
        for article in dataset: