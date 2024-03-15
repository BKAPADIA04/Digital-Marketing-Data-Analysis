# -*- coding: utf-8 -*-
"""eda_part1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1WQrr-bC-KcK_O-zinm5N80SvHhEhQ_dt
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style("dark")

"""**We have the updated dataframes after data accessing and data cleaning.**"""

df = pd.read_csv('../dataframes/marketing_digital_after_accessing_cleaning_with_specific_dtypes.csv')
df = df.astype({
    'month': 'category',
    'day': 'int16',
    'campaign_number': 'category',
    'user_engagement': 'category',
    'displays': 'int32',
    'cost': 'float16',
    'clicks': 'int16',
    'revenue': 'float16',
    'post_click_conversions': 'int16',
    'post_click_sales_amount': 'float32',
    'updated_placement': 'category',
    'banner_width': 'int64',
    'banner_height': 'int64',
    'banner_area': 'int64'
})
df.head()

df.shape

df.info()

"""***EDA***

**Column Types**
- Categorical : month,campaign_number,user_engagement,updated_placement
- Numerical : day,displays,cost,clicks,revenue,post_click_conversions,post_click_sales_amount,banner_width,banner_height,banner_area

**Q1) What is the overall trend in user engagement throughout the campaign period?**
"""

df['user_engagement'].value_counts()

sns.displot(data = df, x = 'user_engagement', kind = 'hist')
plt.title('User Engagement')
plt.xlabel('User Engagements')
plt.ylabel('Count of users')
plt.show()

df['user_engagement'].value_counts().plot(kind='pie',autopct='%0.02f%%')
plt.title('User Engagement')
plt.show()

sns.countplot(data = df,x = 'user_engagement',hue = 'campaign_number')
plt.title('User Engagement')
plt.xlabel('User Engagements')
plt.ylabel('Count of users')
plt.show()

cross_tab = pd.crosstab(df['user_engagement'],df['campaign_number'])

cross_tab

sns.heatmap(cross_tab)
plt.show()

"""**Conclusions on User Engagements**
- Medium engagements slightly surpass both Low and High user engagements, holding a slight edge in comparison.
- Examining the data in terms of campaign numbers:
  1. For Campaign 1, user engagements are nearly equal across categories but show a slight edge in High engagements.
  2. Campaign 2 records engagements primarily in Low and Medium categories.
  3. In the case of Campaign 3, engagements are nearly balanced across all types.
- The camp 1 category, exhibiting high user engagement, is characterized by the maximum number of user engagements observed in the heatmap.
- The camp 2 category, marked by high user engagement, registers zero values in the heatmap.

**Q2) How does the size of the ad (banner) impact the number of clicks generated?**
"""

df2 = pd.read_csv('../dataframes/online_advertising_performance_data.csv')
df['banner'] = df2['banner']
df['banner'] = df['banner'].astype('category')

df[['banner','clicks']] #categorical vs numerical

sns.catplot(kind = 'box',data = df,x = 'banner',y = 'clicks',aspect=2)
plt.title('Banner vs Clicks')
plt.xlabel('Banners')
plt.ylabel('Clicks')
plt.show()

sns.catplot(kind = 'bar',data = df,x = 'banner',y = 'clicks',aspect=2)
plt.title('Banner vs Clicks')
plt.xlabel('Banners')
plt.ylabel('Clicks')
plt.show()

df.pivot_table(index = 'banner',values='clicks',aggfunc=['mean','median','sum','max','min'])

"""**Two columns : Mean and Sum Clicks of utmost importance.**"""

banner_clicks = df.pivot_table(index = 'banner',values='clicks',aggfunc=['mean','sum'])

sns.barplot(x=banner_clicks.index, y = ('mean', 'clicks'), data=banner_clicks , hue = ('sum', 'clicks'))
plt.title('Banner vs Clicks')
plt.xlabel('Banners')
plt.ylabel('Clicks')
plt.show()

"""**Conclusions on Size of Ad(Banner) vs Clicks**
- As shown in the boxplot, there are numerous outliers in each section regarding the size of the ad and the number of clicks.
- For each section, the barplot illustrates the mean central tendency along with a 95% Confidence Interval.
- The category 240 x 400 exhibits the highest mean and sum of the number of clicks, followed by approximately equal values for other sections.
- However, the mean for categories 468 x 60 and 800 x 250 is nearly zero.
- Hence, the distribution of mean clicks versus the size of the ad is *non-uniform*, as evident from the bar plot generated from the pivot table.

**Q3) Which publisher spaces (placements) yielded the highest number of displays and clicks?**
"""

df[['updated_placement','clicks','displays']]

"""**We would not consider 'No Data Available' Section.**"""

q3_df = df[df['updated_placement'].isin(['abc','def','ghi','jkl','mno'])]

q3_df[['updated_placement','clicks','displays']]

updated_index = q3_df['updated_placement'] != 'No Data Available'
q3_df.pivot_table(index = 'updated_placement',values=['clicks','displays'],aggfunc=['mean','sum','max','min'])

placements_clicks_displays = q3_df.pivot_table(index = 'updated_placement',values=['clicks','displays'],aggfunc=['mean','sum','max'])
placements_clicks_displays

sns.barplot(x=placements_clicks_displays.index, y = ('mean', 'clicks'), data = placements_clicks_displays , hue = ('sum', 'clicks'))
plt.title('Placements vs Clicks')
plt.xlabel('Placements')
plt.ylabel('Clicks')
plt.show()

sns.barplot(x=placements_clicks_displays.index, y = ('mean', 'displays'), data = placements_clicks_displays , hue = ('sum', 'displays'))
plt.title('Placements vs Displays')
plt.xlabel('Placements')
plt.ylabel('Displays')
plt.show()

"""**Conclusions regarding the association between publisher placements and displays as well as clicks.**
- The publisher "GHI" stands out with the highest mean and sum of clicks, while "ABC" lags behind with the least.
- The publisher "MNO" achieves the highest mean and total number of displays, while "ABC" yields the lowest.
"""

df.head()

"""**Q4) Is there a correlation between the cost of serving ads and the revenue generated from clicks?**"""

df[['cost','revenue']] # Numerical vs Numerical

"""**First we will check distribution of cost and revenue separately**"""

plt.figure(figsize=(8, 6))
sns.kdeplot(data = df,x = 'cost',color='r',fill = True,label = 'Cost')
sns.kdeplot(data = df,x = 'revenue',color='b',fill = True,label = 'Revenue')
plt.title('KDE Plots for Cost and Revenue')
plt.xlabel('Cost and Revenue')
plt.ylabel('Probability Density')
plt.legend()
plt.show()

q4_df = df
q4_df['cost'] = q4_df['cost'].astype('float64')
q4_df['cost'].skew()
q4_df['revenue'] = q4_df['revenue'].astype('float64')
q4_df['revenue'].skew()

q4_df['cost'].skew()

df['cost'].kurtosis()

df['revenue'].kurtosis()

"""**Plots : Scatterplot,2D Histogram,2D Kdeplot**

"""

sns.relplot(kind = 'scatter',data = df,x = df['cost'],y = df['revenue'],color = 'red',hue = 'campaign_number')
plt.title('Scatter Plot for Cost vs Revenue')
plt.xlabel('Cost')
plt.ylabel('Revenue')
plt.show()

sns.displot(kind = 'hist',data = df,x = 'cost',y = 'revenue',color = 'red')
plt.xlim(0,50)
plt.ylim(0,50)
plt.title('2D Histogram')
plt.xlabel('Cost')
plt.ylabel('Revenue')
plt.show()

sns.displot(kind = 'kde',data = df,x = 'cost',y = 'revenue',color = 'red')
plt.xlim(0,100)
plt.ylim(0,100)
plt.title('2D KDE Plot')
plt.xlabel('Cost')
plt.ylabel('Revenue')
plt.show()

sns.lmplot(data = df , x = 'cost',y = 'revenue',hue = 'campaign_number')
plt.title('Linear Regression Plot')
plt.xlabel('Cost')
plt.ylabel('Revenue')
plt.show()

"""**Correlation Coefficient**"""

corr_coeff = df['cost'].corr(df['revenue'])
corr_coeff

"""**Conclusions for relationship between the cost of serving ads and the revenue generated from clicks.**
- Both the cost and revenue exhibit positive skewness and kurtosis.
- The scatterplot illustrates a positive correlation coefficient.
- A correlation coefficient of 0.7605 indicates strong positive linear relationship between cost and revenue.
- Some outliers show notably high costs paired with low revenue, deviating significantly from the linear regression plot's expected values..

**Q5)What is the average revenue generated per click for Company X during the campaign period?**
"""

df.head()

df['revenue_per_click'] = (df['revenue'] / df['clicks']).fillna(0)

df['revenue'].mean()

revenue_campaign_number = df.pivot_table(index = 'campaign_number',values = ['revenue_per_click','revenue'],aggfunc='mean')
revenue_campaign_number

revenue_campaign_number['revenue'].plot(kind = 'pie',autopct = '%0.02f%%')
plt.title('Revenue Per Campaign')
plt.show()

revenue_campaign_number['revenue_per_click'].plot(kind = 'pie',autopct = '%0.02f%%')
plt.title('Revenue Per Click Per Campaign')
plt.show()

"""**Conclusions for average revenue generated per click during the campaign period.**
- The mean revenue generated per click for Company X during the campaign period is approximately 17.94.
- The pie chart highlights that Campaign 1 boasts the highest mean revenue generated per campaign, while Campaign 3 records the lowest.
- The pie chart illustrates the variability in the average revenue per click across campaigns, showcasing Campaign 1 with the highest mean revenue per click and Campaign 2 with the lowest.

**Q6) Which campaigns had the highest post-click conversion rates?**
"""

df[['campaign_number','post_click_conversions']]

"""**Firstly we would compute the overall post-click conversion rates across all the three campaigns 1,2 and 3.**"""

overall_post_click_conversion_rate = ((df['post_click_conversions'].sum()) / (df['clicks'].sum())) * 100
overall_post_click_conversion_rate

"""**Now we would compute campaign wise post-click conversions rate.**"""

campaign_post_conversions = df.pivot_table(index = 'campaign_number',values = ['clicks','post_click_conversions'],aggfunc='sum')
campaign_post_conversions['post_click_conversions_rate'] = (campaign_post_conversions['post_click_conversions'] / campaign_post_conversions['clicks']) * 100
campaign_post_conversions

campaign_post_conversions['post_click_conversions_rate'].plot(kind = 'pie',autopct = '%0.02f%%')
plt.title('Revenue Per Click Per Campaign')
plt.show()

sns.catplot(kind = 'bar',x = campaign_post_conversions.index,y = campaign_post_conversions['post_click_conversions_rate'],color='red')
plt.title('Post Click Conversion Rates')
plt.xlabel('Campaign Numbers')
plt.ylabel('Conversion Rates')
plt.show()

"""**The conclusions regarding the highest post-click conversion rates in relation to the campaigns.**
- The aggregate post-click conversion rate for all campaigns combined is approximately 26.15%.
- Indeed, based on the data, it is evident that Campaign 1 exhibits the highest post-click conversion rate (44.93%), demonstrating clear dominance over Campaigns 2 and 3 in terms of driving on-site transactions following ad clicks.

**Q7) Are there any specific trends or patterns in post-click sales amounts over time?**
"""

df.pivot_table(index = ['month','day'],values = 'post_click_sales_amount',aggfunc='sum')['post_click_sales_amount'].sort_values(ascending=False)

df.pivot_table(index = ['month','day'],values = 'post_click_sales_amount',aggfunc='sum').plot(color = 'maroon')
plt.title('Post Click Sales Amount')
plt.xlabel('Month,Day')
plt.ylabel('Amount')
plt.show()

month_day_camp_num_post_sales_amt = df.pivot_table(index = ['month','day','campaign_number'],values = 'post_click_sales_amount',aggfunc='sum')
month_day_camp_num_post_sales_amt

mon_day_camp_sales_amt = df.pivot_table(index=['month', 'day'], columns='campaign_number', values='post_click_sales_amount', aggfunc='sum')
mon_day_camp_sales_amt

mon_day_camp_sales_amt.plot()
plt.title('Post Click Sales Amount')
plt.xlabel('Month,Day')
plt.ylabel('Amount')
plt.show()

"""**Conclusions regarding particular patterns observed in post-click sales amounts over time.**
- Sales amounts reach their peak around April 4-5 and decrease notably around April 30.
- Following April 30, there's a subsequent increase in sales amounts, yet they fail to exceed their initial peak before declining back to zero around June 30.
- Following the decline around June 30, sales amounts experience a resurgence, reaching their second highest peak around May 16, and subsequently fluctuate with typical ups and downs.
- Campaign 1 significantly outperforms in post-click sales amount, followed by Campaign 2 and Campaign 3, which generate nearly equal sales but substantially less compared to Campaign 1.

**Q8) How does the level of user engagement vary across different banner sizes?**
"""

df[['user_engagement','banner']] # Categorical vs Categorical

user_banner = pd.crosstab(df['user_engagement'],df['banner'])
user_banner

sns.heatmap(user_banner)
plt.title('User Engagement vs Banner Size')
plt.xlabel('Banner Size')
plt.ylabel('User Engagements')
plt.show()

pd.crosstab(df['user_engagement'],df['banner'],normalize='index').plot(kind = 'bar')
plt.xlabel('User Engagement')
plt.ylabel('Proportion')
plt.title('Multivariate Bar Plot of User Engagement by Banner')
plt.legend(loc='upper left')
plt.show()

user_eng_banner_df = pd.crosstab(df['user_engagement'],df['banner'],normalize='index')
user_eng_banner_df.plot(kind='bar', stacked=True)
plt.xlabel('User Engagement')
plt.ylabel('Proportion')
plt.title('Stacked Bar Plot of User Engagement by Banner')
plt.legend(loc='upper left')
plt.show()

"""**Concise summary of the user engagement trends based on banner size is as follows:**
- Engagement levels across both 160 x 600 and 728 x 90 banners were largely comparable, with a slight preference towards 'medium' engagement.
- 'Medium' engagement takes precedence in both 300 x 250 and 670 x 90 banners, followed by 'low' and then 'high' engagement levels.
- Engagement levels are equivalent between 'low' and 'medium' for both 240 x 400 and 580 x 400 banners, both of which exceed 'high' engagement levels.
- In the case of the 468 x 60 banner, 'medium' engagement takes the lead in user engagement.
- In the case of the largest banner size, 800 x 250, 'high' user engagement predominates over the other categories.
- Hence the distribution of user engagement levels and banner size is non-uniform.

**These trends are depicted visually in a heatmap, stacked bar graph, and multivariable bar graph, providing insights into the varying levels of user engagement across different banner sizes.**

**Q9) Can we identify any seasonal patterns or fluctuations in displays and clicks throughout the campaign period?**
"""

df[['campaign_number','clicks','displays']]

"""**Correlation Coefficient**"""

df['clicks'].corr(df['displays'])

sns.relplot(kind = 'scatter',data = df,x = 'clicks',y = 'displays',color = 'blue')
plt.title('Seasonal Patterns in Displays and Clicks During the Campaign Period')
plt.xlabel('Number of Clicks')
plt.ylabel('Number of Displays')
plt.show()

sns.relplot(kind = 'scatter',data = df,x = 'clicks',y = 'displays',col = 'campaign_number',color = 'maroon')
plt.show()

sns.lmplot(data = df , x = 'clicks',y = 'displays')
plt.title('Linear Regression Plot For Clicks vs Displays')
plt.xlabel('Clicks')
plt.ylabel('Displays')
plt.show()

"""**Conclusions for relationship between number of clicks and displays throughout the campaign period.**
- The correlation coefficient between clicks and displays is 0.7669, indicating a strong positive correlation between these two variables.
- Outliers, such as instances where the number of clicks exceeds 12,000 while the displays fall within the range of 200,000 to 300,000, are present in the dataset. These outliers represent data points that significantly deviate from the overall pattern observed in the scatter plot.
- According to the Linear Regression Model, it suggests that the displays for the above outliers should have been around 700,000, indicating a substantial difference from the observed values.
- Comparing displays with respect to 2000 clicks, Campaign 1 exhibits the maximum number of displays, followed by Campaign 2. Unfortunately, the number of clicks in Campaign 3 is significantly low, falling below the 2000 threshold.

**Q10) Is there a correlation between user engagement levels and the revenue generated?**
"""

df[['user_engagement','revenue']]

pd.pivot_table(data = df,index = 'user_engagement',values='revenue',aggfunc=['sum','mean','median','max','min'])

sns.catplot(kind = 'box',data = df,x = 'user_engagement',y = 'revenue')
plt.title('User Engagement vs Revenue')
plt.xlabel('User Engagements')
plt.ylabel('Revenue')
plt.show()

sns.scatterplot(data = df,x = df.index,y = 'revenue',hue = 'user_engagement')
plt.title('User Engagement vs Revenue')
plt.xlabel('User Engagements')
plt.ylabel('Revenue')
plt.show()

from pandas import factorize

labels, categories = factorize(df['user_engagement'])
df['labels'] = labels
abs(df['revenue'].corr(df['labels']))

"""**Conclusions regarding the correlation between user engagement levels and revenue generation.**
- Total and mean revenue is maximized when targeting users with 'high' engagement levels, followed by those with 'medium' and 'low' engagement levels, respectively.
- Despite the low median revenues overall, the "medium" engagement group's median revenue surpasses that of the "high" group, which in turn exceeds that of the "low" group.
- Outliers are present across all sections, particularly notable in the high and medium user engagement categories.
- The correlation between user engagement and revenue generated is negligible, with a coefficient of 0.1344.

**Q11)Which placement types result in the highest post-click conversion rates?**
"""

q11_df = df[df['updated_placement'].isin(['abc','def','ghi','jkl','mno'])]
updated_index = q11_df['updated_placement'] != 'No Data Available'
q11_df = q11_df.pivot_table(index = 'updated_placement',values = ['clicks','post_click_conversions'],aggfunc='sum')
q11_df['post_click_conversions_rate'] = (q11_df['post_click_conversions'] / q11_df['clicks']) * 100
q11_df

q11_df['post_click_conversions_rate'].plot(kind = 'pie',autopct = '%0.02f%%')
plt.title('Post Click Conversion Rates Placement Wise')
plt.show()
## 0.00% is for NaN values which we assigned 'No Data Available'

sns.catplot(kind = 'bar',x = q11_df.index,y = q11_df['post_click_conversions_rate'],color='orange')
plt.title('Post Click Conversion Rates')
plt.xlabel('Placements')
plt.ylabel('Conversion Rates')
plt.show()

"""**The findings regarding placement types associated with the highest post-click conversion rates are as follows:**
- The publisher 'abc' stands out with an impressive post-click conversion rate of 52.02%, showcasing its dominance in this aspect.
- The publishers 'ghi', 'jkl', and 'mno' demonstrate nearly identical conversion rates, all slightly surpassing half of that achieved by 'abc'.
- The conversion rate for 'def' is the lowest among all publishers.
"""