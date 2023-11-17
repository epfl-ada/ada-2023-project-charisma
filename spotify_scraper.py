#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 11 17:46:48 2023

@author: anandchoudhary
"""

import numpy as np
import pandas as pd
import random
import datetime
import re
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from config import SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET


def movie_music_data_spotify_scraper(movie_wikipedia_id_net, movie_name_net, movie_release_date_net):
    
    """
    Function that scrapes music data from Spotify corresponding to the movies data in the movies_metadata dataset from the CMU Movie Summary Corpus
    
    Arguments:
        movie_wikipedia_id_net: List of Wikipedia IDs of the movies in the movies_metadata dataset (To be used when merging the Spotify dataset with the movies_metadata dataset)
        movie_name_net: List of names of movies in the movies_metadata dataset (For retrieving corresponding album data from Spotify)
        movie_release_date_net: List of release dates of movies in the movies_metadata dataset (For selecting the correct album while retrieving album data from Spotify)
        
    Returns: 
        movie_music_df: Dataframe containing the Album and corresponding Track Related Data of the Music (in the Movies) from Spotify
        error_wikipedia_movie_IDs: List containing the Wikipedia movie IDs of movies for which scraping data from Spotify resulted in some errors (typically, due to Rate Limits Errors, HTTP Connection Errors) so that we can scrape data for these movies later on
    """ 
    
    #Instantiate the Spotify Client
    spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(SPOTIPY_CLIENT_ID,SPOTIPY_CLIENT_SECRET))

    movie_music_data = []
    
    #Column Labels in the finally generated movie_music_df
    #Description of Album Features is available at https://developer.spotify.com/documentation/web-api/reference/get-an-album
    #Description of Track Audio Features is available at https://developer.spotify.com/documentation/web-api/reference/get-audio-features
    
    music_dict_keys = ['Wikipedia_Movie_ID',
    'Movie_Name',
    'Album_Name',
    'Album_Release_Date',
    'Album_Genres',
    'Album_Popularity',
    'Album_Total_Tracks',
    'Track_Name',
    'Track_Duration',
    'Track_Acousticness',
    'Track_Danceability',
    'Track_Energy',
    'Track_Instrumentalness',
    'Track_Key',
    'Track_Liveness',
    'Track_Loudness',
    'Track_Mode',
    'Track_Speechiness',
    'Track_Tempo',
    'Track_Time_Signature',
    'Track_Valence']
    

    #Release Date Cutoff (so that we don't scrape albums beyond these movie release date)
    #Set to 2015 to allow for delay in album release on Spotify (after performing some scraping)
    release_date_cutoff = datetime.datetime.strptime('2015','%Y')
    
    error_wikipedia_movie_IDs = []
    
    #Loop over the movies
    for ctr, (movie_name, movie_release_date) in enumerate(zip(movie_name_net, movie_release_date_net)):
        
        #Lowercase the movie name
        movie_name_lowercased = movie_name.lower()

        #Initialization
        movie_album_URI = np.nan
        flag = 0

        if movie_release_date == movie_release_date: #testing for non-NaNs
            #Convert the release date only to the release year for comparison since a lot of albums on Spotify only have the release year mentioned
            movie_release_date = datetime.datetime.strptime(movie_release_date[:4],'%Y')
        else:
            movie_release_date = np.nan #Convert any pandas NaTs to numpy NaNs
            
        #In this 1st stage, we search for official movie albums on Spotify by itertaively checking for movie albums using keywords (movie name and suffix)
        #After checking various official movie albums on Spotify, we ensure this by checking for the name of the movie in the album together with a movie name suffix commonly used for original movie albums on Spotify
        #These suffixes are: (Original Motion Picture Soundtrack), (Music from the Motion Picture) and (Original Motion Picture Score)
        #Finally, if we don't retrieve the album even after trying all of these suffixes, we check for the presence of the words 'Original', 'Motion Picture', 'Soundtrack' and 'Score' in the name of the movie album 
        #This is because some movie album names have other suffixes containing one/more of the aforemntioned words (like Original Soundtrack Recording, etc.)
        #If we don't retrieve any movie album info even after performing all these checks, we conclude that the required official movie album doesn't exist on Spotify or that the movie didn't have any music in the first place
        
        
        #Check for movie album with the 1st suffix
        movie_name_suffix = '(Original Motion Picture Soundtrack)'
        movie_album_results = spotify.search(q='album:' + movie_name + movie_name_suffix, type='album')['albums']['items']
        
        #If we find any movie albums, only then do we try to find the URI for the correct movie album
        if len(movie_album_results) != 0:
            
            #Only 1 movie album is found: Simple Case
            if len(movie_album_results) == 1:
                movie_album_name = movie_album_results[0]['name'].lower()
                #Ensure that the movie name is in the album name (case insensitive)
                if re.search(rf'{movie_name_lowercased}',rf'{movie_album_name}',flags = re.I):
                    movie_album_release_date = datetime.datetime.strptime(movie_album_results[0]['release_date'][:4],'%Y')
                    #Ensure that the movie album's release date is less than the release date cutoff
                    if movie_album_release_date <= release_date_cutoff:
                        flag = 1
                        #Store the URI of the movie's album
                        movie_album_URI = movie_album_results[0]['uri']
                        
            #More than 1 movie album is found: Complex Case
            else:
                
                movie_album_name_net = [movie_album['name'] for movie_album in movie_album_results]
                movie_album_release_date_net = []
                movie_album_URI_net = []
                
                #First, select only the movie albums which satisfy the required criteria of name and release date cutoff
                for movie_album in movie_album_results:
                    movie_album_name = movie_album['name'].lower()
                    #Ensure that the movie name is in the album name (case insensitive)
                    if re.search(rf'{movie_name_lowercased}',rf'{movie_album_name}',flags = re.I):
                        movie_album_release_date = datetime.datetime.strptime(movie_album['release_date'][:4],'%Y')
                        #Ensure that the movie album's release date is less than the release date cutoff
                        if movie_album_release_date <= release_date_cutoff:
                            #Store the URIs of the albums and their corresponding release dates
                            movie_album_release_date_net.append(movie_album_release_date)
                            movie_album_URI_net.append(movie_album['uri'])
                
                #Check if we have movie albums to select from
                if len(movie_album_release_date_net) != 0:
                    
                    flag = 1
                    
                    #Selecting the correct album via comparison with the movie's release date is only possible if the movie does have a release date in the first place.
                    #Check for this first
                    if movie_release_date == movie_release_date:
                        #Compute the difference in the release dates of the movie and the movie albums retrieved from Spotify (after having performed an initial selection)
                        movie_music_release_date_diff_net = np.array([abs(movie_release_date - movie_album_release_date) for movie_album_release_date in movie_album_release_date_net])
                        #Identify the album(s) having the release date closest to the release date of the movie.
                        best_movie_album_match_idx_net = np.where(movie_music_release_date_diff_net == min(movie_music_release_date_diff_net))[0]
                        #Only 1 Album with Minimum Release Date Difference ==> Proceed with storing its Index
                        if len(best_movie_album_match_idx_net) > 1:
                            best_movie_album_match_idx = random.choice(best_movie_album_match_idx_net)
                        #More than 1 Album with Minimum Release Date Difference ==> Proceed with storing the Index of any movie album (randomly selected) from best_movie_album_match_idx_net
                        else:
                            best_movie_album_match_idx = best_movie_album_match_idx_net[0]
                        movie_album_URI = movie_album_URI_net[best_movie_album_match_idx]
                        
                    else:
                        #If we don't have the movie's release date, we can't make comparisons with the album release dates and hence, we select an album at random
                        movie_album_URI_net = [movie_album['uri'] for movie_album in movie_album_results]
                        movie_album_URI = random.choice(movie_album_URI_net)
        
        #Check for movie album with the 2nd suffix only if no album was retrieved using the 1st suffix           
        if not flag:
            
            #Check for movie album with the 2nd suffix
            movie_name_suffix = '(Music from the Motion Picture)'
            movie_album_results = spotify.search(q='album:' + movie_name + movie_name_suffix, type='album')['albums']['items']
            
            #Subsequent code structure follows from the corresponding code for the 1st suffix
            if len(movie_album_results) != 0:
                
                
                if len(movie_album_results) == 1:
                    
                    movie_album_name = movie_album_results[0]['name'].lower()
                    if re.search(rf'{movie_name_lowercased}',rf'{movie_album_name}',flags = re.I):
                        movie_album_release_date = datetime.datetime.strptime(movie_album_results[0]['release_date'][:4],'%Y')
                        if movie_album_release_date <= release_date_cutoff:
                            flag = 1
                            movie_album_URI = movie_album_results[0]['uri']
                
                else:
                    
                    movie_album_name_net = [movie_album['name'] for movie_album in movie_album_results]
                    movie_album_release_date_net = []
                    movie_album_URI_net = []
                    
                    for movie_album in movie_album_results:
                        movie_album_name = movie_album['name'].lower()
                        if re.search(rf'{movie_name_lowercased}',rf'{movie_album_name}',flags = re.I):
                            movie_album_release_date = datetime.datetime.strptime(movie_album['release_date'][:4],'%Y')
                            if movie_album_release_date <= release_date_cutoff:
                                movie_album_release_date_net.append(movie_album_release_date)
                                movie_album_URI_net.append(movie_album['uri'])
                            
                    if len(movie_album_release_date_net) != 0:
                        
                        flag = 1
                    
                        if movie_release_date == movie_release_date:
                            movie_music_release_date_diff_net = np.array([abs(movie_release_date - movie_album_release_date) for movie_album_release_date in movie_album_release_date_net])
                            best_movie_album_match_idx_net = np.where(movie_music_release_date_diff_net == min(movie_music_release_date_diff_net))[0]
                            if len(best_movie_album_match_idx_net) > 1:
                                best_movie_album_match_idx = random.choice(best_movie_album_match_idx_net)
                            else:
                                best_movie_album_match_idx = best_movie_album_match_idx_net[0]
                            movie_album_URI = movie_album_URI_net[best_movie_album_match_idx]
                            
                        else:
                            movie_album_URI_net = [movie_album['uri'] for movie_album in movie_album_results]
                            movie_album_URI = random.choice(movie_album_URI_net)
                    
            #Check for movie album with the 3rd suffix only if no album was retrieved using the 2nd suffix              
            if not flag:
                
                #Check for movie album with the 3rd suffix
                movie_name_suffix = '(Original Motion Picture Score)'
                movie_album_results = spotify.search(q='album:' + movie_name + movie_name_suffix, type='album')['albums']['items']
                
                #Subsequent code structure follows from the corresponding code for the 1st suffix
                if len(movie_album_results) != 0:
                    
                    
                    if len(movie_album_results) == 1:
                        movie_album_name = movie_album_results[0]['name'].lower()
                        if re.search(rf'{movie_name_lowercased}',rf'{movie_album_name}',flags = re.I):
                            movie_album_release_date = datetime.datetime.strptime(movie_album_results[0]['release_date'][:4],'%Y')
                            if movie_album_release_date <= release_date_cutoff:
                                flag = 1
                                movie_album_URI = movie_album_results[0]['uri']
                    
                    else:
                        
                        movie_album_name_net = [movie_album['name'] for movie_album in movie_album_results]
                        movie_album_release_date_net = []
                        movie_album_URI_net = []
                        
                        for movie_album in movie_album_results:
                            movie_album_name = movie_album['name'].lower()
                            if re.search(rf'{movie_name_lowercased}',rf'{movie_album_name}',flags = re.I):
                                movie_album_release_date = datetime.datetime.strptime(movie_album['release_date'][:4],'%Y')
                                if movie_album_release_date <= release_date_cutoff:
                                    movie_album_release_date_net.append(movie_album_release_date)
                                    movie_album_URI_net.append(movie_album['uri'])
                                
                        if len(movie_album_release_date_net) != 0:
                            
                            flag = 1
                        
                            if movie_release_date == movie_release_date:
                                movie_music_release_date_diff_net = np.array([abs(movie_release_date - movie_album_release_date) for movie_album_release_date in movie_album_release_date_net])
                                best_movie_album_match_idx_net = np.where(movie_music_release_date_diff_net == min(movie_music_release_date_diff_net))[0]
                                if len(best_movie_album_match_idx_net) > 1:
                                    best_movie_album_match_idx = random.choice(best_movie_album_match_idx_net)
                                else:
                                    best_movie_album_match_idx = best_movie_album_match_idx_net[0]
                                movie_album_URI = movie_album_URI_net[best_movie_album_match_idx]
                                
                            else:
                                movie_album_URI_net = [movie_album['uri'] for movie_album in movie_album_results]
                                movie_album_URI = random.choice(movie_album_URI_net)
                        
                #Check for movie album with the set of keywords (mentioned earlier) if no album was retrieved using the 3rd suffix                          
                if not flag:
                    
                    movie_album_results = spotify.search(q='album:' + movie_name, type='album')['albums']['items']
                    
                    #Subsequent code structure mostly follows from the corresponding code for the 1st suffix (Comments have added for major differences)
                    if len(movie_album_results) != 0:
                        
                        movie_name_lowercased = movie_name.lower()
                        
                        if len(movie_album_results) == 1:
                            
                            movie_album_name = movie_album_results[0]['name'].lower()
                            if re.search(rf'{movie_name_lowercased}',rf'{movie_album_name}',flags = re.I):
                                #Remove movie name from the album name to avoid any overlap in words in the movie name and the keyword set used for extracting the albums
                                movie_album_name = re.sub(rf'{movie_name_lowercased}','',movie_album_name)
                                #Check whether any of the keywords are present in the album name
                                if re.search('Original|Motion\sPicture|Soundtrack|Score',rf'{movie_album_name}',flags = re.I):
                                    movie_album_release_date = datetime.datetime.strptime(movie_album_results[0]['release_date'][:4],'%Y')
                                    if movie_album_release_date <= release_date_cutoff:
                                        flag = 1
                                        movie_album_URI = movie_album_results[0]['uri']
                        
                        else:
                            movie_album_name_net = [movie_album['name'] for movie_album in movie_album_results]
                            movie_album_release_date_net = [movie_album['release_date'] for movie_album in movie_album_results]
                            selected_movie_album_name_idx_net = []
                            
                            for i, movie_album_name in enumerate(movie_album_name_net):
                                
                                movie_album_name = movie_album_name.lower()
                                if re.search(rf'{movie_name_lowercased}',rf'{movie_album_name}',flags = re.I):
                                    #Remove movie name from the album name to avoid any overlap in words in the movie name and the keyword set used for extracting the albums
                                    movie_album_name = re.sub(rf'{movie_name_lowercased}','',movie_album_name)
                                    #Check whether any of the keywords are present in the album name
                                    if re.search('Original|Motion\sPicture|Soundtrack|Score',rf'{movie_album_name}',flags = re.I):
                                        movie_album_release_date = datetime.datetime.strptime(movie_album_release_date_net[i][:4],'%Y')
                                        if movie_album_release_date <= release_date_cutoff:
                                            selected_movie_album_name_idx_net.append(i)
                                        
                            movie_album_release_date_net = []
                            movie_album_URI_net = []
                            
                            if len(selected_movie_album_name_idx_net) != 0:
                                
                                if movie_release_date == movie_release_date:
                                    for i, movie_album in enumerate(movie_album_results):
                                        if i in selected_movie_album_name_idx_net:
                                            movie_album_release_date_net.append(datetime.datetime.strptime(movie_album['release_date'][:4],'%Y'))
                                            movie_album_URI_net.append(movie_album['uri'])
                                    
                                    movie_music_release_date_diff_net = np.array([abs(movie_release_date - movie_album_release_date) for movie_album_release_date in movie_album_release_date_net])
                                    best_movie_album_match_idx_net = np.where(movie_music_release_date_diff_net == min(movie_music_release_date_diff_net))[0]
                                    if len(best_movie_album_match_idx_net) > 1:
                                        best_movie_album_match_idx = random.choice(best_movie_album_match_idx_net)
                                    else:
                                        best_movie_album_match_idx = best_movie_album_match_idx_net[0]
                                    movie_album_URI = movie_album_URI_net[best_movie_album_match_idx]
                                    
                                else:
                                    movie_album_URI_net = [movie_album['uri'] for movie_album in movie_album_results]
                                    movie_album_URI = random.choice(movie_album_URI_net)
                            
        #Check whether we've got a non-NaN movie album URI                    
        if movie_album_URI == movie_album_URI:
            
            try:
                #Extract all album data from Spotify using the movie album URI          
                movie_album = spotify.album(movie_album_URI)
                album_name = movie_album['name']
                album_release_date = movie_album['release_date']
                album_genres = movie_album['genres']
                album_popularity = movie_album['popularity']
                album_total_tracks = movie_album['total_tracks']
                album_track_net = movie_album['tracks']['items']
                #Loop over the tracks in the album
                for album_track in album_track_net:
                    
                    music_dict_values = []
                    music_dict_values.extend((movie_wikipedia_id_net[ctr],movie_name,album_name,album_release_date,album_genres,album_popularity,album_total_tracks))
                    
                    music_dict_values.extend((album_track['name'],album_track['duration_ms']))
                    
                    #Extract all track data (audio features) from Spotify using the track's URI 
                    track_uri = album_track['uri']
                    track_audio_features = spotify.audio_features([track_uri])[0]
                    
                    #Save the audio features corresponding to the track only if we successfully retrieved them or only if they exist
                    if track_audio_features:
                        
                        music_dict_values.extend((track_audio_features['acousticness'],track_audio_features['danceability'],track_audio_features['energy'],track_audio_features['instrumentalness'],track_audio_features['key'],track_audio_features['liveness'],track_audio_features['loudness'],track_audio_features['mode'],track_audio_features['speechiness'],track_audio_features['tempo'],track_audio_features['time_signature'],track_audio_features['valence']))
                        
                        music_dict = dict(zip(music_dict_keys,music_dict_values))
                        
                        movie_music_data.append(music_dict)
                        
                    
                    
                    
                    i += 1
                    
            #Capture all the wikipedia IDs of movies for which scraping resulted in an error (e.g., Rate Limit Errors, HTTP Connection Errors, etc.)
            #This is done so that we can retrieve data for them in the subsequent round(s) of scraping after the rate limit is reset and/or the HTTP Connection issue with the API gets resolved
            except Exception:
                error_wikipedia_movie_IDs.append(movie_wikipedia_id_net[ctr])
                
            
            

    #Save all the music data and create a dataframe
    movie_music_df = pd.DataFrame(movie_music_data)
                          
    return movie_music_df, error_wikipedia_movie_IDs         
                        


