import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

months = ['january', 'february', 'march', 'april', 'may', 'june']
weekdays = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

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
        try:
            city = str(input('\nWould you want to see the data for Chicago, New York City, Washington or all? Please type:\n')).lower()
            if city in CITY_DATA.keys(): 
                print('Alright! You chose {}.\n'.format(city.capitalize()))
                break
            else:                
                print('Invalid input. Please choose between Chicago, New York City, Washington or all\n')
        except KeyboardInterrupt:
            print('\nInput terminated by user\n')
            break
                     
                  
    # TO DO: get user input for month (all, january .. june)     
    while True:
        try:
            month = str(input('Please choose a month between January and June or all to analyze: ')).lower()
            if month in months: 
                print('We will filter the data by the month {}.\n'.format(month.capitalize()))
                break
            elif month == 'all': 
                print('We will not filter the data by months\n')
                break
            else:
                print('Invalid input. Please choose a month between January and June or all')
        except KeyboardInterrupt:
            print('\nInput terminated by user')
            break   

    # TO DO: get user input for day of week (all, monday .. sunday)                   
    while True:
        try:
            day = str(input('Please choose a day of the week or all to analyze: ')).lower()
            if day in weekdays:
                print('{} will be the weekday in focus.\n'.format(day.capitalize()))
                break
            elif day == 'all':
                print('All weekdays will be checked\n')
                break
            else:
                print('Invalid input. Please choose a day of the week or all')
        except KeyboardInterrupt:
            print('\nInput terminated by user')
            break    

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
    
    df = pd.read_csv(CITY_DATA[city])        
    df['Start Time'] = pd.to_datetime(df['Start Time']) 
    
    df['month'] = df['Start Time'].dt.month
    if month != 'all':        
        month = months.index(month) + 1
        df = df[df['month'] == month]
    
    df['weekday'] = df['Start Time'].dt.weekday_name
    if day != 'all':
        df = df[df['weekday'] == day.title()]
    
    return df

def display_data(df):
    n = 0
    m = 5
        
    try:
        data = str(input('Do you want to see the first 5 lines of data? Type yes or no\n')).lower()
        print(df.iloc[n:m])
        while data != 'no':
            data = str(input('Do you want to see the next 5 lines of data? Type yes or no\n')).lower()
            if data == 'yes':
                n += 5
                m += 5                
                if m > len(df.index):
                    print('No more data to display\n')
                    break
                else:
                    print(df.iloc[n:m])
            else:
                print('Answer not recognized. Please type yes or no\n')
    except KeyboardInterrupt:
        print('\nInput terminated by user')              

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    popular_month = df['month'].mode()[0]
    print(months[popular_month - 1].capitalize() + ' is the most common month.\n')

    # TO DO: display the most common day of week
    popular_day = df['weekday'].mode()[0]
    print(popular_day + ' is the most common weekday.\n')

    # TO DO: display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print(str(popular_hour) + ' is the most common start hour.\n')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    popular_startstat = df['Start Station'].mode()[0]
    print(popular_startstat + ' is the most common start station.\n')

    # TO DO: display most commonly used end station
    popular_endstat = df.groupby(["End Station"]).size().sort_values(ascending=False).idxmax()
    print(popular_endstat + ' is the most common end station.\n')

    # TO DO: display most frequent combination of start station and end station trip
    sorted_trip = df.groupby(["Start Station", "End Station"]).size().sort_values(ascending=False).idxmax()
    print(sorted_trip[0] + ' to ' + sorted_trip[1] + ' is the most frequent trip.\n')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time    
    time_total = df['Trip Duration'].sum()
    year = time_total // 31536000
    day = (time_total - (year * 31536000)) // 86400
    hour = (time_total - ((year * 31536000) + (day * 86400))) // 3600
    minute = (time_total - ((year * 31536000) + (day * 86400) + (hour * 3600))) // 60
    second = time_total - ((year * 31536000) + (day * 86400) + (hour * 3600) + (minute * 60))
    print('Total travel time is\n' + str(year) + ' years\n' + str(day) + ' days\n' + str(hour) + ' hours\n' + str(minute) + ' minutes\n' + str(second) + ' seconds\n')
    
    # TO DO: display mean travel time
    time_mean = df['Trip Duration'].mean()
    minute = time_mean // 60
    second = time_mean - (minute * 60)
    print('The mean travel time is approximately\n' + str(int(minute)) + ' minutes\n' + str(int(second)) + ' seconds\n')    #converting to int and then to str to avoid decimals

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    utypes = df.groupby(['User Type'])['User Type'].count()
    print('Following the count of each ' + str(utypes) + '\n')

    # TO DO: Display counts of gender
    gtypes = df.groupby(['Gender'])['Gender'].count()
    print('Following the count of each ' + str(gtypes) + '\n')

    # TO DO: Display earliest, most recent, and most common year of birth
    yob_oldest = df['Birth Year'].min()
    yob_youngest = df['Birth Year'].min()
    yob_common = df['Birth Year'].mode()[0]
    print('The earliest year of birth is ' + str(int(yob_oldest)) + '\nThe most recent year of birth is ' + str(int(yob_youngest)) + '\nThe most common year of birth is ' + str(int(yob_common)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        
        display_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
