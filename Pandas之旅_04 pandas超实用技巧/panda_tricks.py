
# coding: utf-8

# ## Pandas不为人知的八大实用技巧

# 大家好，我今天勤快地回来了，这一期主要是和大家分享一些pandas的实用技巧，会在日常生活中大大提升效率，希望可以帮助到大家,还是老样子，
# 先给大家奉上这一期的章节目录:
# 
# 1. 自定义pandas选项，设置
# 2. 实用pandas中testing模块构建测试数据
# 3. 巧用accessor接口方法
# 4. 合并其他列拼接DatetimeIndex
# 5. 使用分类数据（Categorical Data）节省时间和空间
# 6. 利用Mapping巧妙实现映射
# 7. 压缩pandas对象
# 8. 源码及GitHub地址
# 
# 好啦，话不多说，让我们一个个看吧
# 

# ### 1. 自定义pandas选项，设置

# 首先，大家可能不知道，pandas里面有一个方法pd.set_option()，利用它我们可以改变一些pandas中默认的核心设置，
# 从而适应我们自身的需要，开始前还是老样子，让我们先导入numpy和pandas包

# In[1]:


import numpy as np
import pandas as pd
f'Using {pd.__name__}, Version {pd.__version__}'


# 现在让我们编写一个start方法来实现自定义pandas设置

# In[2]:


def start():
    options = {
        'display': {
            'max_columns': None,
            'max_colwidth': 25,
            'expand_frame_repr': False,  # Don't wrap to multiple pages
            'max_rows': 14,
            'max_seq_items': 50,         # Max length of printed sequence
            'precision': 4,
            'show_dimensions': False
        },
        'mode': {
            'chained_assignment': None   # Controls SettingWithCopyWarning
        }
    }

    for category, option in options.items():
        for op, value in option.items():
            pd.set_option(f'{category}.{op}', value)  # Python 3.6+

if __name__ == '__main__':
    start()
    del start  # Clean up namespace in the interpreter


# 大家可以发现，我们在方法的最后调用了pandas的set_option方法，直接利用我们自定义的参数替代了原有的pandas参数，现在让我们测试一下：

# In[3]:


pd.get_option('display.max_rows')


# 可以发现max_rows 已经被替换成了我们设置的14，现在用一个真实的例子，我们利用一组公开的鲍鱼各项指标的数据来实验，数据源来自机器学习平台的公开数据
# 

# In[4]:


url = ('https://archive.ics.uci.edu/ml/'
       'machine-learning-databases/abalone/abalone.data')
cols = ['sex', 'length', 'diam', 'height', 'weight', 'rings']
abalone = pd.read_csv(url, usecols=[0, 1, 2, 3, 4, 8], names=cols)
abalone


# 我们可以看到，数据截断为14行，保留了小数点后4位小数作为精度，和我们刚刚设置的precision=4是一样的

# ### 2. 实用pandas中testing模块构建测试数据

# 通过pandas.util.testing提供的方法，我们可以很容易的通过几行代码就构建出一个简单的测试数据类型，比如我们现在构建一个DataTime类型的数据，
# 时间间隔为月：

# In[5]:


import pandas.util.testing as tm
tm.N, tm.K = 15, 3         # 规定行和列

import numpy as np
np.random.seed(444)

tm.makeTimeDataFrame(freq='M').head() # 设置时间间隔为月
# tm.makeTimeDataFrame(freq='D').head()  设置时间间隔为天


# 瞎生成一组乱七八糟的数据：

# In[6]:


tm.makeDataFrame().head()


# 关于可以随机生成的数据类型, 一共大概有30多种，大家如果感兴趣可以多试试：

# In[7]:


[i for i in dir(tm) if i.startswith('make')]


# 这样我们如果有测试的需求，会很容易地构建相对应的假数据来测试。

# ### 3. 巧用accessor接口方法
# 

# accessor（访问器） 具体就是类似getter和setter，当然，Python里面不提倡存在setter和getter方法，但是这样可以便于大家理解，pandas Series类型有3类accessor：
# 

# In[8]:


pd.Series._accessors


# - .cat用于分类数据，
#  - .str用于字符串（对象）数据，
#  - .dt用于类似日期时间的数据。

# 让我们从.str开始看：假设现在我们有一些原始的城市/州/ 邮编数据作为Dataframe的一个字段：

# In[9]:


addr = pd.Series([
    'Washington, D.C. 20003',
    'Brooklyn, NY 11211-1755',
    'Omaha, NE 68154',
    'Pittsburgh, PA 15211'
])


# In[10]:


addr.str.upper()  # 因为字符串方法是矢量化的，这意味着它们在没有显式for循环的情况下对整个数组进行操作


# In[11]:


addr.str.count(r'\d')  # 查看邮编有几位


# 如果我们想把每一行分成城市，州，邮编分开，可以用正则；

# In[12]:


regex = (r'(?P<city>[A-Za-z ]+), '      # One or more letters
         r'(?P<state>[A-Z]{2}) '      # 2 capital letters
         r'(?P<zip>\d{5}(?:-\d{4})?)')  # Optional 4-digit extension

addr.str.replace('.', '').str.extract(regex)


# 第二个访问器.dt用于类似日期时间的数据。它其实属于Pandas的DatetimeIndex，如果在Series上调用，它首先转换为DatetimeIndex

# In[13]:


daterng = pd.Series(pd.date_range('2018', periods=9, freq='Q'))  # 时间间隔为季度
daterng


# In[14]:


daterng.dt.day_name()


# In[15]:


daterng[daterng.dt.quarter > 2]  # 查看2019年第3季度和第4季度


# In[16]:


daterng[daterng.dt.is_year_end]  #查看年末的一天


# 最后有关.cat访问器我们会在第5个技巧中提到

# ### 4. 合并其他列拼接DatetimeIndex

# 现在先让我们构建一个包含时间类型数据的Dataframe：

# In[17]:


from itertools import product
datecols = ['year', 'month', 'day']

df = pd.DataFrame(list(product([2017, 2016], [1, 2], [1, 2, 3])),
                  columns=datecols)
df['data'] = np.random.randn(len(df))
df


# 我们可以发现year，month，day是分开的三列，我们如果想要把它们合并为完整的时间并作为df的索引，可以这么做:

# In[18]:


df.index = pd.to_datetime(df[datecols])
df.head()


# 我们可以扔掉没用的列并把这个df压缩为Series：

# In[19]:


df = df.drop(datecols, axis=1).squeeze()
df.head()


# In[20]:


type(df)


# In[21]:


df.index.dtype_str


# ### 5. 使用分类数据（Categorical Data）节省时间和空间

# 刚刚我们在第3个技巧的时候提到了访问器，现在让我们来看最后一个.cat

# pandas中Categorical这个数据类型非常强大，通过类型转换可以让我们节省变量在内存占用的空间，提高运算速度，不过有关具体的pandas加速实战，我会在
# 下一期说，现在让我们来看一个小栗子：

# In[22]:


colors = pd.Series([
    'periwinkle',
    'mint green',
    'burnt orange',
    'periwinkle',
    'burnt orange',
    'rose',
    'rose',
    'mint green',
    'rose',
    'navy'
])

import sys
colors.apply(sys.getsizeof)


# 我们首先创建了一个Series，填充了各种颜色，接着查看了每个地址对应的颜色所占内存的大小
# >**注意这里我们使用sys.getsizeof()来获取占内存大小，但是实际上空格也是占内存的，sys.getsizeof('')返回的是49bytes**

# 接下来我们想把每种颜色用占内存更少的数字来表示（机器学习种非常常见），这样可以减少占用的内存，首先让我们创建一个mapper字典，给每一种颜色指定
# 一个数字

# In[23]:


mapper = {v: k for k, v in enumerate(colors.unique())}
mapper


# 接着我们把刚才的colors数组转化为int类型：

# In[24]:


# 也可以通过 pd.factorize(colors)[0] 实现
as_int = colors.map(mapper)
as_int


# 再让我们看一下占用的内存：

# In[25]:


as_int.apply(sys.getsizeof)


# 现在可以观察到我们的内存占用的空间几乎是之前的一半，其实，刚刚我们做的正是模拟Categorical Data的转化原理。现在让我们直接调用一下：

# In[26]:


colors.memory_usage(index=False, deep=True)


# In[27]:


colors.astype('category').memory_usage(index=False, deep=True)


# 大家可能感觉节省的空间并不是非常大对不对？ 因为目前我们这个数据根本不是真实场景，我们仅仅把数据容量增加10倍，现在再让我们看看效果：

# In[28]:


manycolors = colors.repeat(10)
len(manycolors) / manycolors.nunique()  # Much greater than 2.0x 


# In[29]:


f"Not using category : { manycolors.memory_usage(index=False, deep=True)}"


# In[30]:


f"Using category : { manycolors.astype('category').memory_usage(index=False, deep=True)}"


# 这回内存的占用量差距明显就出来了，现在让我们用.cat来简化一下刚刚的工作：

# In[31]:


new_colors = colors.astype('category')
new_colors


# In[32]:


new_colors.cat.categories   # 可以使用.cat.categories查看代表的颜色


# 现在让我们查看把颜色代表的数字：

# In[33]:


new_colors.cat.codes


# 我们如果不满意顺序也可以从新排序：

# In[34]:


new_colors.cat.reorder_categories(mapper).cat.codes


# 有关cat其他的方法，我们还是可以通过遍历dir来查看：

# In[35]:


[i for i in dir(new_colors.cat) if not i.startswith('_')]


# > Categorical 数据通常不太灵活，比如我们不能直接在new_colors上新增一个新的颜色，要首先通过
# .add_categories来添加

# In[36]:


ccolors.iloc[5] = 'a new color'


# In[ ]:


new_colors = new_colors.cat.add_categories(['a new color'])


# In[ ]:


new_colors.iloc[5] = 'a new color'  # 不会报错


# In[ ]:


new_colors.values  # 成功添加


# ### 6. 利用Mapping巧妙实现映射

# 假设现在我们有存贮国家的一组数据，和一组用来映射国家所对应的大洲的数据：

# In[ ]:


countries = pd.Series([
    'United States',
    'Canada',
    'Mexico',
    'Belgium',
    'United Kingdom',
    'Thailand'
])

groups = {
    'North America': ('United States', 'Canada', 'Mexico', 'Greenland'),
    'Europe': ('France', 'Germany', 'United Kingdom', 'Belgium')
}


# 我们可以通过下面的方法来实现简单的映射：

# In[ ]:


from typing import Any

def membership_map(s: pd.Series, groups: dict,
                   fillvalue: Any=-1) -> pd.Series:
    # Reverse & expand the dictionary key-value pairs
    groups = {x: k for k, v in groups.items() for x in v}
    return s.map(groups).fillna(fillvalue)


# In[ ]:


membership_map(countries, groups, fillvalue='other')


# 很简单对不对，现在让我们看一下最关键的一行代码，groups = {x: k for k, v in groups.items() for x in v}，这个是我之前提到过的字典推导式：

# In[ ]:


test = dict(enumerate(('ab', 'cd', 'xyz')))
{x: k for k, v in test.items() for x in v}


# ### 7. 压缩pandas对象

# In[ ]:


如果你的pandas版本大于0.21.0，那么都可以直接把pandas用压缩形式写入，常见的类型有gzip, bz2, zip，这里我们直接用刚才鲍鱼的数据集：


# In[ ]:


abalone.to_json('df.json.gz', orient='records',lines=True, compression='gzip')  # 压缩为gz类型
abalone.to_json('df.json', orient='records', lines=True)                        #压缩为json


# In[ ]:


import os.path
os.path.getsize('df.json') / os.path.getsize('df.json.gz')  #压缩大小差了10倍，还是gz更厉害


# ### 8. 源码及GitHub地址

# 这一期为大家总结了很多pandas实用的小技巧，希望大家喜欢
# 
# 我把这一期的ipynb文件和py文件放到了Github上，大家如果想要下载可以点击下面的链接：
#  - Github仓库地址： [https://github.com/yaozeliang/pandas_share](https://github.com/yaozeliang/pandas_share)
# 
# 
# 这一期就到这里啦，希望大家能够继续支持我，完结，撒花
