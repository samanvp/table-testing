import argparse
import os

import h5py
import numpy


def get_output_info(input_dir, hstack=True):
    
    num_files_to_merge = len(os.listdir(input_dir))

    h5_file = h5py.File(os.path.join(input_dir, os.listdir(input_dir)[0]), 'r')
    data_dims = h5_file["data"].shape
    compression = h5_file["data"].compression
    compression_opts = h5_file["data"].compression_opts
    
    if hstack:
        output_dims = (data_dims[0], data_dims[1]*num_files_to_merge)
    else:
        output_dims = (data_dims[0]*num_files_to_merge, data_dims[1])
    return {"shape": output_dims,
            "compression": compression,
            "compression_opts": compression_opts}

def write_output_file(output_file_name, input_dir, hstack):
    
    output_info = get_output_info(input_dir, hstack)

    output_file = h5py.File(output_file_name, 'w')
    output_file.create_dataset(
        name="data",
        shape=output_info["shape"],
        compression=output_info["compression"],
        compression_opts=output_info["compression_opts"],
        dtype=numpy.dtype(numpy.int32))
    output_file.create_dataset(
        name="cell_names",
        shape=(output_info["shape"][1],),
        dtype=h5py.special_dtype(vlen=bytes))
    output_file.create_dataset(
        name="gene_names",
        shape=(output_info["shape"][0],),
        dtype=h5py.special_dtype(vlen=bytes))

    for i, file_name in enumerate(os.listdir(input_dir)):
        print(i, file_name)
        h5_file = h5py.File(os.path.join(input_dir, file_name), "r")
        data = h5_file["data"]
        if hstack:
            output_file["data"][:, i] = data[...].flatten()
        else:
            output_file["data"][i, :] = data[...].flatten()
    output_file.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir", required=True)
    parser.add_argument("--output-file", required=True)
    parser.add_argument("--vstack", action='store_true')
    args = parser.parse_args()
	
    write_output_file(args.output_file, args.input_dir, not args.vstack)

if __name__ == "__main__":
    main()
