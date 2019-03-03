
# coding: utf-8

# In[58]:


# import numpy as np
import pandas as pd
print (f" Using {pd.__name__},Version {pd.__version__}")


# ## 创建空Dataframe

# In[59]:


df = pd.DataFrame() 
print(df)


# ## 从Dict创建Dataframe(1)

# In[60]:


dict = {'name':["Tom", "Bob", "Mary", "James"], 
        'age': [18, 30, 25, 40], 
        'city':["Beijing", "ShangHai","GuangZhou", "ShenZhen"]} 
  
df = pd.DataFrame(dict) 
df


# ## 从Dict创建Dataframe(2)

# In[61]:


index = pd.Index(["Tom", "Bob", "Mary", "James"],name = 'person')
cols = ['age','city']
data = [[18,'Beijing'],
        [30,'ShangHai'],
        [25,'GuangZhou'],
        [40,'ShenZhen']]

df =pd.DataFrame(index = index,data =data,columns = cols)
df


# ## 对columns的基础操作 ##

# ### add column

# In[62]:


# 还用刚刚的dataframe
dict = {'name':["Tom", "Bob", "Mary", "James"], 
        'age': [18, 30, 25, 40], 
        'city':["Beijing", "ShangHai","GuangZhou", "ShenZhen"]} 
  
df = pd.DataFrame(dict) 
df


# In[63]:


df['country'] = 'USA'
df


# In[64]:


df['adress'] = df['country']
df


# ### Change column values
# 

# In[65]:


df['country'] = 'China'
df


# In[66]:


df['adress'] = df['city']+','+ df['country']
df


# ### Delete columns
# 

# In[67]:


df.drop('country',axis=1, inplace=True)
del df['city']
df


# ### Select columns
# 

# In[68]:


df['age']


# In[69]:


df.name


# In[70]:


df[['age','name']]  # This is a dataframe, Not a Serie


# In[71]:


df.columns


# ### Rename columns

# In[72]:


# df.columns = ['Age','Name','Adress']
# df


# In[73]:


df.rename(index = str, columns = {'age':'Age','name':'Name','adress':'Adress'},inplace=True)
df


# In[74]:


df.rename(str.lower, axis='columns',inplace =True)
df


# In[75]:


df.rename(str.capitalize, axis='columns',inplace =True)
df


# ### Set column value with conditions
# 

# In[76]:


df['Group'] = 'elderly'
df.loc[df['Age']<=18, 'Group'] = 'young'
df.loc[(df['Age'] >18) & (df['Age'] <= 30), 'Group'] = 'middle_aged'
df


# ## 对rows的基础操作 ##

# ### loc函数查询

# In[78]:


df


# In[81]:


df.loc[:]


# ### loc函数条件查询

# In[82]:


df.loc[df['Age']>20]


# ### loc函数条件行列查询

# In[86]:


df.loc[df['Group']=='middle_aged','Name']


# ### Where 查询

# In[92]:


filter_adult = df['Age']>25
result = df.where(filter_adult)
result


# ### Query 筛选

# In[99]:


df


# In[106]:


# df.query('Age==30') 
df.query('Group=="middle_aged"'and 'Age>30' )


# ### 了解Dataframe

# In[118]:


df.shape


# In[120]:


df.describe()


# In[123]:


df.head(3)
df.tail(3)


# ## 读取，写出CSV ##
# 

# ### 把df导出为CSV，不要index 

# In[112]:


df.to_csv('person.csv',index=None,sep=',')


# In[113]:


import os
os.getcwd()


# ### 读取CSV为dataframe

# In[116]:


person = pd.read_csv('person.csv')
person

