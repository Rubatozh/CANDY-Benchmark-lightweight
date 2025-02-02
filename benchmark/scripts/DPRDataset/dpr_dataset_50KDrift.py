import numpy as np
import random
from dpr_dataset_generate import generate_dpr_embeddings, generate_dpr_embeddings_with_word_pollution, append_fvecs
import nltk
import os

if __name__ == "__main__":
    # This is an example script to generate the DPR dataset, containing 10M base vector embeddings and 10k queries, used
    # in the paper "Similarity search in the blink of an eye with compressed indices", Aguerrebere, C.; Bhati I.;
    # Hildebrand M.; Tepper M.; Willke T.
    #
    # Please see the documentation of the generate_dpr_embeddings function for details on the required parameters.
    #
    # The dataset was generated using text snippets from the files in the "en" (305GB) variant of the C4 dataset
    # available at: https://huggingface.co/datasets/allenai/c4
    # We used files c4-train.00000-of-01024.json.gz and c4-train.00001-of-01024.json.gz in the train folder (c4/en/train)
    # to generate the base vectors, and file c4-validation.00000-of-00008.json in the validation folder
    # (c4/en/validation/) to generate the queries.
    #
    # The output .fvecs file with the generated embeddings is located at {dataset_dir}/embeddings and the filename
    # is given by: {fname_prefix_out}_queries_{int(num_embd / 1000)}k_files{init_file}_{init_file+number_of_files}.fvecs

    base_C4_folder = 'c4/en'  # Set this path to where your c4/en folder is located
    cache_folder = f'.cache/huggingface/datasets/'  # Set to the hugginface datasets cache path

    doc_stride = 32
    max_length = 64
    dim = 768
    fname_prefix_out = 'c4-raw'

    np.random.seed(0)
    random.seed(0)

    ## --- Base vectors generation ----
    # Generate 1K base vectors and save them to a .fvecs file in dataset_dir/embeddings. The function fvecs_read in
    # dpr_dataset_generate.py can be used to read the .fvecs files.
    dataset_dir = f'{base_C4_folder}/'
    num_embd = 50000
    batch_size = 512
    init_file = 0
    number_of_files = 1  # Make sure the input files (2 in this case) are enough to generate the requested number of embeddings.
    # For a fast estimate, use the optional parameter get_total_embeddings_only to get the number
    # of embeddings that can be generated from a certain group of files without actually generating
    # the embeddings.
    if (os.path.exists("DPR50KDriftBegin.fvecs") == False):
        generate_dpr_embeddings(init_file, number_of_files, num_embd, doc_stride, max_length, dim,
                                batch_size,
                                dataset_dir, fname_prefix_out, cache_folder)
        os.system("cp " + dataset_dir + "/embeddings/" + fname_prefix_out + "*.fvecs " + "DPR50KDriftBegin.fvecs")
    if (os.path.exists("DPR50KDriftEnd.fvecs") == False):
        init_file = 1
        fname_prefix_out = 'c4-drift-pollute'
        generate_dpr_embeddings_with_word_pollution(init_file, number_of_files, num_embd, doc_stride, max_length, dim,
                                                    batch_size,
                                                    dataset_dir, fname_prefix_out, cache_folder, 'Covid19', 0.3)
        os.system("cp " + dataset_dir + "/embeddings/" + fname_prefix_out + "*.fvecs " + "DPR50KDriftEnd.fvecs")
    append_fvecs("DPR50KDriftEnd.fvecs", "DPR50KDriftBegin.fvecs", "DPR100KDrift.fvecs")
    ## --- Query vectors generation ----
    # Generate 10k query vectors and save them to a .fvecs file in dataset_dir/embeddings. The function fvecs_read in
    # dpr_dataset_generate.py can be used to read the .fvecs files.
