
# coding: utf-8

# ## Pandas 如何根据需要创建简单模型

# 大家好，今天这一期我想和大家分享有关于pandas创建模型的部分，首先让我们来看一个比较常见的场景：
# 
# >**你每天需要打开N个excel进行相同的操作，各种眼花缭乱的VBA函数后老眼昏花。。。。
# 
# 这种情况下，最好的解决办法是先仔细想想业务需求是什么，根据实际情况可以用pandas搭建一个小型模型，一旦搭建完毕，你每天上班时就可以愉快地运行Python脚本，转身去喝杯咖啡，几分钟后心满意足地回来，发现所有的繁琐操作已经搞定了，生活是这么美好、、、
# 
# 
# 闲话少说，让我今天抛砖引玉，为大家简单介绍一个我使用比较多的小模型：检验数据一致性（新老数据增加和减少的数量一致），今天的文章主要分为5部分
# 
# 1. 制作假数据
# 2. 明确模型的目的
# 3. 开始实践
# 4. 源码及GitHub地址
# 
# 好啦，话不多说，让我们一个个看吧

# ## 1. 制作假数据

# In[1]:


import os


# In[2]:


#这两行仅仅是切换路径，方便我上传Github，大家不用理会
os.chdir("F:\\Python教程\\segmentfault\\pandas_share\\Pandas之旅_05 如何构建基础模型")
os.getcwd()


# 首先让我们一起制作一些假数据，我这里接下来生成一些有关订单的假数据，当然，到了文章的最后可能你会发现我们的模型并不是完美适用于这个类型，你会在生活中根据自己需要来调整，但是至少基础的思路已经有啦！

# 先建立一个fake_product的字典，keys是产品，value是单价，这里我们用一个在网上随便找到的商品名称的csv数据集,它只有一列ProductNames

# In[3]:


import numpy as np
import pandas as pd
f"Using {pd.__name__},{pd.__version__}"


# In[4]:


fake_df = pd.read_csv("product_names.csv")
fake_df.head(10)


# In[5]:


fake_df['Product_Names'].is_unique


# 这里我们可以看到，数据集主要包括的就是一些产品的名字，而且没有重复值，我们现在把他们导出至一个字典，并随机给每个产品任意的价格(在20至100之间),因为这里我们要随机生成一些假数据，所以让我们引用random这个包

# In[6]:


import random


# In[7]:


fake_product = { k:random.randint(20,100) for k in fake_df['Product_Names']}
fake_product


# In[8]:


len(fake_product)


#  这里我们看到生成了一个有144个item组成，key为产品名称，value及单价的fake_product字典，接下来为了省事，
# 我简单地创建了一个方法get_fake_data可以让我们最终得到一个填充好的假数据集合，返回的也是字典

# In[9]:


def get_fake_data(id_range_start,id_range_end,random_quantity_range=50):
#     Id=["A00"+str(i) for i in range(0,id_range)]
    Id=[]
    Quantity = []
    Product_name=[]
    Unit_price=[]
    Total_price=[]

    for i in range(id_range_start,id_range_end):
        random_quantity = random.randint(1,random_quantity_range)
        name, price = random.choice(list(fake_product.items()))

        Id.append("A00"+str(i))
        Quantity.append(random_quantity)
        Product_name.append(name)
        Unit_price.append(price)
        Total_price.append(price*random_quantity)
   
    result = {
    'Product_ID':Id,
    'Product_Name':Product_name,
    'Quantity':Quantity,
    'Unit_price':Unit_price,
    'Total_price':Total_price
}
    
    return result

# total = [quantity[i]* v for i,v in enumerate(unit_price)]    也可以最后用推导式来求total，皮一下
# total_price=[q*p for q in quantity for p in unit_price]


# 首先，这个方法不够简洁，大家可以优化一下，但是今天的重点在于小模型，让我们着重看一下最后返回的dict，它包含如下几列：
#  - Product_ID：订单号，按照顺序递增生成
#  - Product_Name：产品名称，随机生成
#  - Quantity：随机生成在1~random_quantity_range之间的每个订单的产品订购量
#  - Unit_price:产品价格
#  - Total_price：总价
#   
# 每组数据长度均为 id_range_end - id_range_start，现在让我们生成两组假数据：

# In[10]:


fake_data= get_fake_data(1,len(fake_product)+1)


# 这里我们可以看到我们生成了一组假数据，Id从A001 ~ A00145

# 让我们简单看看假数据的keys和每组数据的长度：

# In[11]:


fake_data.keys()


# In[12]:


for v in fake_data.values():
    print(len(v))


# 可以发现每组key对应的list长度都是144

# ## 2. 明确模型的目的

# 我们可以利用pandas自带的from_dict方法把dict转化为Dataframe，这里我们分别用刚刚生成的fake_data来模拟1月的库存和2月的库存情况，我们可以把fake_data分成两组，A001-A00140一组，A008-A00144一组，这样就完美的模拟了实际情况。
# 
# 因为大多数的商品名称不会改变（8~140的部分），但是从一月到二月，因为各种原因我们减少了7个商品种类的库存（1-7），又增加了4个种类的库存（141-144），我们这里验证一致性的公式就是：
# 

# > 新增的 + 一月数据总量 = 减少的 + 二月数据总量

# ## 3. 开始实践

# 现在让我们来实现这个小模型，首先生成stock_jan，stock_fev两个dataframe

# In[13]:


stock= pd.DataFrame.from_dict(fake_data)
stock.head()


# In[14]:


stock.set_index(stock['Product_ID'],inplace=True)
stock.drop('Product_ID',axis=1,inplace=True)
stock.head()


# In[15]:


# 获得1月份stock数据,A001-A00140
stock_jan=stock[:'A00140']
stock_jan.tail()


# In[16]:


# 获得2月份stock数据
stock_fev=stock['A008':]
stock_fev.tail()


# 现在让我们简单停顿一下，看看这两个df：
#  - stock_jan: A001 - A00140的所有数据
#  - stock_fev: A008 - A00144的所有数据
# 

# 接下来的操作很简单，用我们上篇文章提到的merge函数，这里merge的公有列为索引Product_ID，Product_Name,使用的是outer merge

# In[17]:


merge_keys=['Product_ID','Product_Name'] 


# In[18]:


check_corehence = stock_jan.merge(stock_fev,on=merge_keys,how='outer',suffixes=("_jan","_fev"))
check_corehence.head(10)


# In[19]:


check_corehence.tail()


# 大家可以发现前7行正是减少的商品库存，而后4行正是二月份新增的商品库存，现在让我们分别获得减少的商品库存数据和新增的商品库存数据：

# In[20]:


new_stock = check_corehence.loc[(check_corehence['Quantity_jan'].isnull()) & (check_corehence['Quantity_fev'].notnull())]
num_new = new_stock.shape[0]
num_new


# In[21]:


remove_stock = check_corehence.loc[(check_corehence['Quantity_fev'].isnull()) & (check_corehence['Quantity_jan'].notnull())]
num_remove = remove_stock.shape[0]
num_remove


# 再让我们分别看看1月和2月的数据量：

# In[22]:


# 1月数据量
num_stock_jan = stock_jan.shape[0]
num_stock_jan


# In[23]:


# 2月数据量
num_stock_fev = stock_fev.shape[0]
num_stock_fev


# 现在让我们套入公式：

# In[24]:


num_stock_jan + num_new


# In[25]:


num_stock_fev + num_remove


# 结果相等，数据一致性过关！

# ## 4. 源码及GitHub地址

# In[26]:


这一期为大家分享了一个简单的pandas检验数据一致性的模型，模型还是非常初级阶段，功能非常简单，但是基础的搭建流程想必大家已经熟悉了，接下来
小伙伴们可以根据业务需求搭建自己的模型啦，只要你每天和Excel打交道，总有一款模型适合你

我把这一期的ipynb文件和py文件放到了Github上，大家如果想要下载可以点击下面的链接：
 - Github仓库地址： [https://github.com/yaozeliang/pandas_share](https://github.com/yaozeliang/pandas_share/tree/master/Pandas%E4%B9%8B%E6%97%85_04%20pandas%E8%B6%85%E5%AE%9E%E7%94%A8%E6%8A%80%E5%B7%A7)


希望大家能够继续支持我，完结，撒花

