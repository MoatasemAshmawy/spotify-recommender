from fastapi import FastAPI
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler
from matplotlib import pyplot as plt
import numpy as np
import json
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests

columns = ["instrumentalness","energy","loudness"]
# scaler = MinMaxScaler()

# test_colors = ["blue",'green','red','yellow','orange','purple','black','pink','brown','grey','magenta','cyan','gold','silver','indigo']

# df = pd.read_csv('backend-python/spotify-data/dataset.csv')
# df = df.drop_duplicates(subset=['track_id'])
# km = KMeans(init="k-means++",
#                 n_clusters=4,
#                 random_state=15,
#                 max_iter = 500)


# df_2 = df[["instrumentalness","energy","loudness"]]

# x = df_2.values 
# x_scaled = scaler.fit_transform(x)
# df_2 = pd.DataFrame(x_scaled,columns=columns)

# print(scaler.data_max_)
# print(scaler.data_min_)

# dict = {
#    "max": scaler.data_max_.tolist(),
#    "min": scaler.data_min_.tolist()
# }

# with open("backend-python/spotify-data/cluster_min.json", "w") as outfile:
#     json.dump(dict, outfile)

# result = km.fit_predict(df_2)



# with open("backend-python/spotify-data/cluster_centers.json", "w") as outfile:
#     json.dump(km.cluster_centers_.tolist(), outfile)

# df_2['cluster'] = result
# df_2["track_id"] = df["track_id"]
# df_2["track_name"] = df["track_name"]

# #convert to csv
# df_2.to_csv('backend-python/spotify-data/dataset_cluster.csv')

# Showing Clusters
# df_dict ={}
# for x in range(4):
#     df_dict[x] = df_2[df_2["cluster"] == x]

 

# for cluster in range(4):    
#   plt.scatter(df_dict[cluster]["loudness"],df_dict[cluster]["instrumentalness"],c=test_colors[cluster])



# plt.show()

def euclidean_distance(x1,x2):
  sum = 0
  for i,point in enumerate(x2):
    sum+= (point - x1[i])**2
  return np.sqrt(sum)

def scale(x,min,max):
  for i,point in enumerate(x):
    x[i] = (point - min[i])/(max[i]-min[i])
  return x

def recommendSongs(liked_songs,cluster_min,cluster_centers,clustered_data):
  recommendations = []
  for song in liked_songs:
    song = scale(song,cluster_min["min"],cluster_min["max"])
    distances = []
    for center in cluster_centers:
      distances.append(euclidean_distance(song,center))
    cluster_index = distances.index(min(distances))
    cluster_data_of_song = clustered_data[clustered_data["cluster"] == cluster_index]
    distances_to_songs_in_cluster  = []
    for index, row in cluster_data_of_song.iterrows():
      distances_to_songs_in_cluster.append({"distance":euclidean_distance(song,[row["instrumentalness"],row["energy"],row["loudness"]]), "id":row["track_id"]})
    distances_to_songs_in_cluster.sort(key=lambda x: x["distance"])
    recommendations.append(distances_to_songs_in_cluster[0:5])
  return recommendations


cluster_min = json.load(open('spotify-data/cluster_min.json'))
cluster_centers = json.load(open('spotify-data/cluster_centers.json'))
clustered_data = pd.read_csv('spotify-data/dataset_cluster.csv')


class Item(BaseModel):
    accessToken: str


app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://localhost:3000/recommendations",
    
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/recommendations")
def recommend(AccessToken: Item):
  
  r = requests.get("https://api.spotify.com/v1/me/tracks?limit=5&offset=0",headers={"Authorization": f"Bearer {AccessToken.accessToken}"} )
  req_data = r.json()
  tracks = req_data["items"]
  liked_songs = []
  for track in tracks:
    result = []
    req = requests.get(f"https://api.spotify.com/v1/audio-features/{track['track']['id']}",headers={"Authorization": f"Bearer {AccessToken.accessToken}"} )
    song = req.json()
    result.append(song["instrumentalness"])
    result.append(song["energy"]) 
    result.append(song["loudness"]) 
    liked_songs.append(result)
  recommendations_id = recommendSongs(liked_songs,cluster_min,cluster_centers,clustered_data)
  tracks_ids_string = ""
  for recommendation_list in recommendations_id:
    for song in recommendation_list:
      tracks_ids_string+= f'{song["id"]},'
  get_tracks_req = requests.get(f"https://api.spotify.com/v1/tracks?ids={tracks_ids_string}",headers={"Authorization": f"Bearer {AccessToken.accessToken}"} )
  return get_tracks_req.json()
  