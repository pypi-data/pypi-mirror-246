'''
Function that outputs sampled positional weights after pooled inference with peptide
features and TCR activation categories
'''


def pooled_inference_weights_only(TCR_index, # TCR index for each peptide
                                  peptide_feature, # features for each peptide
                                  peptide_activation_category,#activation category
                                  seed, steps): #Random seed and #steps for sampler
    import arviz as az
    import pymc as pm
    import numpy as np
    
    # Infer number of TCRs, peptide length, and number of TCR activation levels
    n_tcr = len(np.unique(TCR_index))
    peptide_length = np.shape(peptide_feature)[1]
    n_level = 1 + max(peptide_activation_category)
    
    # Build Bayesian classifier
    with pm.Model() as peptide_classifier_model:        
        
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
            peptide_feature*weights[TCR_index,:],axis=1)
        
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
        (n_tcr+3):(n_tcr+3+n_tcr*peptide_length),0].to_numpy(),
        newshape=(n_tcr,peptide_length),order='C') #TCR-by-position
    
    return inferred_weights