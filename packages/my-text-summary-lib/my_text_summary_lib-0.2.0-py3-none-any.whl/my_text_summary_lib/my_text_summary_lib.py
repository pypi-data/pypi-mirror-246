"""
This library provides functions for summarizing text 
and identifying outliers in a CSV file.
"""
import pandas as pd
from scipy import stats

import nltk
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from nltk.tokenize.treebank import TreebankWordDetokenizer
from nltk.tokenize import word_tokenize, sent_tokenize

nltk.download('punkt')
nltk.download('stopwords')


def summarize_text(file_path):
    """
    Generates a summary of the text in the given file.

    Parameters:
        file_path (str): The path to the file containing the text.

    Returns:
        str: The summary of the most common words in the text.
    """

    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    sentences = sent_tokenize(text)
    print(sentences)
    words = word_tokenize(text)

    stop_words = set(stopwords.words('english'))
    filtered_words = [word.lower() for word in words if word.isalnum() 
                      and word.lower() not in stop_words]

    freq_dist = FreqDist(filtered_words)
    most_common_words = freq_dist.most_common(5)

    summary = TreebankWordDetokenizer().detokenize(
        [word for word, _ in most_common_words])

    return summary


def identify_outliers(csv_file_path, column_name,
                      output_file_path='outliers.txt'):
    """
    Identify outliers in a given CSV file based on a specified column.
    Parameters:
        csv_file_path (str): The path to the CSV file.
        column_name (str): The name of the column to be analyzed.
        output_file_path (str, optional): The path to the output file.
        Defaults to 'outliers.txt'.
    Returns:
        list: A list of identified outliers.

    """
    data = pd.read_csv(csv_file_path)
    # Extract the specified column
    column_data = data[column_name]
    # Calculate the Z-scores for the data
    z_scores = stats.zscore(column_data)
    # Identify outliers based on the threshold
    threshold = 3
    outlier_indices = list(filter(lambda i: abs(z_scores[i]) > threshold,
                                  range(len(z_scores))))
    outliers = column_data[outlier_indices]

    # Save details of identified outliers to the output file
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        output_file.write("Original Data:\n")
        output_file.write(str(data) + "\n\n")
        output_file.write("Z-Scores:\n")

        print(nltk.__file__)
        output_file.write(str(z_scores) + "\n\n")
        output_file.write("Identified Outliers:\n")
        output_file.write(str(outliers.tolist()) + "\n")

    return outliers.tolist()
