


import pandas as pd
import numpy


# In[120]:


movies = pd.read_csv('tmdb_5000_movies.csv')
credits = pd.read_csv('tmdb_5000_credits.csv')


# In[121]:


movies.head(1)


# In[122]:


credits.head(1)


# In[123]:


#credits.head(1)['crew'].values


# In[124]:


movies =  movies.merge(credits,on='title')


# In[125]:


movies.info()


# In[126]:


# genres # id #keywords # title #overview # cast # crew
movies = movies[["movie_id","title","overview","genres","keywords","cast","crew"]]


# In[127]:


movies.head()


# # Preprocessing

# In[128]:


movies.isnull().sum()


# In[129]:


movies.dropna(inplace=True)


# In[130]:


movies.duplicated().sum()


# In[131]:


movies.iloc[0].genres


# In[132]:


# '[{"id": 28, "name": "Action"}, {"id": 12, "name": "Adventure"}, {"id": 14, "name": "Fantasy"}, {"id": 878, "name": "Science Fiction"}]'
#["Action","Adventure","Fantasy","Science Fiction"]


# In[133]:


def convert(obj):
    L =[]
    for i in ast.literal_eval(obj):
        L.append(i['name'])
    return L


# In[134]:


import ast


# In[135]:


convert('[{"id": 28, "name": "Action"}, {"id": 12, "name": "Adventure"}, {"id": 14, "name": "Fantasy"}, {"id": 878, "name": "Science Fiction"}]')


# In[136]:


movies['genres'] = movies['genres'].apply(convert)


# In[137]:


movies['keywords'] = movies['keywords'].apply(convert)


# In[138]:


def convert1(obj): # to fetch 3 actor
    L =[]
    counter =0
    for i in ast.literal_eval(obj):
        if counter!=3:
            L.append(i['name'])
            counter+=1
        else:
            break


    return L


# In[139]:


movies['cast'] = movies['cast'].apply(convert1)


# In[140]:


def fetch_director(obj):
    L =[]
    for i in ast.literal_eval(obj):
        if i['job'] == 'Director':
            L.append(i['name'])
            break
    return L





# In[141]:


movies['crew'] = movies['crew'].apply(fetch_director)


# In[142]:


movies["overview"][0]


# In[143]:


movies["overview"]  = movies["overview"].apply(lambda x:x.split()) # to convert it into list


# In[144]:


movies.head(1)


# In[145]:


# to remove strings
movies['genres'] = movies['genres'].apply(lambda x:[i.replace(" ","")for i in x])
movies['keywords'] = movies['keywords'].apply(lambda x:[i.replace(" ","")for i in x])
movies['cast'] = movies['cast'].apply(lambda x:[i.replace(" ","")for i in x])
movies['crew'] = movies['crew'].apply(lambda x:[i.replace(" ","")for i in x])


# In[146]:


movies["tags"] = movies["overview"] + movies["genres"] + movies["keywords"] + movies["cast"] + movies["crew"]


# In[147]:


movies.head(1)


# In[148]:


movies['tags'][0]


# In[149]:


new_df = movies[["movie_id","title","tags"]]


# In[150]:


new_df.head(1)


# In[153]:


new_df["tags"] = new_df["tags"].apply(lambda x: " ".join(x)) # converting in to string





new_df['tags'][0]



new_df["tags"] = new_df["tags"].apply(lambda x:x.lower())





import nltk
from nltk.stem.porter import PorterStemmer
ps = PorterStemmer()





def stem(text):
    y = []
    for i in text.split():
        y.append(ps.stem(i))
    return " ".join(y)





new_df['tags'] = new_df['tags'].apply(stem)


#  # Vectorization




from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(max_features=5000,stop_words='english')





vectors = cv.fit_transform(new_df['tags']).toarray()





cv.get_feature_names_out()





from sklearn.metrics.pairwise import cosine_similarity




similarity = cosine_similarity(vectors)





similarity[0]





sorted(list(enumerate(similarity[0])),reverse=True, key = lambda x:x[1])[1:6]


# # main function




def recommend(movie):
    movie_index = new_df[new_df['title'] == movie].index[0]
    distance = similarity[movie_index]
    movie_list = sorted(list(enumerate(distance)),reverse=True, key = lambda x:x[1])[1:6]

    for i in movie_list:
        print(new_df.iloc[i[0]].title)







recommend('Avatar')

import pickle

# Save preprocessed movie dataframe and similarity matrix
pickle.dump(movies, open('movies.pkl', 'wb'))
pickle.dump(similarity, open('similarity.pkl', 'wb'))








