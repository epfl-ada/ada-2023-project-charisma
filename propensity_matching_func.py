# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import networkx as nx
import statsmodels.formula.api as smf
import numpy as np
import pandas as pd

def get_similarity(propensity_score1, propensity_score2):
    '''Calculate similarity for instances with given propensity scores'''
    return 1-np.abs(propensity_score1-propensity_score2)

def propensity_matching(paired_matching_original,MAIN_DATA_PATH,treatment,MATCH=False):
    
    print("----------------------\n"+treatment+" pair matching : \n-----------------------")
    
    paired_matching=paired_matching_original.copy().reset_index()
    paired_matching["Movie_Runtime"]=(paired_matching["Movie_Runtime"]-paired_matching["Movie_Runtime"].mean())/paired_matching["Movie_Runtime"].std()
    paired_matching["Movie_Release_Year"]=(paired_matching["Movie_Release_Year"]-paired_matching["Movie_Release_Year"].mean)/paired_matching["Movie_Release_Year"].std())
    paired_matching["num_movies_languages"]=(paired_matching["num_movies_languages"]-paired_matching["num_movies_languages"].mean())/paired_matching["num_movies_languages"].std()
    paired_matching["num_movies_countries"]=(paired_matching["num_movies_countries"]-paired_matching["num_movies_countries"].mean())/paired_matching["num_movies_countries"].std()
    
    
    # compute propensity score for matching
    formula = treatment + " ~  Movie_Runtime + num_movies_languages + num_movies_countries+ Movie_Release_Year"
    
    mod = smf.logit(formula=formula, data=paired_matching)
    
    res = mod.fit()
    
    paired_matching["propensity_score"] = res.predict(paired_matching)
    
    
    
    if res.converged==False:
        print("No converging regression")
        return 0,0,False 
    
    print(res.summary())
    
    if MATCH:
    
        # try matching with requirement on similarity
        treatment_df = paired_matching[paired_matching[treatment] == 1]
        control_df = paired_matching[paired_matching[treatment] == 0]
    
        # Create an empty undirected graph
        G = nx.Graph()
    
        # Loop through all the pairs of instances
        for control_id, control_row in control_df.iterrows():
            for treatment_id, treatment_row in treatment_df.iterrows():
    
                # Calculate the similarity
                similarity = get_similarity(control_row["propensity_score"], treatment_row["propensity_score"])
    
                if (similarity > 0.95):
                    # Add an edge between the two instances weighted by the similarity between them
                    G.add_weighted_edges_from([(control_id, treatment_id, similarity)])
    
        # Generate and return the maximum weight matching on the generated graph
        matching = nx.max_weight_matching(G)
    
    # collect matched instances
    if MATCH:
        matched = [i[0] for i in list(matching)] + [i[1] for i in list(matching)]
        
    path=MATCHED_TREATMENT_PATH=MAIN_DATA_PATH+"\\balanced_"+treatment+".csv"
    # save the balanced dataset to csv to avoid running the matching again
    if MATCH:
        
        # create the balanced dataset
        balanced_df = paired_matching_original.iloc[matched].copy()
        balanced_df.to_csv(path, index=False)
    
    # restoring state from last matching
    if not MATCH:
        balanced_df = pd.read_csv(path)
        
    
    # divide the dataset into treated and control
    treated_df = balanced_df.loc[balanced_df[treatment] == 1]
    control_df = balanced_df.loc[balanced_df[treatment] == 0]
    
    
    return treated_df, control_df, True