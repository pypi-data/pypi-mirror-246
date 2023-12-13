'''
Function that outputs sampled positional weights and AA matrix after pooled
inference with peptide features and TCR activation categories
'''


def pooled_inference(TCR_index, # TCR index for each peptide
                                  peptide_feature, # features for each peptide
                                  peptide_activation_category,#activation category
                                  aa_change_index,#indexing which AA to which
                                  mode, # symmetric (default) or full
                                  seed, steps): #Random seed and #steps for sampler
    import arviz as az
    import pymc as pm
    import numpy as np

    # Infer number of TCRs, peptide length, and number of TCR activation levels
    n_tcr = len(np.unique(TCR_index))
    peptide_length = np.shape(peptide_feature)[1]
    n_level = 1 + max(peptide_activation_category)
    
    # Renumber AA change index matrix with unique AA change indices
    unique_indices,_, aa_change_index_unique = np.unique(aa_change_index, 
                                   return_index=True,
                                   return_inverse=True);
    aa_change_index_unique = aa_change_index_unique.reshape(
                                                     np.shape(peptide_feature))
    
    
    # Build Bayesian classifier
    with pm.Model() as peptide_classifier_model: 
        
        # TCR-indepedent common amino acid distance matrix multiplier flattened        
        aa_distance_multiplier = pm.math.concatenate([[0],
                                          pm.Normal("aa_distance_multiplier",
                                mu=pm.Normal("mu", mu=0, sigma=0.5),
                                sigma=pm.Exponential("sigma",lam=1),
                                shape=len(unique_indices)-1)], 
                                          axis=0)
        #0 at beginning put for No AA substituion
        
        # TCR-specific parameters
        
        # positional weights, pooled over TCRs and positions
        weights = pm.Beta("weights",
                          alpha = pm.Gamma("alpha_w", mu=1.0, sigma=0.5),
                          beta = pm.Gamma("beta_w", mu=5.0, sigma=1.0),
                          shape=(n_tcr,peptide_length))        
        
        # Hyperprior parameters for TCR-specific intercept        
        mu_bar = pm.Normal("mu_bar", mu=0, sigma=2)
        sigma_bar = pm.HalfNormal("sigma_bar", sigma=2)
        normal = pm.Normal("normal", mu=0, sigma=1, shape=n_tcr) 
        
        intercepts=pm.Deterministic("intercepts",mu_bar+sigma_bar*normal)  
             
        
        # Full Predictor
        eta = intercepts[TCR_index] - pm.math.sum(
            weights[TCR_index,:]*peptide_feature*
            (1 + aa_distance_multiplier[aa_change_index_unique]),
            axis=1) #positional weight * D *(1+multiplier) summed over positions
                    
        
        # Binomial Regression
        # Generate cutpoints
        cutpoints=pm.Normal("cutpoints", 
                            mu=0.0, sigma=2.0, shape=[n_level-1],
         transform=pm.distributions.transforms.univariate_ordered,
         initval=np.linspace(0.1,0.5,n_level-1))
        
        peptide_activation_category_obs = pm.OrderedLogistic(
                                        "peptide_activation_category_obs",
                                        eta=eta,cutpoints=cutpoints,
                                        observed=peptide_activation_category,
                                        compute_p=False)
        
    # Sampling with approximate posterior
    with peptide_classifier_model:
         posterior_draws=pm.fit(n=steps,method="advi",
                                random_seed=seed,progressbar=True)
         inferred_params = az.summary(posterior_draws.sample(50000))     
         
    # Extract position-dependent weights of TCRs         
    inferred_weights=np.reshape(inferred_params.iloc[
        (n_tcr+len(unique_indices)+4):
        (n_tcr+len(unique_indices)+4+n_tcr*peptide_length),0].to_numpy(),
        newshape=(n_tcr,peptide_length),order='C') #TCR-by-position
        
    # Extract inferred AA distance matrix multipliers 
    aa_multiplier = inferred_params.iloc[1:len(unique_indices),0].to_numpy()
    aa_multiplier = np.insert(aa_multiplier,0,0)
    #Insert 0 for no substitution
    
    # Reconstruct full AA factor matrix (to be multiplied with regularizer)
    # Initialize with inferred mean of the pooling distribution for AA multiplier
    inferred_aa_matrix = np.zeros((20,20))+(1+inferred_params.iloc[0,0])
    
    if mode=='symm': #Construct symmetric AA matrix multiplier
        for aa1 in np.arange(0,19,1):
            for aa2 in np.arange(0,19,1):
               if 20*min(aa1,aa2)+max(aa1,aa2) in unique_indices:
                   inferred_aa_matrix[aa1,aa2] = 1+aa_multiplier[
                       np.where(unique_indices==20*min(aa1,aa2)+max(aa1,aa2))[0][0]]                   
                   # Takes care of AA reindexing done at the beginning
      
    if mode=='full': #Construct full AA matrix multiplier
        for aa1 in np.arange(0,19,1):
            for aa2 in np.arange(0,19,1):
               if 20*aa1+aa2 in unique_indices:
                   inferred_aa_matrix[aa1,aa2] = 1+aa_multiplier[
                       np.where(unique_indices==20*aa1+aa2)[0][0]]                   
                   # Takes care of AA reindexing done at the beginning
 
    return inferred_weights,inferred_aa_matrix
