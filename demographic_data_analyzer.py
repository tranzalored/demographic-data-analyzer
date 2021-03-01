import pandas as pd
import numpy as np

def calculate_demographic_data(print_data=True):
    # Read data from file
    df = pd.read_csv('adult.data.csv')

    # How many of each race are represented in this dataset? This should be a Pandas series with race names as the index labels.
    race_count = df.groupby(['race']).count()

    # What is the average age of men?
    t=df.groupby('sex').mean()
    average_age_men = round(t['age']['Male'],1)

    # What is the percentage of people who have a Bachelor's degree?
    percentage_bachelors = round(df['education'].value_counts(normalize=True)['Bachelors']*100,1)

    # What percentage of people with advanced education (`Bachelors`, `Masters`, or `Doctorate`) make more than 50K?
    # What percentage of people without advanced education make more than 50K?

    # with and without `Bachelors`, `Masters`, or `Doctorate`
    higher_education = round(df['education'].value_counts()[['Bachelors','Masters','Doctorate']].sum(),1)
    lower_education = round(df['education'].value_counts().sum()-higher_education,1)

    # percentage with salary >50K
    t=df[['education','salary']].value_counts()[['Bachelors','Masters','Doctorate']]
    share_higher_rich=t.loc[['Bachelors','Masters','Doctorate'], '>50K'].sum()/t.sum()
    higher_education_rich = round(share_higher_rich*100,1)

    t=df[~df['education'].isin(['Bachelors','Masters','Doctorate'])]
  
    t=t[['education','salary']].value_counts()
    share_lower_rich=t.loc(axis=0)[:, '>50K'].sum()/t.sum()
    lower_education_rich = round(share_lower_rich*100,1)

    # What is the minimum number of hours a person works per week (hours-per-week feature)?
    min_work_hours = df['hours-per-week'].min()

    # What percentage of the people who work the minimum number of hours per week have a salary of >50K?
    df_min_hours=df[df['hours-per-week']==min_work_hours]
    num_min_workers = df_min_hours['salary'].value_counts().sum()

    rich_percentage =  num_min_workers_share=df_min_hours['salary'].value_counts()['>50K']*100/num_min_workers

    # What country has the highest percentage of people that earn >50K?
    country_salary=df[['native-country','salary']].value_counts()
    dict_percentage_country={'percentage':[],'country':[]}
    rich_workers=country_salary.loc[:,'>50K']
    poor_workers=country_salary.loc[:,'<=50K']
    for index1 in rich_workers.index:
      for index2 in poor_workers.index:
        if index1==index2:
          calcul=rich_workers.loc[index1]*100/(rich_workers.loc[index1]+poor_workers.loc[index2])
          dict_percentage_country['percentage'].append(calcul)
          dict_percentage_country['country'].append(index1)
    max_percentage=np.array(dict_percentage_country['percentage']).max()
    idx=dict_percentage_country['percentage'].index(max_percentage)

    highest_earning_country = dict_percentage_country['country'][idx]
    highest_earning_country_percentage = round(max_percentage,1)

    # Identify the most popular occupation for those who earn >50K in India.
    activities=df[(df['native-country']=='India') & (df['salary']=='>50K')]['occupation'].value_counts()
    top_IN_occupation = activities.index[0]

    # DO NOT MODIFY BELOW THIS LINE

    if print_data:
        print("Number of each race:\n", race_count) 
        print("Average age of men:", average_age_men)
        print(f"Percentage with Bachelors degrees: {percentage_bachelors}%")
        print(f"Percentage with higher education that earn >50K: {higher_education_rich}%")
        print(f"Percentage without higher education that earn >50K: {lower_education_rich}%")
        print(f"Min work time: {min_work_hours} hours/week")
        print(f"Percentage of rich among those who work fewest hours: {rich_percentage}%")
        print("Country with highest percentage of rich:", highest_earning_country)
        print(f"Highest percentage of rich people in country: {highest_earning_country_percentage}%")
        print("Top occupations in India:", top_IN_occupation)

    return {
        'race_count': race_count,
        'average_age_men': average_age_men,
        'percentage_bachelors': percentage_bachelors,
        'higher_education_rich': higher_education_rich,
        'lower_education_rich': lower_education_rich,
        'min_work_hours': min_work_hours,
        'rich_percentage': rich_percentage,
        'highest_earning_country': highest_earning_country,
        'highest_earning_country_percentage':
        highest_earning_country_percentage,
        'top_IN_occupation': top_IN_occupation
    }