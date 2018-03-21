""" Official evaluation script for v1.1 of the SQuAD dataset. """
from __future__ import print_function
from collections import Counter
import string
import re
import argparse
import json
import sys


def normalize_answer(s):
    """Lower text and remove punctuation, articles and extra whitespace."""
    def remove_articles(text):
        return re.sub(r'\b(a|an|the)\b', ' ', text)

    def white_space_fix(text):
        return ' '.join(text.split())

    def remove_punc(text):
        exclude = set(string.punctuation)
        return ''.join(ch for ch in text if ch not in exclude)

    def lower(text):
        return text.lower()

    return white_space_fix(remove_articles(remove_punc(lower(s))))


def f1_score(prediction, ground_truth):
    prediction_tokens = normalize_answer(prediction).split()
    ground_truth_tokens = normalize_answer(ground_truth).split()
    common = Counter(prediction_tokens) & Counter(ground_truth_tokens)
    num_same = sum(common.values())
    if num_same == 0:
        return 0
    precision = 1.0 * num_same / len(prediction_tokens)
    recall = 1.0 * num_same / len(ground_truth_tokens)
    f1 = (2 * precision * recall) / (precision + recall)
    return f1


def exact_match_score(prediction, ground_truth):
    return (normalize_answer(prediction) == normalize_answer(ground_truth))


def metric_max_over_ground_truths(metric_fn, prediction, ground_truths):
    scores_for_ground_truths = []
    for ground_truth in ground_truths:
        score = metric_fn(prediction, ground_truth)
        scores_for_ground_truths.append(score)
    return max(scores_for_ground_truths)


def evaluate(dataset, predictions):
    f1 = exact_match = total = 0
    for article in dataset:
        for paragraph in article['paragraphs']:
            for qa in paragraph['qas']:
                total += 1
                if qa['id'] not in predictions:
                    message = 'Unanswered question ' + qa['id'] + \
                              ' will receive score 0.'
                    print(message, file=sys.stderr)
                    continue
                ground_truths = list(map(lambda x: x['text'], qa['answers']))
                prediction = predictions[qa['id']]
                exact_match += metric_max_over_ground_truths(
                    exact_match_score, prediction, ground_truths)
                f1 += metric_max_over_ground_truths(
                    f1_score, prediction, ground_truths)

    exact_match = 100.0 * exact_match / total
    f1 = 100.0 * f1 / total

    return {'exact_match': exact_match, 'f1': f1}


def evaluate2(dataset, predictions):
    f1 = exact_match = total = 0
    f1_who = exact_match_who = total_who = 0
    f1_when = exact_match_when = total_when = 0
    f1_where = exact_match_where = total_where = 0
    f1_why = exact_match_why = total_why = 0
    f1_what = exact_match_what = total_what = 0
    f1_which = exact_match_which = total_which = 0
    f1_how = exact_match_how = total_how = 0
    for article in dataset:
        for paragraph in article['paragraphs']:
            for qa in paragraph['qas']:
                total += 1
                if qa['id'] not in predictions:
                    message = 'Unanswered question ' + qa['id'] + \
                              ' will receive score 0.'
                    print(message, file=sys.stderr)
                    continue
                ground_truths = list(map(lambda x: x['text'], qa['answers']))
                prediction = predictions[qa['id']]
                question = qa['question']
                if metric_max_over_ground_truths(
                        exact_match_score, prediction, ground_truths) == 0:
                    print(question, qa['answers'][0]['text']," | ", prediction)
                exact_match += metric_max_over_ground_truths(
                    exact_match_score, prediction, ground_truths)
                f1 += metric_max_over_ground_truths(
                    f1_score, prediction, ground_truths)
                if "who" in question or "Who" in question or "whom" in question:
                    exact_match_who += metric_max_over_ground_truths(
                        exact_match_score, prediction, ground_truths)
                    f1_who += metric_max_over_ground_truths(
                        f1_score, prediction, ground_truths)
                    total_who += 1
                elif "when" in question or "When" in question:
                    exact_match_when += metric_max_over_ground_truths(
                        exact_match_score, prediction, ground_truths)
                    f1_when += metric_max_over_ground_truths(
                        f1_score, prediction, ground_truths)
                    total_when += 1
                elif "where" in question or "Where" in question:
                    exact_match_where += metric_max_over_ground_truths(
                        exact_match_score, prediction, ground_truths)
                    f1_where += metric_max_over_ground_truths(
                        f1_score, prediction, ground_truths)
                    total_where += 1
                elif "why" in question or "Why" in question:
                    exact_match_why += metric_max_over_ground_truths(
                        exact_match_score, prediction, ground_truths)
                    f1_why += metric_max_over_ground_truths(
                        f1_score, prediction, ground_truths)
                    total_why += 1
                elif "what" in question or "What" in question:
                    exact_match_what += metric_max_over_ground_truths(
                        exact_match_score, prediction, ground_truths)
                    f1_what += metric_max_over_ground_truths(
                        f1_score, prediction, ground_truths)
                    total_what += 1
                elif "which" in question or "Which" in question:
                    exact_match_which += metric_max_over_ground_truths(
                        exact_match_score, prediction, ground_truths)
                    f1_which += metric_max_over_ground_truths(
                        f1_score, prediction, ground_truths)
                    total_which += 1
                elif "how" in question or "How" in question:
                    exact_match_how += metric_max_over_ground_truths(
                        exact_match_score, prediction, ground_truths)
                    f1_how += metric_max_over_ground_truths(
                        f1_score, prediction, ground_truths)
                    total_how += 1

    exact_match = 100.0 * exact_match / total
    f1 = 100.0 * f1 / total
    exact_match_who = 100.0 * exact_match_who / total_who
    f1_who = 100.0 * f1_who / total_who
    exact_match_when = 100.0 * exact_match_when / total_when
    f1_when = 100.0 * f1_when / total_when
    exact_match_where = 100.0 * exact_match_where / total_where
    f1_where = 100.0 * f1_where / total_where
    # exact_match_why = 100.0 * exact_match_why / total_why
    # f1_why = 100.0 * f1_why / total_why
    exact_match_how = 100.0 * exact_match_how / total_how
    f1_how = 100.0 * f1_how / total_how
    exact_match_what = 100.0 * exact_match_what / total_what
    f1_what = 100.0 * f1_what / total_what
    exact_match_which = 100.0 * exact_match_which / total_which
    f1_which = 100.0 * f1_which / total_which

    return {'exact_match': exact_match, 'f1': f1,
            'exact_match_who': exact_match_who, 'f1_who': f1_who,
            'exact_match_when': exact_match_when, 'f1_when': f1_when,
            'exact_match_where': exact_match_where, 'f1_where': f1_where,
            # 'exact_match_why': exact_match_why, 'f1_why': f1_why,
            'exact_match_how': exact_match_how, 'f1_how': f1_how,
            'exact_match_what': exact_match_what, 'f1_what': f1_what,
            'exact_match_which': exact_match_which, 'f1_which': f1_which,
            }

if __name__ == '__main__':
    expected_version = '1.1'
    parser = argparse.ArgumentParser(
        description='Evaluation for SQuAD ' + expected_version)
    parser.add_argument('dataset_file', help='Dataset file')
    parser.add_argument('prediction_file', help='Prediction File')
    args = parser.parse_args()
    with open(args.dataset_file) as dataset_file:
        dataset_json = json.load(dataset_file)
        if (dataset_json['version'] != expected_version):
            print('Evaluation expects v-' + expected_version +
                  ', but got dataset with v-' + dataset_json['version'],
                  file=sys.stderr)
        dataset = dataset_json['data']
    with open(args.prediction_file) as prediction_file:
        predictions = json.load(prediction_file)
    print(json.dumps(evaluate(dataset, predictions)))
