'''
Function to train BATMAN, using TCR activation data provided in a csv file.
Refer to the example file to see format of the input TCR activation datafile.

TCR activation levels must start from 0 (weakest) and are integers 
(no missing level allowed)

AA matrix can be the name of a stored matrix (e.g., "BLOSUM100"), or be custom 
defined. Custom AA matrix must be a 20-by-20 Pandas Dataframe object 
with AAs as row and column names.

Runs in one of 3 modes: weights_only, full, or symm, based on if only weights
are inferred (AA matrix being the one specified) or if both weights and AA matrices
are inferred (symmetric or full AA matrix)

Also takes #steps for sampling and a seed argument for reproduction 

'''

def train(filename,#Path to file containing TCR data (see example for format)
          mode,# weights_only, symm, or full
          # Default values of optional parameters
          aa_matrix='BLOSUM100',#Named or user-defined AA matrix used for regularization
          seed=100,#seed for sampling
          steps=20000):# number of steps for sampling


    import pandas as pd
    import numpy as np
    import os.path, sys
    from generate_mutant_features import generate_mutant_features
    from pooled_inference_weights_only import pooled_inference_weights_only
    from pooled_inference import pooled_inference
    
    # Mode must be specified as one of 3 options
    if mode not in ('weights_only','symm','full'):
        sys.exit("Mode must be one of: 'weights_only', 'symm', 'full'")
    
    # Check if file exists and is csv
    if os.path.isfile(filename)==False:
        sys.exit("File does not exist. Check filename and/or directory again.")
    
    if filename.endswith('.csv')==False:
        sys.exit("File must be of csv format. See example input for details.")
    
    # Check that file has correct headers for relevant columns
    if {'activation', 'index', 'peptide', 'tcr'}.issubset(
            set(pd.read_csv(filename).columns))==False:
        sys.exit(''.join(["Input file must have these 4 headers:", 
                 "'activation', 'index', 'peptide', 'tcr'.",
                 "Check spelling and have all headers in lower case."]))

    # Check that 'activation' column has 0 and integer data
    if ((pd.read_csv(filename)['activation'].to_numpy().dtype.kind not in ('i','u'))
    or (min(pd.read_csv(filename)['activation'].to_numpy()))!=0):
        sys.exit("activation levels must be 0 and positive integer(s) (smaller=weaker)")
    
    # Check that all activation levels between 0 to K (max) are present in data
    if sum(np.unique(pd.read_csv(filename)['activation'])!=
           np.arange(0,1+max((pd.read_csv(filename)['activation'].to_numpy())),1))!=0:
        sys.exit("One or more missing activation levels in data")
    
    
    # Read and featurize peptide data
    peptide_data = pd.read_csv(filename)
    
    # Assign indices to unique TCRs in data
    TCR_names, TCR_index = np.unique(peptide_data['tcr'], return_inverse=True)
    
    # Make list of index peptide
    index_list = peptide_data['index'].tolist()
    # Make list of mutant peptide
    peptide_list = peptide_data['peptide'].tolist()
    
    # Make peptide features
    peptide_feature = generate_mutant_features(index_list,
                                               peptide_list,
                                               aa_matrix)
    
    # Peptide activation categories
    peptide_activation_category = peptide_data['activation'].to_numpy()
    
    if mode=='weights_only':
        # Run sampling for Inference of only weights
        inferred_weights = pooled_inference_weights_only(TCR_index, 
                                                         peptide_feature, 
                                                         peptide_activation_category, 
                                                         seed=seed, steps=steps)
        # Add TCR names
        inferred_weights = pd.DataFrame(inferred_weights,index=TCR_names)
        return inferred_weights
    
    else: 
        
        #AA name list
        aa_list=np.array(['A','C','D','E','F','G','H','I','K','L','M','N','P','Q','R',
                         'S','T','V','W','Y'])
        # List which AA substitutions are in data (based on full or symm AA matrix)
        # Indices of index and mutant AAs in AA list (flattened)
        index_aa = np.where(np.array(list(''.join(index_list)))[:, None] == 
                            aa_list[None, :])[1]
        peptide_aa = np.where(np.array(list(''.join(peptide_list)))[:, None] == 
                              aa_list[None, :])[1]
        
        if mode=='symm':
            #Symmetric case, indicate a single number to index AA substitution, 
            #and reshape flattened array
            aa_subs = (20*np.minimum(index_aa,peptide_aa)+ np.maximum(index_aa,peptide_aa))
            aa_subs[index_aa==peptide_aa]=0 #assign 0 to positions with unchanged AA 
            aa_change_index = aa_subs.reshape(np.shape(peptide_feature))
            
        if mode=='full':
            #full AA matrix, indicate a single number to index AA substitution, 
            #and reshape flattened array
            aa_subs = (20*index_aa + peptide_aa)
            aa_subs[index_aa==peptide_aa]=0 #assign 0 to positions with unchanged AA 
            aa_change_index = aa_subs.reshape(np.shape(peptide_feature))   
        
        # Run Inference
        inferred_weights,inferred_aa_matrix = pooled_inference(TCR_index,
                                                               peptide_feature, 
                                                               peptide_activation_category, 
                                                               aa_change_index, 
                                                               mode=mode, 
                                                               seed=seed, steps=steps)
        # Add TCR names
        inferred_weights = pd.DataFrame(inferred_weights,index=TCR_names)
        
        # multiply to regularizer AA matrices
        # Load named AA distance matrix data if the name is provided
        if isinstance(aa_matrix, str): #Name of AA matrix provided
            aa_matrix_prior = pd.read_csv("".join(['data/AA_matrices/',
                                                  aa_matrix,
                                                  '.csv']),index_col=0);
          
        inferred_aa_matrix = aa_matrix_prior*inferred_aa_matrix 
        
    return inferred_weights,inferred_aa_matrix

