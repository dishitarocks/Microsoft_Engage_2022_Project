#Importing libraries

import pandas as pd
import numpy as np
import json
import re 
import sys
import itertools
import warnings
warnings.filterwarnings("ignore")
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler
from collections import defaultdict

import os
import flask
import random
from flask import Flask, request


class recommendation_system:

    def __init__(self):

        #reading the data
        self.music_info_dataset = pd.read_csv('data/data.csv')
        data_w_genre = pd.read_csv('data/data_w_genres.csv')

        data_w_genre['genres_upd'] = data_w_genre['genres'].apply(lambda x: [re.sub(' ','_',i) for i in re.findall(r"'([^']*)'", x)])
        self.music_info_dataset['artists_upd_v1'] = self.music_info_dataset['artists'].apply(lambda x: re.findall(r"'([^']*)'", x))
        self.music_info_dataset[self.music_info_dataset['artists_upd_v1'].apply(lambda x: not x)].head(5)
        self.music_info_dataset['artists_upd_v2'] = self.music_info_dataset['artists'].apply(lambda x: re.findall('\"(.*?)\"',x))
        self.music_info_dataset['artists_upd'] = np.where(self.music_info_dataset['artists_upd_v1'].apply(lambda x: not x), self.music_info_dataset['artists_upd_v2'], self.music_info_dataset['artists_upd_v1'] )
        self.music_info_dataset['artists_song'] = self.music_info_dataset.apply(lambda row: row['artists_upd'][0]+row['name'],axis = 1)
        self.music_info_dataset.sort_values(['artists_song','release_date'], ascending = False, inplace = True)
        self.music_info_dataset.drop_duplicates('artists_song',inplace = True)

        artists_exploded = self.music_info_dataset[['artists_upd','id']].explode('artists_upd')
        artists_exploded_enriched = artists_exploded.merge(data_w_genre, how = 'left', left_on = 'artists_upd',right_on = 'artists')
        artists_exploded_enriched_nonnull = artists_exploded_enriched[~artists_exploded_enriched.genres_upd.isnull()]
        artists_genres_consolidated = artists_exploded_enriched_nonnull.groupby('id')['genres_upd'].apply(list).reset_index()
        artists_genres_consolidated['consolidates_genre_lists'] = artists_genres_consolidated['genres_upd'].apply(lambda x: list(set(list(itertools.chain.from_iterable(x)))))

        self.music_info_dataset = self.music_info_dataset.merge(artists_genres_consolidated[['id','consolidates_genre_lists']], on = 'id',how = 'left')
        self.music_info_dataset['year'] = self.music_info_dataset['release_date'].apply(lambda x: x.split('-')[0])
        self.float_cols = self.music_info_dataset.dtypes[self.music_info_dataset.dtypes == 'float64'].index.values
        # create 5 point buckets for popularity 
        self.music_info_dataset['popularity_red'] = self.music_info_dataset['popularity'].apply(lambda x: int(x/5))
        # tfidf can't handle nulls so fill any null values with an empty list
        self.music_info_dataset['consolidates_genre_lists'] = self.music_info_dataset['consolidates_genre_lists'].apply(lambda d: d if isinstance(d, list) else [])

        self.complete_feature_set = self.create_feature_set(self.music_info_dataset, float_cols=self.float_cols)

    def get_random(self):
        d = self.music_info_dataset
        keys = random.sample(list(d["id"]), 10)
        values = []
        for k in keys:
            values.append(d[(d["id"] == str(k))][['name','year', 'duration_ms', 'id']].to_dict())

        return values

    def get_by_id(self, id):
        d = self.music_info_dataset
        return d[(d["id"] == str(id))][['name','year', 'duration_ms', 'id']].to_dict()

    def read_data(self , user_type_input):

        #self.recommend_songs([{'name': 'La Victoire De La Madelon', 'year':1921}],  self.music_info_dataset , self.complete_feature_set)
        recommended_songs_info = self.recommend_songs(user_type_input,  self.music_info_dataset , self.complete_feature_set)
        return recommended_songs_info

    def one_hot_encoding(self,df, column, new_name): 

        """ 
    Create One Hot Encoded features of a specific column

    Parameters: 
        df (pandas dataframe): Spotify Dataframe
        column (str): Column to be processed
        new_name (str): new column name to be used
        
    Returns: 
        tf_df: One hot encoded features 
    """
    
        tf_df = pd.get_dummies(df[column])
        feature_names = tf_df.columns
        tf_df.columns = [new_name + "|" + str(i) for i in feature_names]
        tf_df.reset_index(drop = True, inplace = True)    
        return tf_df

    def create_feature_set(self,df, float_cols):

        """ 
            Process spotify df to create a final set of features that will be used to generate recommendations

            Parameters: 
                df (pandas dataframe): Spotify Dataframe
                float_cols (list(str)): List of float columns that will be scaled 
                
            Returns: 
                final: final set of features 
        """
    
        #tfidf genre lists
        tfidf = TfidfVectorizer()
        tfidf_matrix =  tfidf.fit_transform(df['consolidates_genre_lists'].apply(lambda x: " ".join(x)))
        genre_df = pd.DataFrame(tfidf_matrix.toarray())
        genre_df.columns = ['genre' + "|" + i for i in tfidf.get_feature_names()]
        genre_df.reset_index(drop = True, inplace=True)
  
        #explicity_ohe = ohe_prep(df, 'explicit','exp')
        year_ohe = self.one_hot_encoding(df, 'year','year') * 0.5
        popularity_ohe = self.one_hot_encoding(df, 'popularity_red','pop') * 0.15

        #scale float columns
        floats = df[self.float_cols].reset_index(drop = True)
        scaler = MinMaxScaler()
        floats_scaled = pd.DataFrame(scaler.fit_transform(floats), columns = floats.columns) * 0.2

        #concanenate all features
        final = pd.concat([genre_df, floats_scaled, popularity_ohe, year_ohe], axis = 1)
        
        #add song id
        final['id']=df['id'].values
        
        return final
    
    def name_to_id(self,user_input, music_data):
        song_id = []
        try:
            for song in user_input:
                
                song_id.append(music_data[(music_data['year'] == str(song['year'])) & (music_data['name'] == song['name'])].iloc[0:])
                                    
            return song_id
        
        except IndexError:
            
            return 0

    def user_input_feature_formation(self,user_input , music_data , feature_music_data ):

        user_song_features =[]
        song_id = self.name_to_id(user_input, music_data)
        
        for ty in song_id:
            
            user_song_features.append(feature_music_data[(feature_music_data['id'] == ty['id'].iloc[0])])
            index = str(feature_music_data[(feature_music_data['id'] == ty['id'].iloc[0])].index)
            tempi = str()
            for i in index[12:]:
                if(i==']'):
                    break
                else:
                    tempi = tempi + i

            index=int(tempi)

            user_song_features[0] = user_song_features[0].drop('id', axis = 1)
            
        return user_song_features, index


    def id_to_name_and_year(self,best_recommendations_ids , music_data):
    
        recommended_songs_info =[]

        try:
            for cvb in best_recommendations_ids.iloc[0:]:
                recommended_songs_info.append(music_data[(music_data['id'] == cvb)][['name','year', 'duration_ms', 'id']].to_dict())
            return recommended_songs_info
        
        except IndexError:
            return 0


    def recommend_songs(self, user_input , music_data , feature_music_data , top_recommendations = 15):

        user_song_features, index = self.user_input_feature_formation(user_input , music_data , feature_music_data)

        try:
            feature_music_data_subset = feature_music_data.iloc[index-20000 : index+20000]

        except:

            try:
                feature_music_data_subset = feature_music_data.iloc[0 : index+20000]

            except:
                feature_music_data_subset = feature_music_data.iloc[index-20000 : -1 ]

        # applying cosine similarity      
        feature_music_data_subset['similarity_ratio'] = cosine_similarity(feature_music_data_subset.drop('id', axis = 1).values, user_song_features[0].values.reshape(1, -1))[:,0]

        best_recommendations = feature_music_data_subset.sort_values('similarity_ratio',ascending = False).iloc[1:top_recommendations+1]

        best_recommendations_ids = best_recommendations["id"]
        
        recommended_songs_info = self.id_to_name_and_year(best_recommendations_ids, music_data)

        return recommended_songs_info

recommendation_system_ = recommendation_system()

#using flask to integrate the backend with the frontend files
app=Flask(__name__, static_url_path='', static_folder='static')
@app.route('/')
def index():
    print('here')
    return app.send_static_file('index.html')

@app.route('/predict',methods = ['GET'])
def result():
    name = request.args.get('name')
    year = request.args.get('year')

    print(name, year)

    user_typed_input = [{'name': name, 'year': year}]
    output = recommendation_system_.read_data(user_typed_input)

    return json.dumps(output)


@app.route('/random',methods = ['GET'])
def getRandom():
    data = recommendation_system_.get_random()
    return json.dumps(data)

@app.route('/song',methods = ['GET'])
def getSong():
    id = request.args.get('id')
    data = recommendation_system_.get_by_id(id)
    return json.dumps(data)


if __name__ == '__main__':
    app.run(debug=True)