import argparse
import os

import pandas
import numpy


def write_output_file(output_file_name, input_dir):
    
    dfs = [] 
    counter = 0
    for file_name in os.listdir(input_dir):
        df = pandas.read_feather(os.path.join(input_dir, file_name))
        df.index = df["index"]
        df = df.drop(["index"], axis=1)
        dfs.append(df)
        counter += 1
        print(counter)
    merged_df = pandas.concat(dfs, join="inner", axis=1)
    merged_df = merged_df.reset_index()
    merged_df.to_feather(output_file_name)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir", required=True)
    parser.add_argument("--output-file", required=True)
    args = parser.parse_args()
	
    write_output_file(args.output_file, args.input_dir)

if __name__ == "__main__":
    main()
