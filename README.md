# table-testing

This repository provides a collaborative space to specify requirements, examples, and tests for on-disk file formats used to store expression matrices arising from single-cell RNA sequencing analyses. There are currently a wide variety of formats used for these data, including generic formats (e.g. CSV) and those designed specifically for this domain (e.g. Loom). 

Please open an issue or make a PR if you'd like to add ideas or start a discussion!

Associated documents that inform this repo can be found in this [Google Drive](https://drive.google.com/drive/u/0/folders/1D___JK5hnlc5A3Qhkp5LrZgiYycvsd_2) and are linked throughout the repository.

We meet from time to time, here are our [meeting notes](https://docs.google.com/document/d/1v0NSeML2F6JRuLrjXm7Kprh-BiamnpiODqHHpBnituY/edit), feel free to reach out and join!

## Goals

- Catalog the requirements that existing or future formats may or may not satisfy
- Provide example datasets and loading scripts (cross language) for these examples
- Provide test suites that evaluate performance of formats against requirements

## Requirements

In many discussions, requirements fall broadly into two categories, archival (long-term storage) and analysis (daily use with analytical software in e.g. R or Python). As written, some of these are explicit requirements (e.g. self-describing), whereas others are dimensions along which different formats vary (e.g. size and speed).

#### Archival
- Long-term abilily to read and parse the file (does it depend on APIs or language-features that are likely to change?)
- Self-describing (are the semantics of the file contained within it?)
- Size (especially after compression)

#### Analysis
- Partial IO (can portions of the file be read without loading the whole thing?)
  - Loading subsets of genes (e.g. fitting a regression model to each gene in parallel)
  - Loading subsets of cells (e.g. for differential expression)
  - Making arbitrary byte-range queries (e.g. for a web service)
- Speed of reading and writing data
- Storing additional metadata or features alongide primary table (e.g. derived features or auxillery measurements)
- Optomized for sparsity (affects both speed and size)
- Ability to handle large numbers of cells (e.g. out-of-memory, memory mapping, etc.)

## Formats

Here we list formats that have been used or proposed thus far in the community (please add!):
- `.csv` (also includes TSV)
- `.mat` (matlab)
- `.mtx` (matrix market)
- `.h5` (HDF5)
- `.h5ad` (a wrapped of HDF5 used by `scanpy`)
- `.loom` (a wrapper of `.h5`)
- `.npy` (serialized `numpy` matrices)
- `.arrow` (not currently used but potentially promising)
- `.Robj` (serialized R objects, e.g. from Seurat)
- `.zarr` [(chunked, compressed, N-dimensional arrays, python)](http://zarr.readthedocs.io/en/stable/index.html)

## Standard Matrices

We benchmark data formats and APIs on standard matrices. These matrices are found in the public S3 bucket `matrix-format-test-data`.

That bucket has two relevant folders, `matrices` and `sources`. The `sources` folder contains raw data from a number of different data sources, in the form that they were originally delivered. These are meant to span a range of matrix sizes and properties so we can develop tests for diverse use cases:

| Source Name | Description |
| ----------- | ----------- |
| tenx_mouse_neuron_1M | The 1.3 million mouse neuron dataset released by 10x. |
| tenx_mouse_neuron_20k | A sample of 20k cells from the 1.3 million cell dataset, also provided by 10x. |
| immune_cell_census_cord_blood | Cord blood cells from the Immune Cell Atlas dataset released for the HCA preview. 384,000 cells sequenced with 10x.|
| immune_cell_census_bone_marrow | Bone marrow cells from the Immune Cell Atlas dataset released for the HCA preview. 378,000 cells sequenced with 10x. |
| GSE84465_whole | 3589 cells sequenced with SmartSeq2 from GEO Series GSE84465. |
| GSE84465_split | 3589 cells sequenced with SmartSeq2 from GEO Series GSE84465, split so there is one matrix file per cell. |

The `matrices` folder contains two levels of subfolders. The first is the matrix format. These are the formats that are being tested for performance among a set of different tasks.

| Format Name | Description |
| ----------- | ----------- |
| anndata | The HDF5-based format used by [scanpy](https://github.com/theislab/scanpy) |
| feather | [Feather format](https://github.com/wesm/feather) |
| hdf5_10000_10000_chunks_3_compression | Dense matrix in an HDF5 dataset with (10000, 10000) chunks and gzip=3 compression |
| hdf5_1000_1000_chunks_3_compression | Dense matrix in an HDF5 dataset with (1000, 1000) chunks and gzip=3 compression |
| hdf5_25000_25000_chunks_3_compression | Dense matrix in an HDF5 dataset with (25000, 25000) chunks and gzip=3 compression |
| loom | [Loom format](http://loompy.org/) |
| parquet | [Parquet format](https://parquet.apache.org/) |
| sparse_hdf5_csc | Compressed Sparse Column matrix in HDF5, similar to what is produced by Cell Ranger |
| sparse_hdf5_csr | Compressed Sparse Row matrix in HDF5 |
| zarr_10000_10000 | [Zarr](https://zarr.readthedocs.io/en/stable/) Directory Store with (10000, 10000) chunks |
| zarr_1000_1000 | [Zarr](https://zarr.readthedocs.io/en/stable/) Directory Store with (1000, 1000) chunks |
| zarr_25000_25000 | [Zarr](https://zarr.readthedocs.io/en/stable/) Directory Store with (25000, 25000) chunks |

The next level of subfolder is the sources, which are detailed above. So for example, `s3://matrix-format-test-data/matrices/anndata/immune_cell_census_bone_marrow/anndata_immune_cell_census_bone_marrow.h5ad` is the Immune Cell Atlas bone marrow data converted into the scanpy anndata format.

## Test suite

Given [use cases](https://docs.google.com/document/d/1Vu0AJfV9N27hhcanRkrTcxP676ff-1qMuujrSs8jky8/edit#), we have collected we are creating a test suite to benchmark file formats contained in this project.

[TODO Add details on test suite]

[TODO Add details on extending test suite to new use cases]

[TODO Add detials on extending test suite to new file formats]

[TODO Add details on extending test suite to new data sets]

Fell free to contribute!
