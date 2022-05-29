# Movieflix


Content based Movie Recommendation System with sentiment Analysis

![Python](https://img.shields.io/badge/Python-3.8-blueviolet)
![Framework](https://img.shields.io/badge/Framework-Flask-red)
![Frontend](https://img.shields.io/badge/Frontend-HTML/CSS/JS-green)
![API](https://img.shields.io/badge/API-TMDB-fcba03)


![](static/website.png)

# About the Recommender System

Content Based Recommender System recommends movies similar to the movie user likes and analyses the sentiments on the reviews given by the user for that movie.

The details of the movies(title, genre, runtime, rating, poster, etc) are fetched using an API by TMDB, https://www.themoviedb.org/documentation/api, and using the IMDB id of the movie in the API, I did web scraping to get the reviews given by the user in the IMDB site using `beautifulsoup4` and performed sentiment analysis on those reviews.

This web application is my submission for the month long challenge to build a video-calling app in Engage'22, a mentorship program conducted by Microsoft.

# Video Demo



## How to get the API key?

Create an account in https://www.themoviedb.org/, click on the `API` link from the left hand sidebar in your account settings and fill all the details to apply for API key. If you are asked for the website URL, just give "NA" if you don't have one. You will see the API key in your `API` sidebar once your request is approved.

## How to run the project?

1. Clone or download this repository to your local machine.
2. Install all the libraries mentioned in the requirements.txt file with the command `pip install -r requirements.txt`.
3. Get your API key from https://www.themoviedb.org/. (Refer the above section on how to get the API key)
4. Replace 'YOUR_API_KEY' in **both** the places (line no. 23 and 43) of `static/recommend.js` file and hit save.(I have saved my api key for reference)
5. Open your terminal/command prompt from your project directory and run the file `myapp.py` by executing the command `python myapp.py`.
6. Go to your browser and type `http://127.0.0.1:5000/` in the address bar.

## How to run the ipynb files on google colab?
Here we have two .iypnb files (Sentiment_Analysis.ipynb and movie_recommender_systems.ipynb) i have made them using google colab due to my computational limitations.
For movie_recommender_systems.ipynb-
1.When we open these files there will be a button on top for open the file in google colab[click on that].
2.Simply mount google drive by running the first cell present.
![image](https://user-images.githubusercontent.com/70278261/170864735-5874b98d-6634-45a9-8e7a-ffc36c8f0dd5.png)
3.Upload the datasets to your google drive(https://github.com/aditya080101/movieflixrec/tree/main/datasets)
4.provide the path to the cell shown below.
![image](https://user-images.githubusercontent.com/70278261/170864823-1e20774f-c9a9-4499-9a27-3ac0e5af3c94.png)
![image](https://user-images.githubusercontent.com/70278261/170864847-84796ed7-ab2e-4aa7-9007-d719ab9d8cf4.png)
![image](https://user-images.githubusercontent.com/70278261/170864880-22b5b5ce-6aa0-4ffa-a2d7-e4eff52bed91.png)
Similarly we can run  Sentiment_Analysis.ipynb on google colab


## Architecture

![Recommendation App](https://user-images.githubusercontent.com/36665975/168742738-5435cf76-1a42-4d87-94b4-999e5bfc48d3.png)

## Similarity Score : 

   How does it decide which item is most similar to the item user likes? Here come the similarity scores.
   
   It is a numerical value ranges between zero to one which helps to determine how much two items are similar to each other on a scale of zero to one. This similarity score is obtained measuring the similarity between the text details of both of the items. So, similarity score is the measure of similarity between given text details of two items. This can be done by cosine-similarity.
   
## How Cosine Similarity works?
  Cosine similarity is a metric used to measure how similar the documents are irrespective of their size. Mathematically, it measures the cosine of the angle between two vectors projected in a multi-dimensional space. The cosine similarity is advantageous because even if the two similar documents are far apart by the Euclidean distance (due to the size of the document), chances are they may still be oriented closer together. The smaller the angle, higher the cosine similarity.
  
  ![image](https://user-images.githubusercontent.com/36665975/70401457-a7530680-1a55-11ea-9158-97d4e8515ca4.png)

  
More about Cosine Similarity : [Understanding the Math behind Cosine Similarity](https://www.machinelearningplus.com/nlp/cosine-similarity/)

### Sources of the datasets 

1. [IMDB 5000 Movie Dataset](https://www.kaggle.com/carolzhangdc/imdb-5000-movie-dataset)
2. [The Movies Dataset](https://www.kaggle.com/rounakbanik/the-movies-dataset)
3. [List of movies in 2018](https://en.wikipedia.org/wiki/List_of_American_films_of_2018)
4. [List of movies in 2019](https://en.wikipedia.org/wiki/List_of_American_films_of_2019)
5. [List of movies in 2020](https://en.wikipedia.org/wiki/List_of_American_films_of_2020)

