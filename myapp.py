import numpy as np
import pandas as pd
from flask import Flask, render_template, request
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json
import bs4 as bs
import urllib.request
import pickle
import requests
from datetime import date, datetime

# load the nlp model and tfidf vectorizer from disk
filename = 'sentiment.pkl'
clf = pickle.load(open(filename, 'rb'))
vectorizer = pickle.load(open('tranform.pkl','rb'))

#loading our dataset and some important files to get our recommendations
small_data1=pickle.load(open('movie_list.pkl','rb'))
count = CountVectorizer(analyzer='word',ngram_range=(1, 2),min_df=0, stop_words='english')
count_matrix = count.fit_transform(small_data1['combination'])
small_data1 = small_data1.reset_index()
titles = small_data1['title']
indices = pd.Series(small_data1.index, index=small_data1['title'])
all_titles = [small_data1['title'][i] for i in range(len(small_data1['title']))]
cosine_sim = cosine_similarity(count_matrix, count_matrix)
  
#getting recommendations for our movie    
def get_recommendations1(title):
    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    try:
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    except:
        sim_scores = sorted(sim_scores, key=lambda x: x[1][1], reverse=True)  
    sim_scores = sim_scores[1:6]
    movie_indices = [i[0] for i in sim_scores]
    tit = small_data1['title'].iloc[movie_indices]
    dat = small_data1['release_date'].iloc[movie_indices]
    rating = small_data1['vote_average'].iloc[movie_indices]
    org_title=small_data1['original_title'].iloc[movie_indices]
    poster=small_data1['poster'].iloc[movie_indices]
    return_df = pd.DataFrame(columns=['Title','Year'])
    return_df['Title'] = tit
    return_df['Year'] = dat
    return_df['Ratings'] = rating
    return_df['org_title']=org_title
    return_df['poster'] =poster
    sorted_df = return_df.sort_values(by=['Ratings'], ascending=False)
    return sorted_df

# converting list of string to list (eg. "["abc","def"]" to ["abc","def"])
def convert_to_list(my_list):
    my_list = my_list.split('","')
    my_list[0] = my_list[0].replace('["','')
    my_list[-1] = my_list[-1].replace('"]','')
    return my_list

# convert list of numbers to list (eg. "[1,2,3]" to [1,2,3])
def convert_to_list_num(my_list):
    my_list = my_list.split(',')
    my_list[0] = my_list[0].replace("[","")
    my_list[-1] = my_list[-1].replace("]","")
    return my_list

def get_suggestions():
    return list(small_data1['title'].str.capitalize())

app = Flask(__name__)

@app.route("/")
@app.route("/home")
def home():
    
    suggestions = get_suggestions()
    return render_template('home.html',suggestions=suggestions)


@app.route("/recommend",methods=["POST"])
def recommend():
    # getting data from AJAX request
    title = request.form['title']
    cast_ids = request.form['cast_ids']
    cast_names = request.form['cast_names']
    cast_chars = request.form['cast_chars']
    cast_bdays = request.form['cast_bdays']
    cast_bios = request.form['cast_bios']
    cast_places = request.form['cast_places']
    cast_profiles = request.form['cast_profiles']
    imdb_id = request.form['imdb_id']
    poster = request.form['poster']
    genres = request.form['genres']
    overview = request.form['overview']
    vote_average = request.form['rating']
    vote_count = request.form['vote_count']
    rel_date = request.form['rel_date']
    release_date = request.form['release_date']
    runtime = request.form['runtime']
    status = request.form['status']
    
    # get movie suggestions for auto complete
    suggestions = get_suggestions()

    # call the convert_to_list function for every string that needs to be converted to list
    cast_names = convert_to_list(cast_names)
    cast_chars = convert_to_list(cast_chars)
    cast_profiles = convert_to_list(cast_profiles)
    cast_bdays = convert_to_list(cast_bdays)
    cast_bios = convert_to_list(cast_bios)
    cast_places = convert_to_list(cast_places)
    
    # convert string to list (eg. "[1,2,3]" to [1,2,3])
    cast_ids = convert_to_list_num(cast_ids)

    # rendering the string to python string
    for i in range(len(cast_bios)):
        cast_bios[i] = cast_bios[i].replace(r'\n', '\n').replace(r'\"','\"')

    for i in range(len(cast_chars)):
        cast_chars[i] = cast_chars[i].replace(r'\n', '\n').replace(r'\"','\"') 
    
    
    movie_name = request.form['title']
    if movie_name not in all_titles:
        return render_template('negative.html',name=movie_name)
    
    #calling recommendation function to get details of the recommended movies.
    movies= get_recommendations1(movie_name)
    rec_movies = movies.Title.to_list()
    rec_posters = movies.poster.to_list()
    rec_movies_org = movies.org_title.to_list()
    rec_year = movies.Year.to_list()
    rec_vote = movies.Ratings.to_list()

    # combining multiple lists as a dictionary which can be passed to the html file so that it can be processed easily and the order of information will be preserved
    movie_cards = {rec_posters[i]: [rec_movies[i],rec_movies_org[i],rec_vote[i],rec_year[i]] for i in range(len(rec_posters))}

    casts = {cast_names[i]:[cast_ids[i], cast_chars[i], cast_profiles[i]] for i in range(len(cast_profiles))}

    cast_details = {cast_names[i]:[cast_ids[i], cast_profiles[i], cast_bdays[i], cast_places[i], cast_bios[i]] for i in range(len(cast_places))}

    # web scraping to get user reviews from IMDB site
    sauce = urllib.request.urlopen('https://www.imdb.com/title/{}/reviews?ref_=tt_ov_rt'.format(imdb_id)).read()
    soup = bs.BeautifulSoup(sauce,'lxml')
    soup_result = soup.find_all("div",{"class":"text show-more__control"})

    reviews_list = [] # list of reviews
    reviews_status = [] # list of comments (good or bad)
    for reviews in soup_result:
        if reviews.string:
            reviews_list.append(reviews.string)
            # passing the review to our model
            movie_review_list = np.array([reviews.string])
            movie_vector = vectorizer.transform(movie_review_list)
            pred = clf.predict(movie_vector)
            reviews_status.append('Positive' if pred else 'Negative')

    # getting current date
    movie_rel_date = ""
    curr_date = ""
    if(rel_date):
        today = str(date.today())
        curr_date = datetime.strptime(today,'%Y-%m-%d')
        movie_rel_date = datetime.strptime(rel_date, '%Y-%m-%d')

    # combining reviews and comments into a dictionary
    movie_reviews = {reviews_list[i]: reviews_status[i] for i in range(len(reviews_list))}     

    # passing all the data to the html file
    return render_template('recommend.html',title=title,poster=poster,overview=overview,vote_average=vote_average,
        vote_count=vote_count,release_date=release_date,movie_rel_date=movie_rel_date,curr_date=curr_date,runtime=runtime,status=status,genres=genres,movie_cards=movie_cards,reviews=movie_reviews,casts=casts,cast_details=cast_details)

if __name__ == '__main__':
    app.run(debug=True)
