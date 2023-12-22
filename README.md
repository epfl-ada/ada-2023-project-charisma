# How Music Moves Movies

Link to our Datastory: [https://team-charisma.github.io](https://team-charisma.github.io)

## Abstract:
Hit musical numbers from the blockbuster movies ‘Dilwale Dulhania Le Jayenge’ and ‘Titanic’ continue to occupy a special place in people’s hearts even today. This might make you think: What are the secret ingredients of music that enrapture all of us and how does it add magic to the movies? With this thought in mind, we will use the CMU Movie Summary Corpus and our [Spotify Dataset](https://drive.google.com/file/d/1THSbO-U5ZIc-K8-NL3pYrrS2utNjUf5f/view?usp=share_link) to find out the dominant music attributes (danceability, energy, liveness, etc.) in different countries across the world so as to possibly reveal country-specific music styles for the top 3 countries (in our combined movie and music dataset). Subsequently, we will observe the change in music features and their interplay with the changes in the emotions portrayed by movies in the top 2 countries (in our combined movie, music and emotion dataset) across the years. Finally, we will connect all the dots to reveal how music moves movies towards success. 

## Research Questions: 
1. What are the country-specific music styles?
2. How has music (in movies) changed (if so) across the years? What is its interplay (if any) with the change in the emotions portrayed by the movies across the years?
3. Can a certain music style move a movie towards success? If so, how?

## Additional Datasets: 
1. [Spotify Dataset](https://drive.google.com/file/d/1THSbO-U5ZIc-K8-NL3pYrrS2utNjUf5f/view?usp=share_link): We scraped music album data from [Spotify](https://developer.spotify.com/documentation/web-api) using the [Spotipy Python Library](https://spotipy.readthedocs.io/en/2.22.1/) corresponding to the movies in the CMU Movie Summary Corpus. `spotify_scraper.py` details how we scraped the data and all the features in our music dataset. Owing to rate limits imposed by Spotify's Web API, we have only scraped and conducted our analysis on a subset of the entire movies data but we will extend this analysis by finishing the scraping of the data while working on Milestone 3.
2. [USD CPI Dataset](https://www.usinflationcalculator.com/inflation/consumer-price-index-and-annual-percent-changes-from-1913-to-2008/): We used this dataset for adjusting movie box office revenues for inflation and hence, removing correlation between box office revenue and release year of the movies.


## Methods:

PART 1: Understanding the Interlinkages between Music and Culture:
 - Data Collection, Pre-Processing, Analysis and Visualization:
    - Movies Metadata Dataset (from CMU Movie Summary Corpus):
       - We eliminated all the duplicates of movie records from the dataset identified using all the attributes corresponding to the movies.
       - We checked for missing values in the dataset and found out that a lot of values of `Movie_Release_Date`, `Movie_Box_Office_Revenue` and `Movie_Runtime` were missing. We planed to fill up some of these using the MovieLens MetaData Dataset, but as the contribution of this dataset wasn't as big as expected, we decided to leave it out.
       - We found out a strong correlation between `Movie_Box_Office_Revenue` and `Movie_Release_Year` and adjusted the revenues for inflation using the USD CPI Dataset to remove this correlation (Useful for PART 3)
       - We identified the top 10 `Movie_Genres`, `Movie_Countries` and `Movie_Languages` (by the number of movies), used pie charts for understanding the movie count breakup amongst them and visualized and analysed the `Movie_Box_Office_Revenue` and `Movie_Runtime` using boxplots and lineplots (w.r.t. `Movie_Release_Year`)
    - Spotify Dataset:
       - We averaged and took the maximum of the relevant audio features of tracks across the movie albums individually so as to obtain a movie wise music attribute mix.
       - We visualised all the relevant averaged features of music corresponding to movies using a scatterplot matrix.
 - Analysis of Links between Music and Culture  We grouped the music data by the top 10 genres, countries, languages. We visualized them and analyzed the differences. We identified especially differences between the Countries India and the rest, as well as for the languages Hindi, Tamil, Malayalam and the rest. We used t-tests to check for and analyse the differences observed. 


PART 2: Connecting Music with Emotions Portrayed by Movies:
 - Emotion Classification cum Analysis of the Plot Summaries of Movies: We  used the plot summaries dataset from the CMU Movie Summary Corpus for extracting plot summaries of the movies. Subsequently, we used transformers such as BERT and/or RoBERTa for affecting an emotion classification cum analysis (e.g., amount of love, anger, sadness, etc. in films) of the plot summaries.
 - Time Series Analysis of the Dominant Emotions across the Years and the Attribute Mix of Music across the Years: For both the two time series, we will check for any trends using Linear Regression, their stationarity using the Augmented Dickey Fuller (ADF) Test and examine the best Autoregressive Integrated Moving Average (ARIMA) and/or Generalised Autoregressive Conditional Heteroscedastic (GARCH) Model Fits using results obtained from the Lagrange Multiplier (LM) Test and Akaike’s Information Criteria (AIC).  We plan to check their predictive power as well. Finally, we will check for long run relationships between the 2 time series using Johansen’s Cointegration Test.

PART 3: How does Music Drive Movies Towards Success:
 - Defining Success: We first planned to use an additional dataset, the IMDb dataset, since it had information on the user ratings and votes for movies. But when we merged with the original dataset, we realised that the dataset wasn't big enough and had too many 0 values to give us a significant contribution. We therefore made the hypothesis, that the success is just defined by Movie Box Office Revenue, although we are well aware that this hypothesis is just an approximation. 
 - Analysis of the Impact of Separate Attributes of Music on Movie Success: We implemented this using paired matching to control for the effect of any confounders and t-tests. 
 - We finally formulate general guidelines (our predictions) of how choosing music appropriately can drive a movie towards success.


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


## Organization/Contribution within the Team:
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



