# -*- coding: utf-8 -*-

PATH = "C:\\Users\\akhilg\\Documents\\CollegeDocuments\\BDMA\\CentralSuperlec\\Coursework\\DM\\Assignments\\Assignment 4\\Gupta-Assignment-4"
assert len(PATH)>0,"Please set the path where the folder has been unzipped."

from math import sqrt, isnan, exp
import pandas as pd



# Manhattan similarity function
def sim_distanceManhattan(person1, person2):
    p1_values = [*(person1).values()]
    p2_values = [*(person2).values()]
    return round(sum( abs(a-b) if not isnan(a) and not isnan(b) else 0
                     for a,b in zip(p1_values,p2_values)),2)


# Euclidienne similarity function
def sim_distanceEuclidienne(person1, person2):
    p1_values = [*(person1).values()]
    p2_values = [*(person2).values()]
    return round(sqrt(sum( (a-b)**2 if not isnan(a) and not isnan(b) else 0
                    for a,b in zip(p1_values,p2_values))),2)


# Pearson Coefficient
def sim_distancePearson(person1, person2):
    sum_xy = 0
    sum_x = 0
    sum_y = 0
    sum_x2 = 0
    sum_y2 = 0
    n = 0
    for key in person1:
        if not isnan(person1[key]) and not isnan(person2[key]):
            n += 1
            x = person1[key]
            y = person2[key]
            sum_xy += x * y
            sum_x += x
            sum_y += y
            sum_x2 += x ** 2
            sum_y2 += y ** 2
    denominator = sqrt(sum_x2 - (sum_x ** 2) / n) * sqrt(sum_y2 - (sum_y ** 2) / n)
    if denominator == 0:
        return 0
    else:
        return (sum_xy - (sum_x * sum_y) / n) / denominator


# Cosine Coefficient
def sim_distanceCosine(person1, person2):
    sum_xy = 0
    sum_x2 = 0
    sum_y2 = 0
    for key in person1:
        if not isnan(person1[key]) and not isnan(person2[key]):
            x = person1[key]
            y = person2[key]
            sum_xy += x * y
            sum_x2 += x ** 2
            sum_y2 += y ** 2
    denominator = sqrt(sum_x2) * sqrt(sum_y2)
    if denominator == 0:
        return 0
    else:
        return (sum_xy) / denominator


class Rating:

    def __init__(self,target,choice):
        self.critiques = {}
        self.movies = []
        self.client = target
        self.movies_not_watched = []
        self.choice = choice

    def setup(self):
        # reading choice for example 1, 2, 3, 4 
        if self.choice == "Movie1":
            file_path = PATH + "\\movies_rating.csv"
        elif self.choice == "Music":
            file_path = PATH + "\\music.csv"
        elif self.choice == "Movie3":
            file_path = PATH + "\\movies3.csv"
        elif self.choice == "Movie4":
            file_path = PATH + "\\movies4.csv"
       
        movies_df = pd.read_csv(file_path)
        cols = movies_df.columns

        #assiging critiques
        self.critiques = {row[0]:{
                cols[i]:row[i] for i in range(1,len(cols))
            } for row in (movies_df.values)}
        # assigning movies
        self.movies = [cols[i] for i in range(1,len(cols))]

        #identifying the movies not watched by the given victim
        self.movies_not_watched = [i for i in self.movies
                           if isnan((self.critiques[self.client])[i]) ]
        print("Items not watched are = ", self.movies_not_watched)

    def recommendNearestNeighbor(self,nouveauCritique):
        recommended_movies = []
        distance = self.computeNearestNeighbor(nouveauCritique)
        dist,neighbour = distance[0]

        neighbour_list = self.critiques[neighbour]
        critique_list = self.critiques[nouveauCritique]
        recommended_movies = [(movie,neighbour_list[movie]) for movie in self.movies
                       if isnan(critique_list[movie]) and
                       not isnan(neighbour_list[movie]) ]
        print("Recommendation as per {0} measure are *{1}*".format("Nearest Neighbour",recommended_movies))


    def computeNearestNeighbor(self,target):
        distances = []
        critique_names = [*(self.critiques).keys()]
        for critique in critique_names:
            if critique == target:
                continue
            else:
                distance = sim_distanceManhattan(self.critiques[critique],
                                                 self.critiques[target])
                distances.append((distance,critique))
                distances.sort()
        return distances

    def Bestrecommend(self,dist_function):
        recommend_movie = ''
        high_score = 0
        for movie in self.movies_not_watched:
            total = 0.0
            sa = 0.0
            for critique_name,values in self.critiques.items():
                sim_dist = 0.0
                if critique_name!=self.client:
                    num = (values[movie])
                    if dist_function == "Manhattan":
                        sim_dist = sim_distanceManhattan(self.critiques[self.client],
                        self.critiques[critique_name])
                    elif dist_function == "Euclidean":
                        sim_dist = sim_distanceEuclidienne(self.critiques[self.client],
                        self.critiques[critique_name])
                    total += (num / (1 + sim_dist))
                    sa += (1 / (1 + sim_dist))
            s_dash = total/sa
            if high_score < (s_dash):
                high_score= s_dash
                recommend_movie = movie
        print("Recommendation as per {0} measure is *{1}*".format(dist_function,recommend_movie))


    def BestrecommendwithExp(self,dist_function):
        recommend_movie = ''
        high_score = 0
        for movie in self.movies_not_watched:
            total = 0.0
            s = 0.0
            for critique_name,values in self.critiques.items():
                sim_dist = 0.0
                if critique_name!=self.client:
                    num = (values[movie])
                    if dist_function == "Manhattan":
                        sim_dist = sim_distanceManhattan(
                                    self.critiques[self.client],
                                    self.critiques[critique_name]
                                 )
                    elif dist_function == "Euclidean":
                        sim_dist = sim_distanceEuclidienne(
                            self.critiques[self.client],
                            self.critiques[critique_name]
                        )
                    total += (num / exp(-1*sim_dist))
                    s += (1 / (exp(-1*sim_dist)))
            s_dash = total/s
            if high_score < (s_dash):
                high_score= s_dash
                recommend_movie = movie
        print("Recommendation as per exponential {0} measure is *{1}*".format(dist_function,recommend_movie))

    def PearsonRecommend(self):
        recommend_movie = ''
        high_score = 0
        for movie in self.movies_not_watched:
            total = 0.0
            s = 0.0
            for critique_name,values in self.critiques.items():
                sim_dist = 0.0
                if critique_name != self.client:
                    sim_dist = sim_distancePearson(self.critiques[self.client],
                                                 self.critiques[critique_name])
                    s += (1 + sim_dist)
                    total += (values[movie] * (1 + sim_dist))
            s_dash = total/s
            if high_score < (s_dash):
                high_score= s_dash
                recommend_movie = movie
        print("Recommendation as per {0} measure is *{1}*".format("Pearson",recommend_movie))

    def CosineRecommend(self):
        recommend_movie = ''
        high_score = 0
        for movie in self.movies_not_watched:
            total = 0.0
            s = 0.0
            for critique_name,values in self.critiques.items():
                sim_dist = 0.0
                if critique_name != self.client:
                    sim_dist = sim_distanceCosine(self.critiques[self.client],
                                                 self.critiques[critique_name])
                    s += (1 + sim_dist)
                    total += (values[movie] * (1 + sim_dist))
            s_dash = total/s
            if high_score < (s_dash):
                high_score= s_dash
                recommend_movie = movie
        print("Recommendation as per {0} measure is *{1}*".format("Cosine",recommend_movie))



if __name__ == "__main__":
    print("\n\nExample 1--Movie Recommendations for Ms.Anne")
    df = Rating("Anne","Movie1")
    df.setup()
    df.recommendNearestNeighbor("Anne")
    df.Bestrecommend("Manhattan")
    df.BestrecommendwithExp("Euclidean")
    df.PearsonRecommend()
    df.CosineRecommend()

    print("\n\nQuestion 3--Music Recommendations for Ms.Veronica")
    df2 = Rating("Veronica", "Music")
    df2.setup()
    df2.recommendNearestNeighbor("Veronica")
    df2.Bestrecommend("Manhattan")
    df2.Bestrecommend("Euclidean")
    df2.BestrecommendwithExp("Manhattan")
    df2.BestrecommendwithExp("Euclidean")
    df2.PearsonRecommend()
    df2.CosineRecommend()
    
    print("\n\nQuestion 3--Music Recommendations for Ms.Hailey")
    df2 = Rating("Hailey", "Music")
    df2.setup()
    df2.recommendNearestNeighbor("Hailey")
    df2.Bestrecommend("Manhattan")
    df2.Bestrecommend("Euclidean")
    df2.BestrecommendwithExp("Manhattan")
    df2.BestrecommendwithExp("Euclidean")
    df2.PearsonRecommend()
    df2.CosineRecommend()
    
    print("\n\nQuestion 3--Different Recommendations as compared to Pearson/ Cosine for a critic, Ms.Anne")
    df3 = Rating("Anne", "Movie3")
    df3.setup()
    #df3.recommendNearestNeighbor("Anne")
    df3.Bestrecommend("Manhattan")
    #df3.Bestrecommend("Euclidean")
    #df3.BestrecommendwithExp("Manhattan")
    df3.BestrecommendwithExp("Euclidean")
    df3.PearsonRecommend()
    #df3.CosineRecommend()
    
    print("\n\nQuestion 4-- Different Recommendations for a critic, Mr.Anant")
    df4 = Rating("Anant", "Movie4")
    df4.setup()
    
    df4.Bestrecommend("Manhattan")
    df4.Bestrecommend("Euclidean")
    df4.BestrecommendwithExp("Manhattan")
    #df4.BestrecommendwithExp("Euclidean")
   # df4.PearsonRecommend()
    df4.CosineRecommend()