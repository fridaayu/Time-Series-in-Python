#!/usr/bin/env python
# coding: utf-8

# In[11]:


#Load data time series
import pandas as pd
gaq2=pd.read_csv('https://dqlab-dataset.s3-ap-southeast-1.amazonaws.com/LO4/global_air_quality_4000rows.csv',
               parse_dates=True,index_col='timestamp')
print('Data Global Air:\n',gaq2.head())



# In[12]:


print('Data Global Air:\n',gaq.info())
#Convert to datatime
gaq=pd.read_csv('https://dqlab-dataset.s3-ap-southeast-1.amazonaws.com/LO4/global_air_quality_4000rows.csv')
print('Sebeleum di ubah ke datetime:\n', gaq.head())
#ubah mejadi datetime
gaq['timestamp']=pd.to_datetime(gaq['timestamp'])
gaq = gaq.set_index('timestamp')
print('Sesudah diubah dalam format datetime:\n',gaq.head())


# In[16]:


#Resampling untuk time series data
#Downsampling
#Mengurangi baris datetime menjadi frekuensi yang lebih lambat, bisa dibilang juga mengurangi rows dataset menjadi lebih sedikit
#Contoh: mengubah kolom datetime yang awalnya daily menjadi monthly
    
#Upsampling
#Kebalikan dari downsampling, menambah baris datetime menjadi frekuensi yang lebih cepat, menambah rows dataset dengan membuat kolom datetime menjadi lebih detail
#Contoh: mengubah kolom datetime yang awalnya daily menjadi hourly

#Downsampling dari daily to weekly dan kita hitung maksimum untuk seminggu
gaq_weekly = gaq.resample('W').mean()
print('Downsampling daily to weekly-mean:\n', gaq_weekly.head())
#Downsampling dari daily to quaterly dan kita hitung minimumnya untuk tiap quarter
gaq_quarterly = gaq.resample('Q').sum()
print('Downsampling daily to quarterly-sum:\n', gaq_quarterly.head())


# In[17]:


#Upsampling dari daily to hourly dan kita hitung reratanya
gaq_hourly = gaq.resample('H').mean()
print('Upsampling daily to hour-mean:\n',gaq_hourly.head())


# In[18]:


#Resample dari daily to 2 monthly, hitung reratanya, dan fillna = 'bfill'
gaq_2monthly = gaq.resample('2M').mean().fillna(method='bfill')
print('Resampling daily to 2 monthly - mean:\n',gaq_2monthly.head())


# In[21]:


#Visualisasi
import matplotlib.pyplot as plt
#Membuat pivot table yang menunjukkan waktu 
#di baris nya dan masing-masing value dari pollutant nya dalam kolom
gaq_vis =gaq[['pollutant','value']].reset_index().set_index(['timestamp','pollutant'])
gaq_vis = gaq_vis.pivot_table(index='timestamp',columns='pollutant',
                            aggfunc='mean').fillna(0)
gaq_vis.columns=gaq_vis.columns.droplevel(0)
print('Data gaq_vis:\n',gaq_vis.head())
#Membuat fungsi yang memberikan default value 0 ketika value nya di bawah 0 dan apply 
#ke setiap elemen dari dataset tersebut, kemudian menampilkannya sebagai chart
def default_val (val):
    if val <0:
        return 0
    else:
        return val
line1 = gaq_vis.resample('M').mean().ffill().applymap(lambda x: default_val(x)).apply(lambda x: x/x.max())
line1.plot(
    title = 'Average value of each pollutant over months',
    figsize =(10,10),
    ylim=(0,1.25),
    subplots=True)
plt.ylabel('AVG pollutant (%)')
plt.xlabel('month')
plt.show()


# In[ ]:




