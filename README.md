# How Music Moves Movies

Link to our Datastory: [https://team-charisma.github.io](https://team-charisma.github.io)

## Abstract:
Hit musical numbers from the blockbuster movies *‘Dilwale Dulhania Le Jayenge’* and *‘Titanic’* continue to occupy a special place in people’s hearts even today. This might make you think: What are the secret ingredients of music that enrapture all of us and how does it add magic to the movies? With this thought in mind, we will use the [CMU Movie Summary Corpus](https://www.cs.cmu.edu/~ark/personas/) and our [Spotify Dataset](https://drive.google.com/file/d/1jQddj3t17Is45Z7sInjA6_KeknGuLgSl/view?usp=share_link) to find out the dominant music attributes (danceability, energy, liveness, etc.) in different countries across the world so as to possibly reveal country-specific music styles for the top 3 countries (in our combined movie and music dataset). Subsequently, we will observe the change in music features and their interplay with the changes in the emotions portrayed by movies in the top 2 countries (in our combined movie, music and emotion dataset) across the years. Finally, we will connect all the dots to reveal how music moves movies towards success.

## Research Questions: 
1. What are the country-specific music styles?
2. How has music (in movies) changed (if so) across the years? What is its interplay (if any) with the change in the emotions portrayed by the movies across the years?
3. Can a certain music style move a movie towards success? If so, how?

## Additional Datasets: 
1. [Spotify Dataset](https://drive.google.com/file/d/1jQddj3t17Is45Z7sInjA6_KeknGuLgSl/view?usp=share_link): We scraped music album data from [Spotify](https://developer.spotify.com/documentation/web-api) using the [Spotipy Python Library](https://spotipy.readthedocs.io/en/2.22.1/) corresponding to the movies in the CMU Movie Summary Corpus. `spotify_scraper.py` details how we scraped the data and obtained all the features in our music dataset.
2. [USD CPI Dataset](https://www.usinflationcalculator.com/inflation/consumer-price-index-and-annual-percent-changes-from-1913-to-2008/): We used this dataset for adjusting movie box office revenues for inflation and hence, removing correlation between box office revenue and release year of the movies.


## Methods:

**PART 1: Deciphering the Links between Music Features and Countries**:
 - **Data Collection, Pre-Processing, Analysis and Visualization**:
    - *Movies Metadata Dataset (from CMU Movie Summary Corpus)*:
       - We eliminated all the duplicates of movie records from the dataset which were identified using all the attributes corresponding to the movies. We were thus able to identify 81734 unique movies in the dataset.
       - We checked for missing values in the dataset and found out that some values of `Movie_Release_Date`, `Movie_Box_Office_Revenue` and `Movie_Runtime` were missing in the dataset. We considered the movie name, runtime and release year (also incorporated in the date) as a unique identifier of a movie and hence, only examine the possibility of dealing with missing values in the `Movie_Box_Office_Revenue` column since that is the only column for which we can deal with the missing values using the values in the other 3 columns. While we saw that about 89.7% of the values in the `Movie_Box_Office_Revenue` column were missing, we figured out that removing these values would still leave us with about 8400 movies in the dataset which is still sufficiently high for our further analysis (PART 3). 
       - We found out a strong correlation between `Movie_Box_Office_Revenue` and `Movie_Release_Year` and adjusted the revenues for inflation using the USD CPI Dataset in order to remove this correlation (Useful for PART 3)
       - We identified the top 10 `Movie_Genres`, `Movie_Countries` and `Movie_Languages` used pie charts for understanding the movie count breakup amongst them and visualized and analysed the `Movie_Box_Office_Revenue` and `Movie_Runtime` across the top 10 (or top 3, in the case of overlapping plots) movies using boxplots and lineplots (w.r.t. `Movie_Release_Year`).
    - *Spotify Dataset*:
       - We averaged and/or kept the first value (in case of the same value for the tracks of a given album) for the relevant audio features of tracks across the movie albums individually so as to obtain a movie-wise music attribute mix.
       - We visualised all the relevant averaged features of music corresponding to movies using a scatterplot matrix. We found out that loudness was strongly correlated with energy while danceability and valence and liveness and valence were also strongly correlated (Strong correlation refers to a correlation coefficient > 0.75 which is also significant: p-value < 0.05). We took these correlations into account for our analysis in PART 3.
    - *The Spotify Dataset + The Movies Metadata Dataset*:
       - Merging the 2 datasets clearly revealed that we had been able to succesfully scrape the music features corresponding to 14055 movies (~ 17.2%) in the movies metadata dataset. This is a sufficiently high number for all our further analyses since all movies don't contain music in the first place.
       - We examined how the movies which contain music are distributed across different languages, countries and genres using pie charts.
       - We then visualized and analysed how the music features differ across the top 10 (and or top 3 in the case of overlapping plots) movies of the various genres, countries and languages.
 - Analysis of Country-Specific Music Features:  We performed t-tests comparing all the music features between movies of a particular country and movies from the rest of the world. We did this for the top 3 countries and as expected this revealed significant differences in music styles highlighting their country specificity.

**PART 2: Connecting Music with Emotions Portrayed by Movies**:

 - *Emotion Classification of the Plot Summaries of Movies*: We used the plot summaries dataset from the CMU Movie Summary Corpus for extracting the plot summaries of the movies. Subsequently, we used the transformer DistilBERT for affecting an emotion classification cum analysis (e.g., amount of love, anger, sadness, etc. in films) of the plot summaries. The dataset of the plot summaries with their corresponding emotions (gennerated by us) can be found at the following link: [Plot_Summaries_with_Emotions.csv](https://drive.google.com/file/d/1Ohbt96e1_HaSBmpjuo35y2XKK0Ycyxqa/view?usp=share_link). It contains movie plot emotions of 42303 movies in (more than 50% of) the movies metadata dataset.
 - *Emotion Correlation Analysis*:
    - We checked for any correlations between the emotions (sadness, anger, fear, joy, love and surprise) portrayed by different movies and found out that none of the emotions were strongly correlated with another one. Accordingly, we decided to go ahead with all the 6 emotions for the analysis in the next step.
 - *Analysis of the Emotions and the Relationships between the Time Series of Emotions and Music*:
    - We zoomed in on the 2 cinematic powerhouses India and the United States of America (USA). Our dataset of movies, music and emotions contained 3381 Indian movies and American movies.
    - We visualized and analyzed the emotions portrayed by movies across the top 5 genres for both the 2 countries using violin plots.
    - We conducted a time series analysis of the music features across the years for movies in the top 5 genres for both the 2 countries.
    - We analyzed the long term relationship (cointegration) between the time series of emotions and music features across the years for the top 5 movie genres for both the 2 countries using the augmented Engle-Granger two-step cointegration test. The null hypothesis is of no cointegration between the 2 time series while the alternative hypothesis is that they are cointegrated, i.e., their linear combination is I(1). We analyzed the interesting findings from these cointegration tests. 

**PART 3: How does Music Drive Movies Towards Success**:
 - *Defining Success*: We considered the box office revenue as the indicator of a film’s success.
 - *Analysis of the Impact of Separate Attributes of Music on Movie Success*:
    - First of all, we compared the box office revenue with different music features to see if there was a correlation between them. This naive analysis allowed us to discern the music features which could act as potential determinants of success.
    - For all these correlated features, we then decided to experiment with a set of thresholds and formed treatment and control groups according to the quantile of the features at the given thresholds. We then chose the threshold with the greatest difference in the Mean Box Office Revenue between the treatment and control groups, whilst checking that the limits of the confidence interval aren’t negative. With this procedure, we narrowed down the list of correlated features.
    - We then conducted paired matching to neutralize the effect of confounders and appropriately identify causal links.
    - We finally formulated general guidelines (our predictions) of how choosing music appropriately can drive a movie towards success.


## Proposed Timeline:
| Deadline | Parts of Research Questions | Data Story |
| ------------- | ------------- | ------------- |
| 17/11/2023  |  Perform Data Collection, Pre-Processing, Analysis and Visualization (Movies Metadata Dataset + Sample of Spotify Dataset) |   |
| 27/11/2023  | Complete Scraping of Spotify Dataset Data Collection, Pre-Processing, Analysis and Visualization (Extension to fully scraped Spotify Dataset) | Develop Initial Framework for Data Story |
| 1/12/2023  | Analyse Country-Specific Music Styles | Develop Initial Rendition of Data Story  |
| 8/12/2023  | Perform Emotion Classification cum Analysis of the Plot Summaries of Movies | Update Data Story  |
|   | Define Success |  |
|   | Analyse the Impact of Separate Attributes of Music on Movie Success |  |
| 15/12/2023 | Perform Time Series Analysis of the Emotions and Music Features across the Years | Update Data Story |
|   | Analysis of Separate Attributes of Music on Movie Success (contd.) |   |
|   | Formulate General Guidelines of How Choosing Music Appropriately can Drive a Movie towards Success | |
| 22/12/2023  | Finalise Everything and Submit | Finalise Data Story and Submit |


## Organization/Contribution within the Team:
| Name | Project Work |
| ------------- | ------------- | 
| Anand Choudhary | Perform Data Collection, Pre-Processing, Analysis and Visualization | 
|  | Develop the Spotify Data Scraper | 
|  | Analyse Country-Specific Music Styles  | 
|  | Perform Emotion Classification cum Analysis of the Plot Summaries of Movies | 
|  | Perform Time Series Analysis of the Emotions and Music Features across the Years | 
|  | Formulate General Guidelines of How Choosing Music Appropriately can Drive a Movie towards Success | 
|  | Create, Update and Finalise Data Story |
| Stefanie Helfenstein | Perform Data Collection, Pre-Processing, Analysis and Visualization | 
|  | Analyse Country-Specific Music Styles  | 
|  | Define Success | 
|  | Analyse the Impact of Separate Attributes of Music on Movie Success | 
|  | Formulate General Guidelines of How Choosing Music Appropriately can Drive a Movie towards Success |  
|  | Create, Update and Finalise Data Story |
| Romain Defferrard | Perform Data Collection, Pre-Processing, Analysis and Visualization | 
|  | Analyse Country-Specific Music Styles  | 
|  | Perform Emotion Classification cum Analysis of the Plot Summaries of Movies | 
|  | Perform Time Series Analysis of the Emotions and Music Features across the Years | 
|  | Create, Update and Finalise Data Story |
| Samuel Darmon | Perform Data Collection, Pre-Processing, Analysis and Visualization | 
|  | Analyse Country-Specific Music Styles |
|  | Develop Helper Functions for Plotting |
|  | Create, Update and Finalise Data Story |
| Mäelle Regnier | Perform Data Collection, Pre-Processing, Analysis and Visualization | 
|  | Analyse Country-Specific Music Styles | 
|  | Define Success | 
|  | Analyse the Impact of Separate Attributes of Music on Movie Success | 
|  | Formulate General Guidelines of How Choosing Music Appropriately can Drive a Movie towards Success |  
|  | Create, Update and Finalise Data Story |



