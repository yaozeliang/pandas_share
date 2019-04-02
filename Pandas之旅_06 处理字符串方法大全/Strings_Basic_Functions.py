
# coding: utf-8

# # 有关字符串基本方法

# 大家好，我又回来了！ 之前的几期我们已经简单了解了pandas的基础操作，但是只要涉及到数据，最常见的就是String（字符串）类型，所以很多时候我们其实都在和字符串打交道，所以今天，我会把我自己总结的，有关字符串的常用方法分享给大家，希望能够帮到各位小伙伴~

# ### Split and format

# In[1]:


latitude = '37.24N'
longitude = '-115.81W'
'Coordinates {0},{1}'.format(latitude,longitude)


# In[2]:


f'Coordinates {latitude},{longitude}'


# In[3]:


'{0},{1},{2}'.format(*('abc'))


# In[4]:


coord = {"latitude":latitude,"longitude":longitude}
'Coordinates {latitude},{longitude}'.format(**coord)


# ### **Access argument' s attribute**

# In[5]:


class Point:
    def __init__(self,x,y):
        self.x,self.y = x,y
    def __str__(self):
        return 'Point({self.x},{self.y})'.format(self = self)
    def __repr__(self):
        return f'Point({self.x},{self.y})'


# In[6]:


test_point = Point(4,2)
test_point


# In[7]:


str(Point(4,2))


# ### **Replace with %s , %r** :

# In[8]:


" repr() shows the quote {!r}, while str() doesn't:{!s} ".format('a1','a2')


# ### **Align** :

# In[9]:


'{:<30}'.format('left aligned')


# In[10]:


'{:>30}'.format('right aligned')


# In[11]:


'{:^30}'.format('centerd')


# In[12]:


'{:*^30}'.format('centerd')


# ### **Replace with %x , %o** :

# In[13]:


"int:{0:d}, hex:{0:x}, oct:{0:o}, bin:{0:b}".format(42)


# In[14]:


'{:,}'.format(12345677)


# ### **Percentage** :

# In[15]:


points = 19
total = 22
'Correct answers: {:.2%}'.format(points/total)


# In[16]:


import datetime as dt
f"{dt.datetime.now():%Y-%m-%d}"


# In[17]:


f"{dt.datetime.now():%d_%m_%Y}"


# In[18]:


today = dt.datetime.today().strftime("%d_%m_%Y")
today


# ### **Split without parameters** :

# In[19]:


"this is a  test".split()


# ### **Concatenate** :

# In[20]:


'do'*2


# In[21]:


orig_string ='Hello'
orig_string+',World'


# In[22]:


full_sentence = orig_string+',World'
full_sentence


# ### **Check string type , slice，count，strip** :

# In[23]:


strings = ['do','re','mi']
', '.join(strings)


# In[24]:


'z' not in 'abc'


# In[25]:


ord('a'), ord('#')


# In[26]:


chr(97)


# In[27]:


s = "foodbar"
s[2:5]


# In[28]:


s[:4] + s[4:]


# In[29]:


s[:4] + s[4:] == s


# In[30]:


t=s[:]
id(s)


# In[31]:


id(t)


# In[32]:


s is t


# In[33]:


s[0:6:2]


# In[34]:


s[5:0:-2]


# In[35]:


s = 'tomorrow is monday'
reverse_s = s[::-1]
reverse_s


# In[36]:


s.capitalize()


# In[37]:


s.upper()


# In[38]:


s.title()


# In[39]:


s.count('o')


# In[40]:


"foobar".startswith('foo')


# In[41]:


"foobar".endswith('ar')


# In[42]:


"foobar".endswith('oob',0,4)


# In[43]:


"foobar".endswith('oob',2,4)


# In[44]:


"My name is yaozeliang, I work at Societe Generale".find('yao')


# In[45]:


# If can't find the string, return -1
"My name is yaozeliang, I work at Societe Generale".find('gent')


# In[46]:


# Check a string if consists of alphanumeric characters
"abc123".isalnum()


# In[47]:


"abc%123".isalnum()


# In[48]:


"abcABC".isalpha()


# In[49]:


"abcABC1".isalpha()


# In[50]:


'123'.isdigit()


# In[51]:


'123abc'.isdigit()


# In[52]:


'abc'.islower()


# In[53]:


"This Is A Title".istitle()


# In[54]:


"This is a title".istitle()


# In[55]:


'ABC'.isupper()


# In[56]:


'ABC1%'.isupper()


# In[57]:


'foo'.center(10)


# In[58]:


'   foo bar baz    '.strip()


# In[59]:


'   foo bar baz    '.lstrip()


# In[60]:


'   foo bar baz    '.rstrip()


# In[61]:


"foo abc foo def fo  ljk ".replace('foo','yao')


# In[62]:


'www.realpython.com'.strip('w.moc')


# In[63]:


'www.realpython.com'.strip('w.com')


# In[64]:


'www.realpython.com'.strip('w.ncom')


# ### **Convert to lists** :

# In[65]:


', '.join(['foo','bar','baz','qux'])


# In[66]:


list('corge')


# In[67]:


':'.join('corge')


# In[68]:


'www.foo'.partition('.')


# In[69]:


'foo@@bar@@baz'.partition('@@')


# In[70]:


'foo@@bar@@baz'.rpartition('@@')


# In[71]:


'foo.bar'.partition('@@')


# In[72]:


# By default , rsplit split a string with white space
'foo bar adf yao'.rsplit()


# In[73]:


'foo.bar.adf.ert'.split('.')


# In[74]:


'foo\nbar\nadfa\nlko'.splitlines()


# ## 总结

# 除了我以上总结的这些，还有太多非常实用的方法，大家可以根据自己的需求去搜索啦！
# 
# 我把这一期的ipynb文件和py文件放到了Github上，大家如果想要下载可以点击下面的链接：
#  - Github仓库地址： [https://github.com/yaozeliang/pandas_share](https://github.com/yaozeliang/pandas_share/tree/master/Pandas%E4%B9%8B%E6%97%85_04%20pandas%E8%B6%85%E5%AE%9E%E7%94%A8%E6%8A%80%E5%B7%A7)
# 
# 
# 希望大家能够继续支持我，完结，撒花
