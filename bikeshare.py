import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

cities_list = ['chicago', 'new york', 'washington']

months_list = ['all', 'january', 'february', 'march', 'april', 'may', 'june']

days_list = ['all', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday' ]

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('Enter Name of the city to filter: (chicago, new york , washington) \n> ').lower()
        if city in cities_list:
            break
        else:
            print('Invalid data')

    # TO DO: get user input for month (all, january, february, ... , june)
    while True:
        month = input('Enter Month to filter: (all, january, february, ... , june) \n> ').lower()
        if month in months_list:
            break
        else:
            print('Invalid data')

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input('Enter day of week to filter: (all, monday, tuesday, ... sunday) \n>').lower()
        if day in days_list:
            break
        else:
            print('Invalid data')
   
    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    
    # filter by month if applicable
    if month != 'all':
        month = months_list.index(month) + 1
    
    # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month = df['month'].mode()[0]
    print('Most Common Month is :', most_common_month)


    # display the most common day of week
    most_common_day_of_week = df['day_of_week'].mode()[0]
    print('Most Common Day is :', most_common_day_of_week)


    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    most_common_start_hour = df['hour'].mode()[0]
    print('Most Common Hour is:', most_common_start_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_station = df['Start Station'].value_counts().idxmax()
    print('Most Commonly used start station is:', start_station)


    # display most commonly used end station
    end_station = df['End Station'].value_counts().idxmax()
    print('Most Commonly used end station is:', end_station)


    # display most frequent combination of start station and end station trip
    frequent_station_combination = df.groupby(['Start Station', 'End Station']).count()
    print('Most Commonly used combination of start station and end station trip:', start_station, " & ", end_station)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
      
    # Converting seconds to readable format(y:d:h:m:s)
    def convertSectoDay(n):  
        year = n//(24 * 3600 * 365)
        n = n % (24 * 3600 * 365)
        day = n // (24 * 3600) 
        n = n % (24 * 3600) 
        hour = n // 3600
        n %= 3600
        minutes = n // 60
        n %= 60
        seconds = n 
        print(year,"years", day,"days", hour, "hours", minutes, "minutes", seconds, "seconds") 
        
    # display total travel time
    total_travel = df['Trip Duration'].sum()
    print("Total travel time:")
    convertSectoDay(total_travel)

    # display mean travel time
    mean_travel = df['Trip Duration'].mean()
    print("\nMean travel time:")
    convertSectoDay(mean_travel)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type_count = df['User Type'].value_counts()
    print('User Types:\n',user_type_count)

    # Display counts of gender
    if 'Gender' in df.columns:
        gender_count = df['Gender'].value_counts()
        print('\nGender Counts:\n',gender_count)

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest = df['Birth Year'].min()
        print("\nEarliest year of birth: ", earliest)
        most_recent = df['Birth Year'].max()
        print("Most recent year of birth: ", most_recent)
        most_common = df['Birth Year'].mode()[0]
        print("Most common year of birth: ", most_common)
       
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def main():
    while True:
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