from math import sqrt
import json

def pearson_collab(dataset,user):
        def pearson(p1,p2):
                bothrated={}
                for item in dataset[p1]:
                        if item in dataset[p2]:
                                bothrated[item]=1
                #print(bothrated)	
                rating_num=len(bothrated)		
                if rating_num==0:
                        return 0
                p1sum=sum([dataset[p1][item] for item in bothrated])
                p2sum=sum([dataset[p2][item] for item in bothrated])
                p1sqsum=sum([pow(dataset[p1][item],2) for item in bothrated])
                p2sqsum=sum([pow(dataset[p2][item],2) for item in bothrated])
                prod=sum([dataset[p1][item] * dataset[p2][item] for item in bothrated])
                x=prod-(p1sum*p2sum/rating_num)
                y=sqrt((p1sqsum-pow(p1sum,2)/rating_num)*(p2sqsum-pow(p2sum,2)/rating_num))
                
                if y == 0:
                        return 0
                else :
                        r =x/y
                        return r
        

        def Rec(person):

                
                totals = {}
                simSums = {}
                rankings_list =[]
                for other in dataset:
                        
                        if other == person:
                                continue
                        sim = pearson(person,other)
                        

                        
                        if sim <=0: 
                                continue
                        for item in dataset[other]:

                                
                                if item not in dataset[person] or dataset[person][item] == 0:

                                
                                        totals.setdefault(item,0)
                                        totals[item] += dataset[other][item]* sim
                                        # sum of similarities
                                        simSums.setdefault(item,0)
                                        simSums[item]+= sim

                        

                rankings = [(total/simSums[item],item) for item,total in totals.items()]
                rankings.sort()
                rankings.reverse()
                
                rec_list = [recommend_item for score,recommend_item in rankings]
                return rec_list

        var = Rec(user)
        return var[0]
