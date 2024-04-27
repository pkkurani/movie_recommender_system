import pickle


# Function to split a pickle file into two
def split_pickle(input_file, output_file1, output_file2):
    with open(input_file, 'rb') as f:
        data = pickle.load(f)

    half_length = len(data) // 2
    data1 = data[:half_length]
    data2 = data[half_length:]

    with open(output_file1, 'wb') as f:
        pickle.dump(data1, f)

    with open(output_file2, 'wb') as f:
        pickle.dump(data2, f)


# Function to combine two pickle files into one
def combine_pickles(input_file1, input_file2, output_file):
    with open(input_file1, 'rb') as f1, open(input_file2, 'rb') as f2:
        data1 = pickle.load(f1)
        data2 = pickle.load(f2)

    combined_data = data1 + data2

    with open(output_file, 'wb') as f:
        pickle.dump(combined_data, f)


# Usage
input_file = 'similarity_tfidf.pkl'
output_file1 = 'split_file1.pkl'
output_file2 = 'split_file2.pkl'

split_pickle(input_file, output_file1, output_file2)

# # Later, to combine the split files
# combined_output_file = 'combined_big_pickle_file.pkl'
# combine_pickles(output_file1, output_file2, combined_output_file)
