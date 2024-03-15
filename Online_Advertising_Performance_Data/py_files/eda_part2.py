# -*- coding: utf-8 -*-
"""eda_part2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1vwCyWWGX0OwOgCphWewg0r5rulZdaqX6
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style("dark")

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

df.info()

"""**Q12) Are there any outliers in terms of cost, clicks, or revenue that warrant further investigation?**"""

fig,ax = plt.subplots(nrows=1,ncols=3,figsize = (20,6))
ax[0].boxplot(df['cost'])
ax[1].boxplot(df['clicks'])
ax[2].boxplot(df['revenue'])

ax[0].set_title('Cost Variance')
ax[0].set_ylabel('Cost Values')
ax[0].set_xlabel('Index')

ax[1].set_title('Clicks Variance')
ax[1].set_ylabel('Number of clicks')
ax[1].set_xlabel('Index')

ax[2].set_title('Revenue Variance')
ax[2].set_ylabel('Revenue Generated')
ax[2].set_xlabel('Index')

plt.show()

df['cost'] = df['cost'].astype('float32')
df['clicks'] = df['clicks'].astype('int32')
df['revenue'] = df['revenue'].astype('float32')

q12_df = df[['cost','clicks','revenue']]

Q3 = q12_df[['cost','clicks','revenue']].quantile(0.75).reset_index()

Q1 = q12_df[['cost','clicks','revenue']].quantile(0.25).reset_index()

q12_describe = Q1.merge(Q3)

q12_describe['IQR'] = q12_describe[0.75] - q12_describe[0.25]
q12_describe['1.5*IQR'] = q12_describe['IQR'] * 1.5
q12_describe['upper_bound'] = q12_describe[0.75] + q12_describe['1.5*IQR']
q12_describe['lower_bound'] = q12_describe[0.25] - q12_describe['1.5*IQR']

q12_describe

"""**Outliers for Cost**"""

df[(df['cost'] > (q12_describe.loc[0]['upper_bound'])) | (df['cost'] < (q12_describe.loc[0]['lower_bound']))]

"""**Outliers for Clicks**"""

df[(df['clicks'] > (q12_describe.loc[1]['upper_bound'])) | (df['clicks'] < (q12_describe.loc[1]['lower_bound']))]

"""**Outliers for Revenue**"""

df[(df['revenue'] > (q12_describe.loc[2]['upper_bound'])) | (df['revenue'] < (q12_describe.loc[2]['lower_bound']))]

"""**The following are the conclusions regarding outliers related to cost, clicks, and revenues.**
- It is evident from the boxplot for each section that outliers are present in all of them.
- Upon conducting a more detailed analysis, it is determined that the cost section contains 2515 outliers, the clicks section has 2325 outliers, and the revenue section has 2512 outliers, out of a total of 15403 values.

**Q13)How does the effectiveness of campaigns vary based on the size of the ad and placement type?**
"""

df2 = pd.read_csv('../dataframes/online_advertising_performance_data.csv')
df['banner'] = df2['banner']
df['banner'] = df['banner'].astype('category')

q11_df = df[df['updated_placement'].isin(['abc','def','ghi','jkl','mno'])]
updated_index = q11_df['updated_placement'] != 'No Data Available'
df['post_click_conversions_rate'] = (q11_df['post_click_conversions'] / q11_df['clicks']) * 100
df['post_click_conversions_rate'].fillna(0,inplace=True)

"""**An overall summary of each section with respect to each banner and placement pair for each campaign**"""

df.pivot_table(index = ['banner','updated_placement'],columns='campaign_number',values = ['clicks','revenue','post_click_conversions','post_click_sales_amount'],aggfunc='sum')

banner_placement_clicks = df.pivot_table(index = ['banner','updated_placement'],columns='campaign_number',values = ['clicks'],aggfunc='sum')
banner_placement_clicks

sns.heatmap(banner_placement_clicks)
plt.title('HeatMap For Banner and Placment and Clicks For Respective Campaigns')
plt.xlabel('Campaigns')
plt.ylabel('Banner and Placements')
plt.show()

"""**The efficacy of campaigns demonstrates variance contingent upon both ad size and placement type, as follows:**
- While there are various other factors contributing to the determination of the campaign's effectiveness, we have focused our analysis primarily on the number of clicks as a key metric.
- The observation revealed that, considering all campaigns, the combination of 240 x 600 ads under placement "ghi" generated the highest number of clicks.
- Regarding camp 1 and camp 2, the 240 x 600 ad placement under "ghi" combination was the most productive.
- Camp 3 exhibited minimal deviation across all combinations, consistently yielding clicks within the range of 30000-40000.

**Q14)Are there any specific campaigns or banner sizes that consistently outperform others in terms of ROI?**
"""

df.head()

df['return'] = df['revenue'] - df['cost']

df.head()

campaign_ROI = df.pivot_table(index = 'campaign_number',values = ['cost','revenue','return'],aggfunc='sum')
campaign_ROI

campaign_ROI['ROI'] = (campaign_ROI['return'] / campaign_ROI['cost']) * 100

campaign_ROI

campaign_ROI['ROI'].plot(kind = 'bar',color = 'r')
plt.title('ROI For Each Campaign')
plt.xlabel('Campaigns')
plt.ylabel('Return on Investments')
plt.show()

banner_ROI = df.pivot_table(index = 'banner',values = ['cost','revenue','return'],aggfunc='sum')
banner_ROI['ROI'] = (banner_ROI['return'] / banner_ROI['cost']) * 100
banner_ROI

banner_ROI['ROI'].plot(kind = 'bar',color = 'orange')
plt.title('ROI For Each Banner Size')
plt.xlabel('Banners')
plt.ylabel('Return on Investments')
plt.show()

"""**Conclusions drawn regarding specific campaigns and banners outperforming others.**
- Campaign 2 demonstrates the highest ROI, exceeding 100%, in comparison to Campaign 1, which yields slightly above 50%, followed by Campaign 3 with a 45% ROI.
- The 240 x 400 banner achieves an exceptional ROI of approximately 130%, whereas the 800 x 250 banner yields a considerably unfavorable ROI of -61%.

**Q15) What is the distribution of post-click conversions across different placement types?**
"""

q11_df.pivot_table(index = 'updated_placement',values = ['post_click_conversions'],aggfunc=['sum','max'])

sns.displot(kind = 'kde',data = q11_df,x = 'post_click_conversions')
plt.title('KDE Plot For Post Click Conversions')
plt.xlabel('Post Click Conversions')
plt.ylabel('Density')
plt.show()

df['post_click_conversions'].skew()

df['post_click_conversions'].kurtosis()

df['post_click_conversions'].mean()

sns.displot(kind = 'kde',data = q11_df,x = 'post_click_conversions',hue = 'updated_placement')
plt.title('KDE Plot For Post Click Conversions')
plt.xlabel('Post Click Conversions')
plt.ylabel('Density')
plt.show()

df.pivot_table(index = 'updated_placement',values = ['post_click_conversions'],aggfunc='sum').plot(kind = 'line',c = 'r')
plt.title('Line Plot For Post Click Conversions For Each Placement')
plt.xlabel('Placements')
plt.ylabel('Post Click Conversions')
plt.show()

"""**Conclusions drawn regarding the distribution of post-click conversions across various placement types.**
- The distribution of post-click conversions across various placements exhibits positive skewness and high kurtosis, both collectively and when examined individually for each placement.
- Outliers are evident within each placement when examined individually.
- Post-click conversions are at their peak for placement "ghi" and at their lowest for placement "abc".

**Q16)Are there any noticeable differences in user engagement levels between weekdays and weekends?**

>The year chosen for analysis in 2020.
"""

import datetime as dt

df['day'] = df['day'].astype('int16')

df['month'].value_counts()

df['month_num'] = 0

def month_check(df):
    for i in df.index:
        month = df.iloc[i]['month']
        if(month == 'April'):
            df.at[i,'month_num'] = 4
        elif(month == 'May'):
            df.at[i,'month_num'] = 5
        elif(month == 'June'):
            df.at[i,'month_num'] = 6

month_check(df)

df['month_num'] = df['month_num'].astype('int16')

df.info()

def day_check(df):
    for i in df.index:
        day = df.iloc[i]['day']
        month = df.iloc[i]['month_num']
        year = 2020
        date_string = f"{year}-{month:02d}-{day:02d}"
        time_stamp = pd.Timestamp(date_string)
        df.at[i,'Day'] = (time_stamp.day_name())

day_check(df)

df.head()

df['Day'] = df['Day'].astype('category')

df['Weekend'] = df['Day'].apply(lambda x: 1 if (x == 'Sunday') or (x == 'Saturday') else 0)

weekend_user_crosstab = pd.crosstab(df['user_engagement'],df['Weekend'])
weekend_user_crosstab # 0 -> weekday and 1 -> weekend

sns.heatmap(weekend_user_crosstab)
plt.title('HeatMap for User Engagements on Weekdays and Weekends')
plt.xlabel('0 -> Weekday and 1 -> Weekend')
plt.ylabel('User Engagements')
plt.show()

sns.countplot(data = df, x = 'user_engagement',hue = 'Weekend')
plt.title('CountPlot for User Engagements on Weekdays and Weekends')
plt.xlabel('User Engagements')
plt.ylabel('Counts')
plt.show()

"""**Conclusions regarding user engagement in relation to weekdays versus weekends.**
- Engagement levels in each category notably peak during weekdays compared to weekends.
- During weekends, user engagement across high, medium, and low sections is observed to be nearly equal.
- On weekdays, medium engagement edges out low engagement, followed by high engagement, with only slight differences.

**Q17)How does the cost per click (CPC) vary across different campaigns and banner sizes?**
"""

df.head()

df['cost_per_click'] = df['cost'] / df['clicks']

df.head()

"""**There are many campaigns which have some cost with zero clicks.**
**We will ignore such campaigns.**
"""

q17_df = df[df['clicks'] != 0]
q17_df.sample(5)

"""**Analysing with respect to campaigns.We would calculate mean cost per click for each campaign.**"""

camp_cost_per_click = q17_df.pivot_table(index = 'campaign_number',values='cost_per_click',aggfunc='mean')
camp_cost_per_click

camp_cost_per_click.plot(kind = 'bar',color = 'maroon')
plt.title('Cost Per Click For Each Campaign')
plt.xlabel('Campaigns')
plt.ylabel('Cost Per Click')
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--',color = 'black')
plt.show()

"""**Analysing with respect to banner sizes.We would calculate mean cost per click for each campaign.**"""

banner_cost_per_click = q17_df.pivot_table(index = 'banner',values='cost_per_click',aggfunc='mean')
banner_cost_per_click

banner_cost_per_click.plot(kind = 'bar',color = 'orange',figsize = (10,6))
plt.title('Cost Per Click For Each Banner')
plt.xlabel('Banners')
plt.ylabel('Cost Per Click')
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--',color = 'black')
plt.show()

q17_df.pivot_table(index = ['campaign_number','banner'],values='cost_per_click',aggfunc='mean').plot(kind = 'bar',figsize = (10,6))
plt.title('Cost Per Click For Each Campaign and Banner Pair')
plt.xlabel('Campaigns-Banners')
plt.ylabel('Cost Per Click')
plt.show()

"""**The findings regarding the variation in cost per click (CPC) across different campaigns and banner sizes are summarized as follows:**
- Camp 1 exhibits the highest mean cost per click, followed by Camp 3 and then Camp 2.
- Hence, Camp 2 boasted the most economical rates, while Camp 1 emerged as the priciest option.
- The 468 x 60 banner size demonstrates the greatest cost per click, followed by the remaining sizes which have nearly identical CPCs. The 800 x 250 size exhibits the lowest CPC.
- After analyzing each camp-banner pair, it was observed that the combination of Camp 1 and the 468x60 banner exhibited the highest CPC compared to others, while the combination of Camp 2 and the 800x250 banner had the lowest CPC.

**Q18)Are there any campaigns or placements that are particularly cost-effective in terms of generating post-click conversions?**
"""

df.head()

"""**We would use the dataframe created in Q17.**

"""

import warnings
warnings.filterwarnings('ignore')
q17_df['post_click_conversions_per_click'] = q17_df['post_click_conversions_rate'] / 100
q17_df['post_click_conversions_sales_per_click'] = q17_df['post_click_sales_amount'] / q17_df['clicks']
q17_df

per_click_cost_sales_conversions_camp = q17_df.pivot_table(index = 'campaign_number',values = ['cost_per_click','post_click_conversions_per_click','post_click_conversions_sales_per_click'],aggfunc='mean')
per_click_cost_sales_conversions_camp

q17_df.pivot_table(index = 'campaign_number',values = ['cost_per_click','post_click_conversions_per_click'],aggfunc='mean').plot(kind = 'bar')
plt.title('Mean Cost per Click and Post-Click Conversions per Click by Campaign Number')
plt.xlabel('Campaign Number')
plt.ylabel('Mean Value')
plt.xticks(rotation=45)
plt.show()

per_click_cost_sales_conversions_camp['post_click_conversions_sales_per_click'].plot(kind = 'area')
plt.title('Mean Post Click Sales Amount per Click by Campaign Number')
plt.xlabel('Campaign Number')
plt.ylabel('Mean Value')
plt.show()

per_click_cost_sales_conversions_placement = q17_df.pivot_table(index = 'updated_placement',values = ['cost_per_click','post_click_conversions_per_click','post_click_conversions_sales_per_click'],aggfunc='mean')
per_click_cost_sales_conversions_placement

q17_df.pivot_table(index = 'updated_placement',values = ['cost_per_click','post_click_conversions_per_click'],aggfunc='mean').plot(kind = 'bar',color=['red', 'green'])
plt.title('Mean Cost per Click and Post-Click Conversions per Click by Placements')
plt.xlabel('Placements')
plt.ylabel('Mean Value')
plt.xticks(rotation=45)
plt.show()

per_click_cost_sales_conversions_placement['post_click_conversions_sales_per_click'].plot(kind = 'area',color = 'purple')
plt.title('Mean Post Click Sales Amount per Click by Placements')
plt.xlabel('Placements')
plt.ylabel('Mean Value')
plt.show()

"""**Conclusions regarding the cost-effectiveness of campaigns or placements concerning post-click conversions.We would ignore 'No Data Available' which stands for NaN Values.**
- When analyzing on a per-click basis, it is evident that Campaign 1 yields the most favorable post-click conversions.
- Post-click sales are also dominated by Campaign 1, solidifying its position as the most cost-effective option, followed by Campaign 3 and then Campaign 2.
- Placement ABC exhibits the most favorable post-click conversions per click.
- The per-click sales amount performance is optimal for placement ABC, followed by JKL, and is least for DEF.

**Q19)Can we identify any trends or patterns in post-click conversion rates based on the day of the week?**
"""

day_wise_post_click_conversion_rates = df[df['clicks'] != 0].pivot_table(index = 'Day',values = 'post_click_conversions_rate',aggfunc = 'mean')
day_wise_post_click_conversion_rates

day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
day_wise_post_click_conversion_rates = day_wise_post_click_conversion_rates.reindex(day_order) # ordering the day index

day_wise_post_click_conversion_rates

day_wise_post_click_conversion_rates.plot(kind = 'barh',color = 'orange',figsize = (18,6))
plt.title('Day-wise Post-Click Conversion Rates')
plt.xlabel('Conversion Rate')
plt.ylabel('Day')
plt.show()

df[df['clicks'] != 0].pivot_table(index = 'Day',columns = 'campaign_number',values = 'post_click_conversions_rate',aggfunc = 'mean').reindex(day_order).plot()
plt.title('Day-wise Post-Click Conversion Rates With Each Campaign')
plt.xlabel('Day')
plt.ylabel('Conversion Rate')
plt.show()

"""**Conclusions regarding trends in post-click conversion rates with respect to days of the week.**
- Post-click conversion rates peak on Thursday, with the other days closely trailing behind.
- When analyzed by campaign, it's evident that Campaign 1 boasts the highest conversion rate, followed by Campaign 3 and then Campaign 2.
- For Campaign 1, the highest conversion rates are observed on Thursday. For Campaign 2, they are on Tuesday, and for Campaign 3, also on Tuesday.

**Q20)How does the effectiveness of campaigns vary between new users and returning users in terms of post-click conversions?**
"""

df.head()

"""**New users are defined as individuals who have only one click.**"""

q20_df = df[df['clicks'] !=0]
q20_df['new_user'] = q20_df['clicks']
q20_df.head()
q20_df['new_user'] = q20_df['new_user'].apply(lambda x: 1 if x==1 else 0)

q20_df.sample(5)

## 1 denotes new user
## 0 denotes returning user
new_returning_user = q20_df.pivot_table(index = 'new_user',values='post_click_conversions_rate',aggfunc='mean')
new_returning_user

new_returning_user.plot(kind = 'bar',cmap='coolwarm')
plt.title('New vs Returning User Post Click Conversions')
plt.xlabel('User Type (New (1) or Returning (0) )')
plt.ylabel('Post Click Conversion Rates')
plt.xticks(rotation = 0)
plt.show()

new_returning_user_camp = q20_df.pivot_table(index = 'new_user',columns='campaign_number',values='post_click_conversions_rate',aggfunc='mean')
new_returning_user_camp

new_returning_user_camp.plot(kind = 'bar',cmap='viridis')
plt.title('New vs Returning User Post Click Conversions For Each Campaign')
plt.xlabel('User Type (New (1) or Returning (0) )')
plt.ylabel('Post Click Conversion Rates')
plt.xticks(rotation = 0)
plt.show()

"""**Here are the conclusions regarding the effectiveness of the campaign concerning post-click conversion rates for both new and returning users.**
- New users demonstrate superior post-click conversion rates compared to returning users in the analyzed campaigns.
- A consistent trend is observed across all three campaigns, with new users outperforming returning users in terms of post-click conversion rates.

**Q21)How does the effectiveness of campaigns vary throughout different user engagement types in terms of post-click conversions?**
"""

user_conversion = q20_df.pivot_table(index = 'user_engagement',values='post_click_conversions_rate',aggfunc='mean')
user_conversion

user_conversion.plot(kind = 'bar',color = 'red')
plt.title('User Engagements and Post-Click Conversion Rates')
plt.xlabel('User Engagements')
plt.ylabel('Post Click Conversion Rates')
plt.xticks(rotation = 0)
plt.show()

user_camp_conversion_rate = q20_df.pivot_table(index = 'user_engagement',columns='campaign_number',values='post_click_conversions_rate',aggfunc='mean').fillna(0)
user_camp_conversion_rate

sns.heatmap(user_camp_conversion_rate,cmap='coolwarm')
plt.title('User Engagements and Post-Click Conversion Rates For Each Campaign')
plt.xlabel('User Engagements')
plt.ylabel('Post Click Conversion Rates')
plt.xticks(rotation = 0)
plt.show()

"""**In conclusion, the campaign's effectiveness in terms of post-click conversions appears to be...**
- The post-click conversion rates are significantly higher for users with high engagement compared to those with medium and low engagement, indicating a notable margin between the groups.
- Camp 1 and Camp 3 exhibit high levels of engagement, while Camp 2 is characterized by medium engagement.
"""