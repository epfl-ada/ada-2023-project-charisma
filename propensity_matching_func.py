
import networkx as nx
import statsmodels.formula.api as smf
import numpy as np
import pandas as pd

def get_similarity(propensity_score1, propensity_score2):
    '''Calculate similarity for instances with given propensity scores
        (given function from ADA exercices)
    '''
    return 1-np.abs(propensity_score1-propensity_score2)

def propensity_matching(paired_matching_original,MAIN_DATA_PATH,treatment,MATCH=False):
    """
    Apply pair matching if logit regression is converging.
    Return True if the logit regression is converging, otherwise False and treated_df and control_df are null.
    If return True, it return treated_df and control_df, two samples from the orgininal dataframe containing rows with similar propensity scores (>0.95) towards a specific attribute.
    
    
    Parameters:
    - paired_matching_original (DataFrame): The original dataFrame containing the data.
    - MAIN_DATA_PATH (str): The path where to save or read the balanced sample.
    - treatment (str): Column of the dataframe, corresponding to the music feature on which we want the pair matching.
    - MATCH (bool, optional) : False by default, boolean variable that indicates if we want to recalculate the pair matching (it takes time) or if we want to read existing treated and control dataframes. 
    """
    
    
    print("--------------------------------------------\n"+treatment+" pair matching : \n--------------------------------------------")
    
    #standardisation of independant variables before applying logit regression.
    paired_matching=paired_matching_original.copy().reset_index()
    paired_matching["Movie_Runtime"]=(paired_matching["Movie_Runtime"]-paired_matching["Movie_Runtime"].mean())/paired_matching["Movie_Runtime"].std()
    paired_matching["num_movies_languages"]=(paired_matching["num_movies_languages"]-paired_matching["num_movies_languages"].mean())/paired_matching["num_movies_languages"].std()
    paired_matching["num_movies_countries"]=(paired_matching["num_movies_countries"]-paired_matching["num_movies_countries"].mean())/paired_matching["num_movies_countries"].std()
    
    
    # logit regression for the music feature
    formula = treatment + " ~  Movie_Runtime + num_movies_languages + num_movies_countries"
    
    mod = smf.logit(formula=formula, data=paired_matching)
    
    res = mod.fit()
    
    #get propensity score for each row towards the music feature
    paired_matching["propensity_score"] = res.predict(paired_matching)
    
    
    #test if the logit regression is converging before doing pair matching
    if res.converged==False:
        print("No converging regression")
        return 0,0,False 
    
    print(res.summary())
    
    #path to save or read the balanced sample
    path=MATCHED_TREATMENT_PATH=MAIN_DATA_PATH+"\\balanced_"+treatment+".csv"
    
    if MATCH:
    
        # separate control and treatment dataframe using music feature as condition
        treatment_df = paired_matching[paired_matching[treatment] == 1]
        control_df = paired_matching[paired_matching[treatment] == 0]
    
        # Create an empty undirected graph
        G = nx.Graph()
    
        # Loop through all the rows of the two dataframes
        for control_id, control_row in control_df.iterrows():
            for treatment_id, treatment_row in treatment_df.iterrows():
    
                # Calculate the similarity
                similarity = get_similarity(control_row["propensity_score"], treatment_row["propensity_score"])
    
                if (similarity > 0.95):
                    # Add an weighted (by similarity) edge between the two rows
                    G.add_weighted_edges_from([(control_id, treatment_id, similarity)])
    
        #Get the maximum weight matching
        matching = nx.max_weight_matching(G)
    
        # collect matched rows
        matched = [i[0] for i in list(matching)] + [i[1] for i in list(matching)]
    
        # create the balanced dataset and save it 
        balanced_df = paired_matching_original.iloc[matched].copy()
        balanced_df.to_csv(path, index=False)
    
    # read the balanced dataframe already computed to avoid running the matching computation 
    if not MATCH:
        balanced_df = pd.read_csv(path)
        
    
    # split the balanced dataframe into treated and control dataframe
    treated_df = balanced_df.loc[balanced_df[treatment] == 1]
    control_df = balanced_df.loc[balanced_df[treatment] == 0]
    
    
    return treated_df, control_df, True