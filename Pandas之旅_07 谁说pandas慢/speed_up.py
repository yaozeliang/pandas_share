
# coding: utf-8

# ## Pandas 加速

# 大家好，今天我们来看pandas加速的相关小技巧，不知道大家在刚刚接触pandas的时候有没有听过如下的说法
# 
# >**pandas太慢了，运行要等半天。。。。
# 
# 其实我想说的是，慢不是pandas的错，大家要知道pandas本身是在Numpy上建立起来的包，在很多情况下是支持向量化运算的，而且还有C的底层设计，所以我今天
# 主要想从几个方面和大家分享一下pandas加速的小技巧，与往常一样，文章分成四部分，本文结构如下：
# 
# 
# 
# 1. 使用datetime类型来处理和时间序列有关的数据
# 2. 批量计算的技巧
# 3. 通过HDFStore存储数据节省时间
# 4. 源码，相关数据及GitHub地址
# 
# 
# 现在就让我们开始吧

# ## 1. 使用datetime类型来处理和时间序列有关的数据

# 首先这里我们使用的数据源是一个电力消耗情况的数据(energy_cost.csv)，非常贴近生活而且也是和时间息息相关的，用来做测试在合适不过了，这个csv文件大家可以在第四部分找到下载的地方哈

# In[1]:


import os
# 这两行仅仅是切换路径，方便我上传Github，大家不用理会,只要确认csv文件和py文件再一起就行啦
os.chdir("F:\\Python教程\\segmentfault\\pandas_share\\Pandas之旅_07 谁说pandas慢")


# 现在让我们看看数据大概长什么样子

# In[2]:


import numpy as np
import pandas as pd
f"Using {pd.__name__},{pd.__version__}"


# In[3]:


df = pd.read_csv('energy_cost.csv',sep=',')
df.head()


# 现在我们看到初始数据的样子了，主要有date_time和energy_kwh这两列，来表示时间和消耗的电力，比较好理解，下面让我们来看一下数据类型

# In[4]:


df.dtypes


# In[5]:


type(df.iat[0,0])


# 这里有个小问题，Pandas和NumPy有dtypes（数据类型）的概念。如果未指定参数，则date_time这一列的数据类型默认object，所以为了之后运算方便，我们可以把str类型的这一列转化为timestamp类型:

# In[6]:


df['date_time'] = pd.to_datetime(df['date_time'])
df.dtypes


# 先在大家可以发现我们通过用pd.to_datetime这个方法已经成功的把date_time这一列转化为了datetime64类型

# In[7]:


df.head()


# 现在再来看数据会发现已经和刚才不同了,我们还可以通过指定format参数实现一样的效果，一般速度上还会快一些

# In[8]:


get_ipython().run_cell_magic('timeit', '-n 10', "def convert_with_format(df, column_name):\n    return pd.to_datetime(df[column_name],format='%Y/%m/%d %H:%M')\n\ndf['date_time']=convert_with_format(df, 'date_time')")


# 有关具体的日期自定义相关方法，大家点击[这里](http://strftime.org/)查看

# ## 2. 批量计算的技巧

# 首先，我们假设根据用电的时间段不同，国家电力收费价目表如下：
# 
# | Type | cents/kwh | periode |
# | --- | --- | --- |
# | Peak | 28 | 17:00 to 24:00 |
# | Shoulder | 20 | 7:00 to 17:00 |
# | Off-Peak | 12 | 0:00 to 7:00 |

# 这里假设我们想要计算出电费，我们常用的一种不太便捷的方式如下：

# In[9]:


def apply_tariff(kwh, hour):
    """Calculates cost of electricity for given hour."""    
    if 0 <= hour < 7:
        rate = 12
    elif 7 <= hour < 17:
        rate = 20
    elif 17 <= hour < 24:
        rate = 28
    else:
        raise ValueError(f'Invalid hour: {hour}')
    return rate * kwh


# #### iterrows()

# 首先我们能做的是循环遍历流程，让我们先用.iterrows()替代上面的方法来试试：

# In[10]:


get_ipython().run_cell_magic('timeit', '-n 10', "def apply_tariff_iterrows(df):\n    energy_cost_list = []\n    for index, row in df.iterrows():\n        # Get electricity used and hour of day\n        energy_used = row['energy_kwh']\n        hour = row['date_time'].hour\n        # Append cost list\n        energy_cost = apply_tariff(energy_used, hour)\n        energy_cost_list.append(energy_cost)\n    df['cost_cents'] = energy_cost_list\n\napply_tariff_iterrows(df)")


# 这里我们有很大的改进空间，下面我们用apply方法来进一步优化

# #### apply()

# In[11]:


get_ipython().run_cell_magic('timeit', '-n 10', "def apply_tariff_withapply(df):\n    df['cost_cents'] = df.apply(\n        lambda row: apply_tariff(\n            kwh=row['energy_kwh'],\n            hour=row['date_time'].hour),\n        axis=1)\n\napply_tariff_withapply(df)")


# 这回速度得到了很大的提升,但是我们依然可以更近一步，采用矢量化操作来提速

# #### isin()

# 假设我们现在的电价是定值，pandas中最快的方法那就是采用(df['energy_kwh'] * price)，这就是矢量化操作的一个例子，
# 它是在Pandas中运行最快的方式。但是如何将条件判断添加到Pandas中的矢量化运算中？这里的技巧就是我们根据条件选择和分组DataFrame，然后对每个选定的组应用矢量化操作:

# In[12]:


df.set_index('date_time', inplace=True)


# In[13]:


get_ipython().run_cell_magic('timeit', '-n 10', "def apply_tariff_isin(df):\n    # Define hour range Boolean arrays\n    peak_hours = df.index.hour.isin(range(17, 24))\n    shoulder_hours = df.index.hour.isin(range(7, 17))\n    off_peak_hours = df.index.hour.isin(range(0, 7))\n\n    # Apply tariffs to hour ranges\n    df.loc[peak_hours, 'cost_cents'] = df.loc[peak_hours, 'energy_kwh'] * 28\n    df.loc[shoulder_hours,'cost_cents'] = df.loc[shoulder_hours, 'energy_kwh'] * 20\n    df.loc[off_peak_hours,'cost_cents'] = df.loc[off_peak_hours, 'energy_kwh'] * 12\n\napply_tariff_isin(df)")


# 这回我们发现速度是真正起飞了，首先我们根据用电的三个时段把df进行分组，再依次进行三次矢量化操作，大家可以发现最后减少了很多运行时间，在运行的时候，.isin（）方法返回一个布尔值数组，如下所示：
# - [False, False, False, ..., True, True, True]
# 
# 
# 接下来布尔数组传递给DataFrame的.loc索引器时，我们获得一个仅包含与3个用电时段匹配DataFrame切片。然后简单的进行乘法操作就行了，这样做的好处是我们已经不需要刚才提过的apply方法了，因为不在存在遍历所有行的问题

# #### 我们可以做的更好吗？

# 通过观察可以发现，在apply_tariff_isin（）中，我们仍然在通过调用df.loc和df.index.hour.isin（）来进行一些“手动工作”。如果要做的更好,
# 我们可以使用cut方法

# In[14]:


get_ipython().run_cell_magic('timeit', '-n 10', "def apply_tariff_cut(df):\n    cents_per_kwh = pd.cut(x=df.index.hour,\n                           bins=[0, 7, 17, 24],\n                           include_lowest=True,\n                           labels=[12, 20, 28]).astype(int)\n    df['cost_cents'] = cents_per_kwh * df['energy_kwh']")


# #### 不要忘了用Numpy

# 毕竟Pandas是在Numpy上建立起来的，所以在Numpy中有类似cut的方法可以实现分组,从速度上来讲差不太多

# In[26]:


get_ipython().run_cell_magic('timeit', '-n 10', "def apply_tariff_digitize(df):\n    prices = np.array([12, 20, 28])\n    bins = np.digitize(df.index.hour.values, bins=[7, 17, 24])\n    df['cost_cents'] = prices[bins] * df['energy_kwh'].values")


# In[ ]:


正常情况下，以上的加速方法是能满足日常需要的，如果有特殊的需求，大家可以上网看看有没有相关的第三方加速包


# ## 3. 通过HDFStore存储数据节省时间

# 这里主要想说的主要是节省预处理的时间，假设我们辛辛苦苦搭建了一些模型，但是每次运行之前都要进行一些预处理，比如类型转换，用时间序列做索引等，如果不用HDFStore的话每次都会花去不少时间，这里Python提供了一种解决方案，可以把经过预处理的数据存储为HDF5格式，方便我们下次运行时直接调用。
# 
# 下面就让我们把本篇文章的df通过HDF5来存储一下：
# 

# In[27]:


# Create storage object with filename `processed_data`
data_store = pd.HDFStore('processed_data.h5')

# Put DataFrame into the object setting the key as 'preprocessed_df'
data_store['preprocessed_df'] = df
data_store.close()


# 现在我们可以关机下班了，当明天接着上班后，通过key（"preprocessed_df"）就可以直接使用经过预处理的数据了

# In[28]:


# Access data store
data_store = pd.HDFStore('processed_data.h5')

# Retrieve data using key
preprocessed_df = data_store['preprocessed_df']
data_store.close()


# In[30]:


preprocessed_df.head()


# In[ ]:


如上图所示，现在我们可以发现date_time已经是处理为index了


# ## 4. 源码，相关数据及GitHub地址

# 这一期为大家分享了一些pandas加速的实用技巧，希望可以帮到各位小伙伴，当然，类似的技巧还有很多，但是核心思想应该一直围绕矢量化操作上，毕竟是基于Numpy上建立的包，如果大家有更好的办法，希望可以在我的文章底下留言哈
# 
# 我把这一期的ipynb文件，py文件以及我们用到的energy_cost.csv放到了Github上，大家可以点击下面的链接来下载：
#  - Github仓库地址： [https://github.com/yaozeliang/pandas_share](https://github.com/yaozeliang/pandas_share/tree/master/Pandas%E4%B9%8B%E6%97%85_04%20pandas%E8%B6%85%E5%AE%9E%E7%94%A8%E6%8A%80%E5%B7%A7)
# 
# 希望大家能够继续支持我，完结，撒花
