# -*- coding: utf-8 -*-
"""
共享单车项目

@author: Roy(Zhang Hailong)
"""
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def group_stats(df, list_label):
    """
    功能：统计某一列（或多列组合）的众数
    参数：需要被统计的列（可以有多列组合）
          df是要分析的DataFrame
          list_label可以是有多个值的list
    返回值：众数，以及众数出现的次数
    """
    group_sum = df.groupby(list_label)['counts'].sum()
    group_sum_max = group_sum.max()
    group_sum_max_name = group_sum[group_sum == group_sum_max].index[0]
    
    return group_sum_max_name, group_sum_max

def get_filters():
    """
    告诉用户怎么输入（城市，月份，星期）相应查找的数据。
    实现交互性，并传递用户输入的值。
    
    返回值：city：用户想要查找的城市
           month：用户想要查找的月份（可以是all,表示所有月份）
           day：用户想要查找的星期（可以是all,表示所有星期）
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    print('Would you like to see data for Chicago, New York city, or Washington?')
    while True:
        # city接受输入城市名
        city = input().lower().strip()
        if city in ['chicago', 'new york city', 'washington']:
            break
        # 如果输入不匹配，需要提醒重新输入
        print('Sorry, There is a problem with the entry. Please enter again!(like "Chicago" "chicago" "CHICAGO")')   
    
    print('Which month? January, February, March, April, May, June, or all?')
    while True:
        # 将输入字符串转换为固定格式
        month = input().lower().title().strip()
        if month in ['January', 'February', 'March', 'April', 'May', 'June', 'All']:
            break
        # 如果输入字符串不匹配，需要提醒重新输入
        print('Sorry, There is a problem with the entry. Please enter again!(like "January" "january")')

    print('Which day?Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or All.')
    # 输入星期
    while True:
        day = input().lower().title().strip()
        if day in ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday','All']:
            break
        print('Sorry, There is a problem with the entry. Please enter again!(like "all" "Monday")')
    
    print('-'*40)
    if month != 'All' and day != 'All':
        print('Now I\'ll make statistics for you about \ncity:{}   month:{}   day:{}'
              .format(city, month, day))
    elif month == 'All' and day != 'All':
        print('Now I\'ll make statistics for you about \ncity:{}   day:{}'
              .format(city, day))
    elif month == 'All' and day == 'All':
        print('Now I\'ll make statistics for you about {}'
              .format(city))
    else:
        print('Now I\'ll make statistics for you about \ncity:{}   month:{}'
              .format(city, month))
    print('-'*40)
    
    return city, month, day


def load_data(city, month, day):
    """
    加载并处理用户输入的数据。
    
    返回值：返回一个按客户输入要求筛选的df数据集
    """
    # 读取city对应的csv文件
    df = pd.read_csv(CITY_DATA[city])
    # 将'Start Time'列转换为datetime对象
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # 从'Start Time'列中提取出month,day_week和hour，并生成新的列
    df['month'] = df['Start Time'].dt.month
    df['day_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour
    # 创建count列，全部赋值1，以便后续统计
    len1 = len(df['Start Time'])
    df['counts'] = np.ones((len1,), dtype = np.int64)
    # 判断并转换month
    if month != 'All':
        # 将输入的month用数字替换
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        month = months.index(month) + 1
        # 筛选出需要查询的month行
        df = df[df['month'] == month]

    # 判断并转换day
    if day != 'All':
        # 筛选出符合输入day的day_week行
        df = df[df['day_week'] == day]

    return df

def time_stats(df):
    """显示统计学信息，月份，星期，小时的众数。"""

    print('\nCalculating The Most Frequent Times of Travel...\n')

    months = ['January', 'February', 'March', 'April', 'May', 'June']
    # month列的众数就是popular month
    popular_month = months[df['month'].mode()[0] - 1]
    print('The most popular month for traveling: {}'.format(popular_month))
    # day_week列的众数就是popular day
    popular_day = df['day_week'].mode()
    print('The most popular day for traveling: {}'.format(popular_day[0]))
    # hour列的众数就是popular hour
    popular_hour = df['hour'].mode()
    print('The most popular hour of the day to start traves: {} o\'clock'.format(popular_hour[0]))
    
    print('-'*40)

def station_stats(df):
    """显示最受欢迎的站点，以及站点组合。"""
    
    print('\nCalculating The Most Popular Stations and Trip...\n')
    # 起点站出现最多的站点名字，以及次数用group_stats()函数
    sta_most_sta, sta_most_num = group_stats(df, 'Start Station')
    print('The most commonly used start station is: {}, {} times'.format(sta_most_sta, sta_most_num))
    # 终点站出现最多的站点名字，以及次数
    end_most_sta, end_most_num = group_stats(df, 'End Station') 
    print('The most commonly used end station is: {}, {} times'.format(end_most_sta, end_most_num))
    # 起点站到终点站出现最多的组合，以及次数
    start_end_sta, start_end_num = group_stats(df, ['Start Station','End Station'])
    print('The most frequent combination of start station and end station trip is: ({}) to ({}), {} times'
          .format(start_end_sta[0], start_end_sta[1], start_end_num))

    print('-'*40)

def trip_duration_stats(df):
    """显示总共租车时间，和平均一次的租车时间。"""

    print('\nCalculating Trip Duration...\n')
    # 总共花费时间
    tal_time = df['Trip Duration'].sum() / 3600
    print('This is the total travel time: {:.2f} hour'.format(tal_time))
    # 每次骑车的平均花费时间
    mean_time = df['Trip Duration'].mean() / 60
    print('This is mean travel time: {:.2f} min'.format(mean_time))
    
    print('-'*40)

def user_stats(df):
    """显示用户的统计学信息。"""
    
    print('\nCalculating User Stats...\n')
    # 显示不同用户类型的数据
    user_type = df.groupby('User Type')['counts'].sum()
    print('User type : {} have {} \nUser type :{} have {}'
          .format(user_type.index[0],user_type[0],user_type.index[1],user_type[1]))

    # 显示不同性别用户的数据
    try:
        gender_sum = df.groupby('Gender')['counts'].sum()
        print('Gender : {} have {} \nGender : {} have {}'
              .format(gender_sum.index[0],gender_sum[0],gender_sum.index[1],gender_sum[1]))   
    except:
        print('-'*40)
        print('Sorry,We don\'t get the data of gender.')
    # 出生日期出现最多的年份，以及出现次数
    try:
        birth_most_year, birth_most_year_num = group_stats(df, 'Birth Year')
        print('The most common year of birth is : {:.0f} have {}'
              .format(birth_most_year, birth_most_year_num))
    # 最早出生的年份
        birth_earliest = df['Birth Year'].min()
        print('The earliest year of birth is : {:.0f}'.format(birth_earliest))
    # 最年轻的出生年份
        birth_recent = df['Birth Year'].max()
        print('The recent year of birth is : {:.0f}'.format(birth_recent))
    except:
        print('-'*40)
        print('Sorry,We don\'t get the data of birth year data.')
    print('-'*40)

def main():
    while True:
        print('-'*40)
        city, month, day = get_filters()
        df = load_data(city, month, day)
        
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
