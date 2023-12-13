'''
Function to generate features of a list of mutant peptides, using their
position-dependent distances from the index peptide,
based on a given AA distance matrix.

Index peptide can be a string (common for all mutants) or a list (potentially
different for all mutants) with length equal to that of mutant list. All input 
sequences must have equal length.

AA matrix can be the name of a stored matrix (e.g., "BLOSUM100"), or be custom 
defined. Custom AA matrix must be a 20-by-20 Pandas Dataframe object 
with AAs as row and column names.

'''

def generate_mutant_features(index_peptide, # Single index peptide or list 
                 mutant_peptide_list, #List of mutant peptide sequences
                 aa_matrix): #Named or user-defined AA matrix   
    
    import pandas as pd
    import numpy as np
    import sys
    import os
    
    #AA names
    amino_acid_list=['A','C','D','E','F','G','H','I','K','L','M','N','P','Q','R',
                     'S','T','V','W','Y']
    
    # Check if mutant peptide list is a list
    if (isinstance(mutant_peptide_list,list) == False):
        sys.exit("Mutant peptides must be supplied as a list")
        
    # Check if there is only one index or as many as mutants
    if ((isinstance(index_peptide, str)==False) and 
        (len(mutant_peptide_list)!=len(index_peptide))):
        sys.exit("Supply either a unique index peptide or one for each mutant")
     
    # Check if index peptides form a list
    if ((isinstance(index_peptide, str)==False) and 
        ((isinstance(index_peptide,list) == False))):
        sys.exit("More than one index peptide must be supplied as a list")
        
    
    # Check if all mutants and index peptides have the same length
    if isinstance(index_peptide, str): #One index peptide provided
        if len(np.unique(np.char.str_len([index_peptide]+mutant_peptide_list)))!=1:
            sys.exit("All index and mutant sequences must have equal length")
    else: #Index peptide list provided
        if len(np.unique(np.char.str_len(index_peptide+mutant_peptide_list)))!=1:
            sys.exit("All index and mutant sequences must have equal length")
    
    
    
    # Check if input sequences contain non-AA and wildcard characters
    if isinstance(index_peptide, str): #One index peptide provided
        if set(list("".join(([index_peptide] +
                             mutant_peptide_list)))).issubset(
                                 set(amino_acid_list)) == False:
           sys.exit("Discard sequences with non-AA characters, including X and *")
    else: #Index peptide list provided
        if set(list("".join((index_peptide +
                             mutant_peptide_list)))).issubset(
                                 set(amino_acid_list)) == False:
           sys.exit("Discard sequences with non-AA characters, including X and *")        
    
    
    
    # If AA matrix provided, check size is 20-by-20 and it has row and column names
    if isinstance(aa_matrix, str)==False: #Name of AA matrix not provided
        if ((isinstance(aa_matrix, pd.DataFrame) == False) or
            (aa_matrix.shape != (20,20)) or
            (set(aa_matrix.index) != set(amino_acid_list)) or
            (set(aa_matrix.columns) != set(amino_acid_list))):
            sys.exit("".join(["Custom AA matrix must be a 20-by-20 Pandas ",
                        "Dataframe object with AAs as row and column names."]))
        else: #If all goes well, load custom AA matrix
            aa_distance_matrix = aa_matrix
    
    # Load named AA distance matrix if the name is provided
    if isinstance(aa_matrix, str): #Name of AA matrix provided
        # Check if input AA distance matrix name exists, if it is provided
        if os.path.isfile("".join(['data/AA_matrices/',aa_matrix,'.csv']))==False:
            sys.exit("".join(['AA matrix ', aa_matrix, ' does not exist. ',
                              'Check spelling and use all upper cases. ',
                       'You can also define your custom matrix as a 20-by-20 ',
                        'pandas DataFrame with AAs as row and column names.']))
        else: #load stored AA matrix
            aa_distance_matrix = pd.read_csv("".join(['data/AA_matrices/',
                                                  aa_matrix,
                                                  '.csv']),index_col=0);    
    
    
    # save row and column AA orders for row to column AA substitutions
    from_AA = np.array(aa_distance_matrix.index).astype(str)
    to_AA = np.array(aa_distance_matrix.columns).astype(str)
    
    # Convert to np matrix for easy indexing
    aa_distance_matrix = aa_distance_matrix.to_numpy()
    
    #infer peptide length
    if isinstance(index_peptide, str): #One index peptide provided
        peptide_length = len(index_peptide)
    else: #List of index peptides provided
        peptide_length = len(index_peptide[0]) 
    
    # To locate mutation positions together in all mutant sequences, join them all
    if isinstance(index_peptide, str): #One index peptide provided
        index_peptide_repeated = np.array(list("".join(list(np.repeat(index_peptide,
                                            len(mutant_peptide_list))))))
    else: #List of index peptide provided
        index_peptide_repeated = np.array(list("".join(index_peptide)))
        
    mutant_peptides_joined = np.array(list("".join(mutant_peptide_list)))
    
    # Compare mutant seqs to index peptide seq to find mutation locations
    is_mutation_location = np.compare_chararrays(list(index_peptide_repeated),
                            list(mutant_peptides_joined),
                            "!=",'True')
    
    # Locations of WT AAs in from_AA array
    from_AA_index = np.nonzero(index_peptide_repeated[is_mutation_location,None] ==
                               from_AA)[1]
    # Locations of mutated AAs in to_AA array
    to_AA_index = np.nonzero(mutant_peptides_joined[is_mutation_location,None] ==
                               to_AA)[1]
    
    # Collect distance matrix elements corresponding to mismatches
    aa_distance = np.zeros(len(index_peptide_repeated)) #initialize
    aa_distance[is_mutation_location] = aa_distance_matrix[from_AA_index,
                                                           to_AA_index]
    
    # Reshape AA distance array to dim #mutants-by-peptide_length
    aa_distance = np.reshape(aa_distance, 
                             (len(mutant_peptide_list),peptide_length))
    
    
    return aa_distance