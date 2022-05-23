import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df=pd.read_csv('fandango_scrape.csv')
print(df.head(),"\n", df.info(),"\n", df.describe())
plt.figure(figsize=(12,6))
#sns.scatterplot(data=df, x=df['RATING'], y=df['VOTES']) #exploring a relationship between popularity and film rating
print(df[['STARS','RATING','VOTES']].corr()) #correlation between stars, rating and votes
df['YEAR']=df['FILM'].apply(lambda title: title.split('(')[-1])
print(df['YEAR'].value_counts())
#sns.countplot(data=df, x='YEAR')
print(df.nlargest(10, 'VOTES'))
df2=df[df['VOTES']>0]
print(df2.nsmallest(10,'VOTES'))
#plt.figure(figsize=(8,4),dpi=150)
#sns.kdeplot(data=df2,x='STARS',clip=[0,5],fill=True,label='Stars Displayed')
df2['STARS_DIFF']=df2['STARS']-df2['RATING']
df2['STARS_DIFF']=df2['STARS_DIFF'].round(2)
#sns.countplot(data=df2,x='STARS_DIFF')
print(df2[df2['STARS_DIFF']>=1])
#PART THREE: COMPARISON OF FANDANGO RATINGS TO OTHER SITES
all_sites = pd.read_csv("all_sites_scores.csv")
print(all_sites.head(),all_sites.info(),all_sites.describe())
#sns.scatterplot(data=all_sites, x=all_sites['RottenTomatoes'])
all_sites['ROTTEN_DIFF']=all_sites['RottenTomatoes']-all_sites['RottenTomatoes_User']
print(all_sites['ROTTEN_DIFF'].abs().mean())
#sns.histplot(data=all_sites,x='ROTTEN_DIFF', kde=True, bins=25)
#plt.title('Rotten Tomatos Critis Score - Rotten Tomatos User Score')
#sns.histplot(data=all_sites,x=all_sites['ROTTEN_DIFF'].abs(), kde=True, bins=25)
#plt.title('Abs Difference Rotten Tomatos Critis Score - Rotten Tomatos User Score')
print(all_sites.nsmallest(5,'ROTTEN_DIFF'))
print(all_sites.nlargest(5,'ROTTEN_DIFF'))
#sns.scatterplot(data=all_sites,x=all_sites['Metacritic'],y=all_sites['Metacritic_User'])
#sns.scatterplot(data=all_sites,x=all_sites['Metacritic_user_vote_count'],y=all_sites['IMDB_user_vote_count'])
print(all_sites.nlargest(1,'IMDB_user_vote_count'))
print(all_sites.nlargest(1,'Metacritic_user_vote_count'))
merged=pd.merge(df,all_sites,on='FILM',how='inner')
merged.info()
print(merged.head())
merged['RT_norm']=np.round(merged['RottenTomatoes']/20,1)
merged['RT_user_norm']=np.round(merged['RottenTomatoes_User']/20,1)
merged['META_norm']=np.round(merged['Metacritic']/20,1)
merged['META_user_norm']=np.round(merged['Metacritic_User']/2,1)
merged['IMDB_norm']=np.round(merged['IMDB']/2,1)

norm_scores=merged[['STARS','RATING','RT_norm','RT_user_norm','META_norm','META_user_norm','IMDB_norm']]
print(norm_scores.head())

def move_legend(ax, new_loc, **kws):
    old_legend = ax.legend_
    handles = old_legend.legendHandles
    labels = [t.get_text() for t in old_legend.get_texts()]
    title = old_legend.get_title().get_text()
    ax.legend(handles, labels, loc=new_loc, title=title, **kws)

#fig, ax = plt.subplots(figsize=(15,6),dpi=150)
#sns.kdeplot(data=norm_scores,clip=[0,5],shade=True,palette='Set1',ax=ax)
#move_legend(ax, "upper left")
#fig, ax = plt.subplots(figsize=(15,6),dpi=150)
#sns.kdeplot(data=norm_scores[['RT_norm','STARS']],clip=[0,5],shade=True,palette='Set1',ax=ax)
#move_legend(ax, "upper left")
#sns.clustermap(norm_scores,cmap='magma',col_cluster=False)
norm_films=merged[['STARS','RATING','RT_norm','RT_user_norm','META_norm','META_user_norm','IMDB_norm','FILM']]
print(norm_films.nsmallest(10,'RT_norm'))
plt.figure(figsize=(15,6),dpi=150)
worst_films = norm_films.nsmallest(10,'RT_norm').drop('FILM',axis=1)
sns.kdeplot(data=worst_films,clip=[0,5],shade=True,palette='Set1')
plt.title("Ratings for RT Critic's 10 Worst Reviewed Films");
print(norm_films.iloc[25])