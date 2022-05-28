# Microsoft Engage Mentorship Program'22 Project   
## MUSICA: A music recommendation web app
## 🚩 Overview 
#### We all use at least one audio-streaming app like Spotify on a daily basis. Isn’t it fascinating that most of the time Spotify is able to recommend songs that we would like to listen to at that moment? After researching more about how the algorithms of audio streaming apps work, I have built Musica: a web app which can give music recommendations based on what the user is currently listening to and the user's song history. The web app makes use of **content based filtering** using the **cosine similarity algorithm** to generate recommendations. 
  
## 🚩 Problem statement (as given):
#### Demonstrate through your app the different kinds of algorithms that a web-streaming app (like Netflix) or an audio-streaming app (like Spotify) may use for their Recommendation Engine.  
- [x] Status : Accomplised by successfully recommending songs to the user 

### UI Glimpse of the App:

#### Screen 01  
<img width=100% src="https://github.com/dishitarocks/Books/blob/cb1caa0c22404551120554015fcd7a6e6ea50a49/Useful%20Images/recommendor_screen1.jpeg"> 

#### Screen 02 
<img width=100% src="https://github.com/dishitarocks/Books/blob/cb1caa0c22404551120554015fcd7a6e6ea50a49/Useful%20Images/recommendor_screen2.jpeg">


## 🔗 Links for project:
#### Video link : [https://youtu.be/Xolry9YlK7I](https://youtu.be/Xolry9YlK7I)  

## 🌐 Web flow
<img width=100% src="https://github.com/dishitarocks/Books/blob/3bde4702b5a346894f388a1f5c61d61d00fff317/Useful%20Images/web%20flow.png" >

## 🚩 Algorithm used: Cosine Similarity

#### Cosine similarity is a metric used to measure how similar two items are. Mathematically it calculates the cosine of the angle between two vectors projected in a multidimensional space. Cosine similarity is advantageous when two similar documents are far apart by Euclidean distance(size of documents) chances are they may be oriented close together. The smaller the angle, higher the cosine similarity.

<img width=100% src="https://github.com/dishitarocks/Books/blob/c38385fcbad6c22a1e1967cac1b610ff87db59e1/Useful%20Images/cosine2.jpeg" >

#### Cosine similarity has been used in the web app to implement content based filtering. Content-based filtering uses item features to recommend other items similar to what the user likes, based on their previous actions or explicit feedback sklearn has the module ‘cosine_similarity’, which we'll use to compute the similarity between two vectors.

<img width=100% src="https://github.com/dishitarocks/Books/blob/c38385fcbad6c22a1e1967cac1b610ff87db59e1/Useful%20Images/cosine1.png" >

##  🚩 Technologies used:

<h3 align="left">Frontend Stacks </h3>
<p align="left"> <a href="https://www.w3.org/html/" target="_blank"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/html5/html5-original-wordmark.svg" alt="html5" width="40" height="40"/> </a>  <a href="https://www.w3schools.com/css/" target="_blank"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/css3/css3-original-wordmark.svg" alt="css3" width="40" height="40"/> </a>  <a href="https://developer.mozilla.org/en-US/docs/Web/JavaScript" target="_blank"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/javascript/javascript-original.svg" alt="javascript" width="40" height="40"/> </a>  </p>

<h3 align="left"> Backend Stacks </h3>
<p align="left"> <a href="https://www.python.org" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" alt="python" width="40" height="40"/> </a> <a href="https://flask.palletsprojects.com/" target="_blank" rel="noreferrer"> <img src="https://www.vectorlogo.zone/logos/pocoo_flask/pocoo_flask-icon.svg" alt="flask" width="40" height="40"/> </a>  </p>

<h3 align="left"> ML Libraries </h3>
<p align="left"> <a href="https://scikit-learn.org/" target="_blank" rel="noreferrer"> <img src="https://upload.wikimedia.org/wikipedia/commons/0/05/Scikit_learn_logo_small.svg" alt="scikit_learn" width="40" height="40"/> </a> <a href="https://pandas.pydata.org/" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/2ae2a900d2f041da66e950e4d48052658d850630/icons/pandas/pandas-original.svg" alt="pandas" width="40" height="40"/> </a> <a href="https://numpy.org/doc/stable/index.html" target="_blank" rel="noreferrer"> <img src="https://numpy.org/doc/stable/_static/numpylogo.svg" alt="numpy" width="60" height="60"/> </a>  </p>



## 🚩Installation/Environment Setup 

  #### 1. Clone App
  
  * Make a new folder and open the terminal there.
  * Write the following command and press enter.
  
  ```
    $ git clone https://yoursrepourl
  ```
    
 #### 2. Install packages
  * Write the following command and press enter to download all required node modules.
 
   ```
   pip install -r requirements.txt
  ```
  
#### 3. Run Locally

 * While you are still inside the cloned folder, write the following command to run the website locally. 
 
 ```
   recommendation_system.py
 ```
  
 ###### NOTE: The port by default will be ```http://127.0.0.1:5000```

## 🚩 Future Scope:-
1. Strengthening the algorithm further to increase accuracy 
2. Generating daily song recommendation playlists
3. Implementing collaborative filtering to create a hybrid recommendation model. 


Thank you Microsoft for such a wonderful mentorship program ❤️

