# How Music Moves Movies

## Abstract:
Hit musical numbers from the blockbuster movies ‘Dilwale Dulhania Le Jayenge’ and ‘Titanic’ continue to occupy a special place in people’s hearts even today. _“Where words fail, music speaks.”_ This might make you think: What are the secret ingredients of music that enrapture all of us and how does it add magic to movies? With this thought in mind, we will use the [CMU Movie Summary Corpus](http://www.cs.cmu.edu/~ark/personas/) and our [Spotify Dataset](https://drive.google.com/file/d/1THSbO-U5ZIc-K8-NL3pYrrS2utNjUf5f/view?usp=share_link) to find out the dominant music attributes (danceability, energy, valence, etc.) in different genres of movies globally so as to possibly reveal any connections between the dominant type of music in a particular movie genre and the cultural identity of a particular country. Subsequently, we will observe the change in the overall attribute mix of music and its interplay with the changes in the overall genre and emotions portrayed by the movies across the years. Finally, we will connect all the dots to reveal how music moves movies towards success.

## Research Questions: 
1. What are the connections (if any) between the dominant type of music in a particular movie genre and the cultural identity of a particular country?
2. How has the overall attribute mix of music (in movies) changed (if so) across the years? What is its interplay (if any) with the change in the overall genre and emotions portrayed by the movies across the years?
3. Can a certain music style move a movie towards success? If so, how?

## Additional Datasets: 
1. [Spotify Dataset](https://drive.google.com/file/d/1THSbO-U5ZIc-K8-NL3pYrrS2utNjUf5f/view?usp=share_link): We scraped music album data from [Spotify](https://developer.spotify.com/documentation/web-api) using the [Spotipy Python Library](https://spotipy.readthedocs.io/en/2.22.1/) corresponding to the movies in the CMU Movie Summary Corpus. `spotify_scraper.py` details how we scraped the data and all the features in our music dataset. Owing to rate limits imposed by Spotify's Web API, we have only scraped and conducted our analysis on a subset of the entire movies data but we will extend this analysis by finishing the scraping of the data while working on Milestone 3.
2. [MovieLens Metadata Dataset](https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset): We plan to use this dataset in order to fill in the missing values in the movies metadata dataset.
3. [USD CPI Dataset](https://www.usinflationcalculator.com/inflation/consumer-price-index-and-annual-percent-changes-from-1913-to-2008/): We used this dataset for adjusting movie box office revenues for inflation and hence, removing correlation between box office revenue and release year of the movies.
4. [IMDb Dataset](http://www.imdb.com/interfaces/): We plan to use this dataset for obtaining the user ratings and votes of movies in the movies metadata dataset for analysing how music moves movies towards success.

## Methods:

PART 1: Understanding the Interlinkages between Music and Culture:
 - Data Collection, Pre-Processing, Analysis and Visualization:
    - Movies Metadata Dataset (from CMU Movie Summary Corpus):
       - We eliminated all the duplicates of movie records from the dataset identified using all the attributes corresponding to the movies.
       - We checked for missing values in the dataset and found out that a lot of values of `Movie_Release_Date`, `Movie_Box_Office_Revenue` and `Movie_Runtime` were missing. (We plan to fill up some of these using the MovieLens MetaData Dataset.)
       - We found out a strong correlation between `Movie_Box_Office_Revenue` and `Movie_Release_Year` and adjusted the revenues for inflation using the USD CPI Dataset to remove this correlation (Useful for PART 3)
       - We identified the top 10 `Movie_Genres`, `Movie_Countries` and `Movie_Languages` (by the number of movies), used pie charts for understanding the movie count breakup amongst them and visualized and analysed the `Movie_Box_Office_Revenue` and `Movie_Runtime` using boxplots and lineplots (w.r.t. `Movie_Release_Year`) (Useful for PART 3)
    - Spotify Dataset:
       - We averaged and took the maximum of the relevant audio features of tracks across the movie albums individually so as to obtain a movie wise music attribute mix.
       - We visualised all the relevant averaged features of music corresponding to movies using a scatterplot matrix.
 - Analysis of Links between Music and Culture - We will group the music data by the top 10 genres, countries and languages and visualise and analyse all the relevant averaged features of music using boxplots and lineplots (w.r.t. `Movie_Release_Year`). We will then use t-tests to check for and analyse any significant differences in the attribute mix of music in movies in certain different countries. Next, since culture is extremely difficult to quantify and datasets available online are mostly biased against Asian and African countries, we will examine these biases and use relevant research articles and books to manually understand the links between culture and music in an unbiased, qualitative manner.


PART 2: Connecting Music with Emotions Portrayed by Movies:
 - Emotion Classification cum Analysis of the Plot Summaries of Movies: We will be using the plot summaries dataset from the CMU Movie Summary Corpus for extracting plot summaries of the movies. We will augment the plot summary dataset using the IMDb Dataset and the MovieLens Metadata dataset if required. Subsequently, we will use transformers such as BERT and/or RoBERTa for affecting an emotion classification cum analysis (e.g., amount of love, anger, sadness, etc. in films) of the plot summaries.
 - Time Series Analysis of the Dominant Emotions across the Years and the Attribute Mix of Music across the Years: For both the two time series, we will check for any trends using Linear Regression, their stationarity using the Augmented Dickey Fuller (ADF) Test and examine the best Autoregressive Integrated Moving Average (ARIMA) and/or Generalised Autoregressive Conditional Heteroscedastic (GARCH) Model Fits using results obtained from the Lagrange Multiplier (LM) Test and Akaike’s Information Criteria (AIC).  We plan to check their predictive power as well. Finally, we will check for long run relationships between the 2 time series using Johansen’s Cointegration Test.

PART 3: How does Music Drive Movies Towards Success:
 - Defining Success: We plan to use the IMDb dataset since it has information on the user ratings and votes for movies and analyse their distributions in conjunction with box office revenue to come up with a notion of success.
 - Analysis of the Impact of Separate Attributes of Music on Movie Success: We will implement this using paired matching to control for the effect of any confounders and t-tests
 - We will finally formulate general guidelines (our predictions) of how choosing music appropriately can drive a movie towards success.


## Proposed Timeline:
| Deadline | Parts of Research Questions | Data Story |
| ------------- | ------------- | ------------- |
| 17/11/2023  |  Perform Data Collection, Pre-Processing, Analysis and Visualization (Movies Metadata Dataset + Sample of Spotify Dataset) |   |
| 27/11/2023  | Complete Scraping of Spotify Dataset Data Collection, Pre-Processing, Analysis and Visualization (Extension to fully scraped Spotify Dataset) | Develop Initial Framework for Data Story |
| 1/12/2023  | Analyse Links between Music and Culture | Develop Initial Rendition of Data Story  |
| 8/12/2023  | Perform Emotion Classification cum Analysis of the Plot Summaries of Movies | Update Data Story  |
|   | Define Success |  |
|   | Analyse the Impact of Separate Attributes of Music on Movie Success |  |
| 15/12/2023 | Perform Time Series Analysis of the Dominant Emotions across the Years and the Attribute Mix of Music across the Years | Update Data Story |
|   | Analysis of Separate Attributes of Music on Movie Success (contd.) |   |
|   | Formulate General Guidelines of How Choosing Music Appropriately can Drive a Movie towards Success | |
| 22/12/2023  | Finalise Everything and Submit | Finalise Data Story and Submit |


## Organization within the Team: 
| Name | Project Work |
| ------------- | ------------- | 
| Anand Choudhary | Perform Data Collection, Pre-Processing, Analysis and Visualization | 
|  | Develop the Spotify Data Scraper | 
|  | Analyse Links between Music and Culture | 
|  | Perform Emotion Classification cum Analysis of the Plot Summaries of Movies | 
|  | Perform Time Series Analysis of the Dominant Emotions across the Years and the Attribute Mix of Music across the Years | 
|  | Formulate General Guidelines of How Choosing Music Appropriately can Drive a Movie towards Success | 
|  | Create, Update and Finalise Data Story |
| Stefanie Helfenstein | Perform Data Collection, Pre-Processing, Analysis and Visualization | 
|  | Analyse Links between Music and Culture | 
|  | Define Success | 
|  | Analyse the Impact of Separate Attributes of Music on Movie Success | 
|  | Formulate General Guidelines of How Choosing Music Appropriately can Drive a Movie towards Success |  
|  | Create, Update and Finalise Data Story |
| Romain Defferrard | Perform Data Collection, Pre-Processing, Analysis and Visualization | 
|  | Analyse Links between Music and Culture | 
|  | Perform Emotion Classification cum Analysis of the Plot Summaries of Movies | 
|  | Perform Time Series Analysis of the Dominant Emotions across the Years and the Attribute Mix of Music across the Years | 
|  | Create, Update and Finalise Data Story |
| Samuel Darmon | Perform Data Collection, Pre-Processing, Analysis and Visualization | 
|  | Develop Helper Functions for Plotting | 
|  | Analyse Links between Music and Culture | 
|  | Perform Emotion Classification cum Analysis of the Plot Summaries of Movies | 
|  | Perform Time Series Analysis of the Dominant Emotions across the Years and the Attribute Mix of Music across the Years |
|  | Create, Update and Finalise Data Story |
| Mäelle Regnier | Perform Data Collection, Pre-Processing, Analysis and Visualization | 
|  | Analyse Links between Music and Culture | 
|  | Define Success | 
|  | Analyse the Impact of Separate Attributes of Music on Movie Success | 
|  | Formulate General Guidelines of How Choosing Music Appropriately can Drive a Movie towards Success |  
|  | Create, Update and Finalise Data Story |


