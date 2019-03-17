
# coding: utf-8

# ## Merge,Join, Concat,Sort

# 大家好，我有回来啦，这周更新的有点慢，主要是因为我更新了个人简历哈哈，如果感兴趣的朋友可以去看看哈
#  [我的主页](www.yaozeliang.com/resume/)，个人认为还是很漂亮的~，不得不说很多时候老外的设计能力还是很强。
#  
#  好了，有点扯远了，这一期我想和大家分享的是pandas中最常见的几种方法，这些方法如果你学会了，某种程度上可以很好的替代Excel，这篇文章是pandas之旅的第三篇，主要会从以下几个方面和大家分享我的心得体会：
#  
# 1. Merge
# 2. Join
# 3. Concat
# 4. 源码及GitHub地址
# 
# 话不多说，让我们开始今天的Pandas之旅吧！
#  

# ## 1. Merge
# 
# 首先merge的操作非常类似sql里面的join，实现将两个Dataframe根据一些共有的列连接起来，当然，在实际场景中，这些共有列一般是Id，
# 连接方式也丰富多样，可以选择inner(默认)，left,right,outer 这几种模式，分别对应的是内连接，左连接，右连接
# 

# ### 1.1 InnerMerge (内连接)
首先让我们简单的创建两个DF,分别为DataFrame1,DataFrame2,他们的公有列是key
# In[2]:


import numpy as np
import pandas as pd
from pandas import Series, DataFrame


# In[17]:


# Let's make a dframe
dframe1 = DataFrame({'key':['X','Z','Y','Z','X','X'],'value_df1': np.arange(6)})
dframe1


# In[18]:


#Now lets make another dframe
dframe2 = DataFrame({'key':['Q','Y','Z'],'value_df2':[1,2,3]})
dframe2

我们现在可以简单地使用pd.merge(dframe1,dframe2)来实现Merge功能
# In[19]:


pd.merge(dframe1,dframe2)

我们现在需要注意一点，X仅仅是存在于dframe1的key，在dframe2中不存在，因此大家可以发现，当我们调用pd.merge的时候，会自动默认为inner join，
我们再换一种方式写一下，大家就明白了：

# In[26]:


pd.merge(dframe1,dframe2,on='key',how='inner')


# In[ ]:


大家可以发现结果是一样的，看到这里，对sql熟悉的朋友们已经有感觉了估计，因为实在是太像了，如果我们不通过on和how来指定
想要merge的公有列或者方式，那么pd.merge就会自动寻找到两个DataFrame的相同列并自动默认为inner join，至此，
估计大家也可以猜出其他几种模式的merge啦


# ### 1.2 LeftMerge (左连接)

# In[ ]:


现在同样的，让我们看一下how='left'的情况，这是一个左连接


# In[27]:


pd.merge(dframe1,dframe2,on='key',how='left')

我们可以看到返回的是dframe1的所有key值对应的结果，如果在dframe2中不存在，显示为Nan空值
# ### 1.3 RightMerge (右连接)
右连接的原理和左连接正相反
# In[28]:


pd.merge(dframe1,dframe2,on='key',how='right')

这里Q只存在于drame2的key中
# ### 1.4 OuterMerge (全连接)

# In[30]:


#Choosing the "outer" method selects the union of both keys
pd.merge(dframe1,dframe2,on='key',how='outer')


# In[ ]:


这里就是一个并集的形式啦，其实就是一个union的结果，会把key这一列在两个Dataframe出现的所有值全部显示出来，如果有空值显示为Nan


# ### 1.5 MultipleKey Merge (基于多个key上的merge)

# 刚才我们都是仅仅实现的在一个key上的merge，当然我们也可以实现基于多个keys的merge

# In[34]:


# Dframe on left
df_left = DataFrame({'key1': ['SF', 'SF', 'LA'],
                  'key2': ['one', 'two', 'one'],
                  'left_data': [10,20,30]})
df_left


# In[35]:


#Dframe on right
df_right = DataFrame({'key1': ['SF', 'SF', 'LA', 'LA'],
                   'key2': ['one', 'one', 'one', 'two'],
                   'right_data': [40,50,60,70]})
df_right


# In[ ]:


这是内连接（交集）的结果


# In[38]:


#Merge， Inner
pd.merge(df_left, df_right, on=['key1', 'key2'])


# In[ ]:


这是外连接（并集）的结果


# In[39]:


#Merge， Outer
pd.merge(df_left, df_right, on=['key1', 'key2'],how='outer')

这里还有一个地方非常有意思，大家可以发现现在df_left,df_right作为key的两列分别是key1和key2，它们的名字是相同的，刚刚我们是通过制定on=['key1', 'key2'],那如果我们只指定一列会怎么样呢？
# In[40]:


pd.merge(df_left,df_right,on='key1')

大家可以看到pandas自动把key2这一列拆分成了key2_x和key2_y，都会显示在最后的merge结果里，如果我们想要给这两列重新命名，也是很容易的：
# In[41]:


# We can also specify what the suffix becomes
pd.merge(df_left,df_right, on='key1',suffixes=('_lefty','_righty'))

像这样，我们可以通过suffixes参数来指定拆分的列的名字。

# ### 1.6 Merge on Index (基于index上的merge)

# In[ ]:


我们还可以实现几个Dataframe基于Index的merge，还是老样子，先让我们创建两个Dataframe


# In[43]:


df_left = DataFrame({'key': ['X','Y','Z','X','Y'],
                  'data': range(5)})
df_right = DataFrame({'group_data': [10, 20]}, index=['X', 'Y'])


# In[44]:


df_left


# In[45]:


df_right

好了，现在我们想要实现两个Dataframe的merge，但是条件是通过df_left的Key和df_right的Index
# In[47]:


pd.merge(df_left,df_right,left_on='key',right_index=True)

这样我们也可以得到结果。
# In[48]:


# We can also get a union by using outer
pd.merge(df_left,df_right,left_on='key',right_index=True,how='outer')

其他的merge方式就类似啦，这里就不一一说了，只是举一个outer join的例子
# In[49]:


# 通过outer实现外连接，union并集
pd.merge(df_left,df_right,left_on='key',right_index=True,how='outer')


# In[ ]:


我们也可以尝试一些有意思的merge，比如，如果一个dataframe的index是多层嵌套的情况：


# In[50]:


df_left_hr = DataFrame({'key1': ['SF','SF','SF','LA','LA'],
                   'key2': [10, 20, 30, 20, 30],
                   'data_set': np.arange(5.)})
df_right_hr = DataFrame(np.arange(10).reshape((5, 2)),
                   index=[['LA','LA','SF','SF','SF'],
                          [20, 10, 10, 10, 20]],
                   columns=['col_1', 'col_2'])


# In[51]:


df_left_hr


# In[52]:


df_right_hr

现在我们穿建了两个Dataframe 分别是df_left_hr和df_right_hr（Index两层），如果我们想通过使用df_left_hr的key1，key2 及df_right_hr的Index作为merge
的列，也是没有问题的
# In[53]:


# Now we can merge the left by using keys and the right by its index
pd.merge(df_left_hr,df_right_hr,left_on=['key1','key2'],right_index=True)

基本到这里，我已经和大家分享了基础的Merge有关的所有操作，如果你平时生活工作中经常使用Excel执行类似操作的话，可以学习一下Merge哈，它会大幅度
减轻你的工作强度的！
# ## 2.Join
现在我们可以接着来看join相关的操作，先让我们看一个小例子
# In[55]:


left = pd.DataFrame({'A': ['A0', 'A1', 'A2', 'A3'], 
                    'B': ['B0', 'B1', 'B2', 'B3']}, 
                    index = ['K0', 'K1', 'K2', 'K3']) 
  
right = pd.DataFrame({'C': ['C0', 'C1', 'C2', 'C3'], 
                      'D': ['D0', 'D1', 'D2', 'D3']}, 
                      index = ['K0', 'K1', 'K2', 'K3']) 


# In[57]:


left


# In[58]:


right


# In[59]:


left.join(right)

其实通过这一个小例子大家也就明白了，join无非就是合并，默认是横向，还有一个点需要注意的是，我们其实可以通过join实现和merge一样的效果，但是为了
避免混淆，我不会多举其他的例子了，因为我个人认为一般情况下还是用merge函数好一些
# ## 3. Concat
为了更加全面彻底地了解Concat函数，大家可以先从一维的Numpy Array开始，首先让我们简单的创建一个矩阵：
# In[60]:


# Create a matrix 
arr1 = np.arange(9).reshape((3,3))
arr1


# In[ ]:


接着让我们通过concatenate函数进行横向拼接：


# In[61]:


np.concatenate([arr1,arr1],axis=1)

再让我们进行纵向拼接：
# In[62]:


# Let's see other axis options
np.concatenate([arr1,arr1],axis=0)

有了基础的印象之后，现在让我们看看在pandas中是如何操作的：
# In[63]:


# Lets create two Series with no overlap
ser1 =  Series([0,1,2],index=['T','U','V'])

ser2 = Series([3,4],index=['X','Y'])

#Now let use concat (default is axis=0)
pd.concat([ser1,ser2])

在上面的例子中，我们分别创建了两个没有重复Index的Series,然后用concat默认的把它们合并在一起，这时生成的依然是Series类型，如果我们把axis换成1，那生成的就是Dataframe,像下面一样
# In[65]:


pd.concat([ser1,ser2],axis=1,sort =True)  # sort=Ture是默认的，pandas总是默认index排序

我们还可以指定在哪些index上进行concat:
# In[66]:


pd.concat([ser1,ser2],axis=1,join_axes=[['U','V','Y']])

也可以给不同组的index加一层标签
# In[67]:


pd.concat([ser1,ser2],keys=['cat1','cat2'])

如果把axis换成是1，那么keys就会变成column的名字：
# In[69]:


pd.concat([ser1,ser2],axis=1,keys=['cat1','cat2'],sort=True)

如果是两个现成的dataframe直接进行concat也是一样：
# In[70]:


dframe1 = DataFrame(np.random.randn(4,3), columns=['X', 'Y', 'Z'])
dframe2 = DataFrame(np.random.randn(3, 3), columns=['Y', 'Q', 'X'])


# In[71]:


dframe1


# In[72]:


dframe2


# In[74]:


#如果没有对应的值，默认为NaN, 空值
pd.concat([dframe1,dframe2],sort=True)


# ## 4. 源码及Github地址

# 今天我为大家主要总结了pandas中非常常见的三种方法：
#  - merge
#  - concat
#  - join
# 
# 大家可以根据自己的实际需要来决定使用哪一种

# 我把这一期的ipynb文件和py文件放到了Github上，大家如果想要下载可以点击下面的链接：
#  - Github仓库地址： [https://github.com/yaozeliang/pandas_share](https://github.com/yaozeliang/pandas_share)
# 
# 
# 这一期就到这里啦，希望大家能够继续支持我，完结，撒花
