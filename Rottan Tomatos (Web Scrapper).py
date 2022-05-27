

# calling libraries

import bs4 as bs
import requests
import string
from operator import itemgetter
from wordcloud import WordCloud
import matplotlib.pyplot as plt

#####################################################################################################################
# clalling list of dicsnory for processing
f = []
link = []
# rivew list contain values that are pre defind according to rottan tommeto web site
rivew = ["/","r","e","v","i","e","w","s","?","t","y","p","e","=","&","s","o","r","t","=","&","p","a","g","e","=","2"]
final_link = []
page_no = []
j = []
final = []
#final1 = []
stopwords = []
b = []
final_riview = []
fl = []
ratings = []
final_ratings = []
dicsnory = {}
# grade and grade1 will use to convert alphabetical ratings into numarical 
grade = {'A+':5, 'A':4.8, 'A-': 4.6, 'B+':4.45, 'B':4.3, 'B-':4.1, 'C+':3.95, 'C':3.8, 'C-':3.6, 'D+':3.45, 'D':3.3, 'D-':3.1}
grade1 = ['A+', 'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'D+', 'D', 'D-']
final_dics = {}
word_cloud_hr = []
word_cloud_lr = []

############################################################################################################

# creating list of stopwords
file = open("A.txt")
for line in file:
    S = line.lower().strip("\n")
    stopwords.append(S)
stopwords.extend(["full","review","original","page"])     # extending the list of stope words

############################################################################################################
# the code for asking input link from user 
# code will break the link after fifth "/" and appand to link list for further use
print("#####################################################################################################")
print()
print(" Enter the Rotten Tomatoes link of the movie Which you want to find top 5 reviews of")
n = input()
print("######################################################################################################")

k = 0
for i in n:
    if i == "/":
        k = k + 1
        if k == 5:
            break
        else:
            link.append(i)
    else:
        link.append(i)

#############################################################################################################
# code for making the final link which will take proram tp direct on review
j = "".join(link + rivew)

#############################################################################################################
# code for finding total no of pages
body = requests.get(j)     
soup = bs.BeautifulSoup(body.text,"lxml")
                             # Below is the class you will reqeierd to read spacific information from web page 
for paragraph in soup.select(".pageInfo"): # ".pageinfo will take the number how many pages of review are there"
    f.append(paragraph.text)
    n = 0
    dummy = []
    for line in f:
        w = line.split()
        n = n + 1
        if n == 1:
            dummy.extend(w)
print()
print("The Movie have",dummy[-1],"Pages of reviews")
print()
print("####################################################################################################")
#############################################################################################################
# code for reading the reviews from site   
print("List of links of the web page visited")
print()          
w = 0
while True:     # whlie loop for scrowling all reviews pages
    w = w + 1
    if w > int(dummy[-1]) :  # for stoping condintion of while loop
        break
    else:
        rivew[-1] = str(w)
        fl = "".join(link + rivew)     # code for creating new links for every site
        
        print(fl)
        body = requests.get(fl)         # adding NYtimes URL
        soup = bs.BeautifulSoup(body.text,"lxml")
        for paragraph in soup.select(".review_desc"):
            f.append(paragraph.text)

        for line in f:
            A = line.strip().split()
            b.append(A)

        for i in b:
            #################################################################################
            # code will eliminate reviews without ratings
            if i[-1] == "Review":
                continue
              ###################################################################################             
              # code for converting rating into 5 
            elif "/" in i[-1]:
                if "/" in i[-1]:
                    dummy_1 = []
                    for word in i[-1]:
                        dummy_1.append(word)

                    # code will extract value before "/"
                    dummy_3 = []
                    for rat1 in dummy_1:
                        if rat1 == "/":
                            break
                        else:
                            dummy_3.append(rat1)
                            j_d = "".join(dummy_3)

                    # code will extract value after "/"        
                    h = 0
                    dummy_2 = []
                    for rat in dummy_1:
                        h = h + 1
                        if h > ((len(dummy_1)/2) + 0.5): 
                            if rat == "/":
                                continue
                            else:
                                dummy_2.append(rat)
                                j_d1 = "".join(dummy_2)
                    g = (5*float(j_d))/float(j_d1)       # equation for finging equivelant rating from 5
                    final_ratings.append(g)
                ##################################################################################
                # code that converts grades into ratings 
            elif i[-1] in grade1:
                b1 = i[-1]
                g = grade[b1]
                final_ratings.append(g)
                ##################################################################################
                # code for cleaning the panctuation and stopeword from reviews 
            l1 = []
            for i1 in i:
                c = i1.lower()
                table = str.maketrans("","", string.punctuation)
                word_f1 = c.translate(table)
                if word_f1 not in stopwords:                    
                    if word_f1.isdigit():
                        continue
                    elif word_f1.isalpha():
                        final.append(word_f1)
            for i1 in i: 
                c = i1.lower()          
                if c in final:
                    l1.append(c)
            if (" ".join(l1)) == "": # code for removining blanks from final reviews
                continue
            else:
                # code for addin values and keys to the final dicsnory         
                k = (" ".join(l1))      
                final_dics[k] = float(g)
    continue
#################################################################################################################
print()
print("#########################################################################################################")
print()
print("The code has succsessfully Identified",len(final_dics),"No of reviews with rating")
print()
print("#########################################################################################################")
#################################################################################################################
top_5 = sorted(dict(final_dics).items(),key=itemgetter(1),reverse=True)
word_cloud_h = dict(sorted(dict(final_dics).items(),key=itemgetter(1),reverse=True)[:4])
word_cloud_l = dict(sorted(dict(final_dics).items(),key=itemgetter(1),reverse=True)[-5:])
print()
print("list of top 5 reviews with hightest ratings")
print()
print("[1]",top_5[0])
print("[2]",top_5[1])
print("[3]",top_5[2])
print("[4]",top_5[3])
print("[5]",top_5[4])
print()
################################################################################################################
for line in word_cloud_h:
    p = line.split()
    for word in p:
        word_cloud_hr.append(word)

wc = WordCloud()
wc.generate(str(word_cloud_hr))
plt.imshow(wc,interpolation="bilinear")
plt.show()

print("##########################################################################################################")
print()
print("list of bottom 5 reviews with lowest ratings")
print()
print("[1]",top_5[-1])
print("[2]",top_5[-2])
print("[3]",top_5[-3])
print("[4]",top_5[-4])
print("[5]",top_5[-5])
##################################################################################################################
for line in word_cloud_l:
    p = line.split()
    for word in p:
        word_cloud_lr.append(word)

wc = WordCloud()
wc.generate(str(word_cloud_lr))
plt.imshow(wc,interpolation="bilinear")
plt.show()

print("Thank You")
print("##########################################################################################################")


