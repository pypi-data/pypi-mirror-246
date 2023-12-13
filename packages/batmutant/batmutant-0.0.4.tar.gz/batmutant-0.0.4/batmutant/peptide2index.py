'''
Function to generate peptide to index distance by multiplying positional weight
profile with features of a list of mutant peptides, created using their
position-dependent distances from the index peptide,
based on a given AA distance matrix.

Index peptide can be a string (common for all mutants) or a list (potentially
different for all mutants) with length equal to that of mutant list. All input 
sequences must have equal length.

AA matrix can be the name of a stored matrix (e.g., "BLOSUM100"), or be custom 
defined. Custom AA matrix must be a 20-by-20 Pandas Dataframe object 
with AAs as row and column names.

Weight profile should be array of size peptide_length-by-1 (common for all) or 
peptide_length-by-#mutants (different weights for different mutants)

'''
def peptide2index(index_peptide, # Single index peptide or list 
                 mutant_peptide_list, #List of mutant peptide sequences
                 aa_matrix, #Named or user-defined AA matrix
                 weight_profile): #array of weights
    
    import numpy as np
    import sys
    from generate_mutant_features import generate_mutant_features
    
    # Create mutant features
    mutant_features = generate_mutant_features(index_peptide, 
                                               mutant_peptide_list, 
                                               aa_matrix)
    
    # Check if weight profile is an array with desired size
    peptide_length = len(mutant_peptide_list[0])    
    if ((weight_profile.dtype not in ('int','float')) or
        (np.shape(weight_profile) not in ((1,peptide_length),
                                (len(mutant_peptide_list),peptide_length)))):
        sys.exit("".join(["Weight profile must be a numerical array of shape ",
                  "(1,peptide length) or (number of mutants,peptide length)"]))
    
    # Calculate peptide-to-index distances by multiplication
    if (np.shape(weight_profile)==(1,peptide_length)):
        distance = mutant_features.dot(weight_profile.transpose())[:,0]
    else:
        distance = np.multiply(mutant_features,weight_profile).sum(axis=1)
    
    return distance
