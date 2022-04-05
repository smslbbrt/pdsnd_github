import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

cities = ['chicago','new york city','washington']
months = ['january', 'february', 'march', 'april', 'may', 'june','all']
days = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday','all']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\n Hello! Let\'s explore some US bikeshare data!\n')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city=''
    #collect and check if input is valid
    while city not in cities:
        city= input('Enter the city you would like to explore, options are Chicago, New York City or Washington. You can enter "all" if you want to analyse all the cities: ').lower()
        if city not in cities:
            print ('\nThe city you indentified does not appear in the data. Please check and re-enter the city')
        else:
            print('\nOK let\'s have a look at data for {}\n'.format(city.title()))

    # get user input for month (all, january, february, ... , june)
    month = ''
    #collect and check if input is valid
    while month not in months:
        month= input('January to June data is availabile. Please enter the name of the month you would like to analyse. You can enter "all" if you want to analyse all the data: ').lower()
        if month not in months:
            print('\nThe month you indicated does not appear in the data.')
        else:
            print('\nOK let\'s have a look at data for {}\n'.format(month.title()))


    # get user input for day of week (all, monday, tuesday, ... sunday)
    day=''
    #collect and check if input is valid
    while day not in days:
        day=input('Please enter the name of day of the week that you would like to analyse, or "all" to apply no day filter: ').lower()
        if day not in days:
            print('\nThe value entered is not valid. Please check the spelling and try again' )
        else:
            print('\nOK let\'s have a look at data for {}\n\n'.format(day.title()))


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

    # extract month and day of week from Start Time and create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int of the month
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    """Args:
        bikeshare dataframe
    Returns:
        none"""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    month_ind= ['January', 'February', 'March', 'April', 'May', 'June']
    month_val= int(df['Start Time'].dt.month.mode())
    common_month =  month_ind[month_val - 1]
    print('\n Most common month for rental is: {} '.format(common_month))


    # display the most common day of week
    common_day=df['day_of_week'].mode()[0]
    print('\n Most popular weekday for rental is: {} '.format(common_day.title()))

    # display the most common start hour
    df['hour']=df['Start Time'].dt.hour
    common_hour=df['hour'].mode()[0]
    print('\n Most frequent hour for rental is: {}:00 '.format(common_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    """Args:
        bikeshare dataframe
    Returns:
        none"""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station=df['Start Station'].mode()[0]
    start_station_count= df['Start Station'].value_counts().mode()
    print('\nMost common Starting Station is: {}'.format(common_start_station))

    # display most commonly used end station
    common_end_station=df['End Station'].mode()[0]
    end_station_count=df['End Station'].value_counts().mode()
    print('\nMost common end station is: {}'.format(common_end_station))

    # display most frequent combination of start station and end station trip
    # create the most commin trip by combining start and end stations
    common_trip=df['Start Station'] + ' to ' + df['End Station']

    # look for the most common trip
    most_common_trip=common_trip.mode()[0]
    trip_count=common_trip.value_counts()
    print('\nThe most frequent combination of stations are: {}'.format(most_common_trip))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    """Args:
        bikeshare dataframe
    Returns:
        none"""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    #calculates the trip duration
    trip_time = df['Trip Duration'].sum()
    # breaks the trip duration down in years, months, weeks, days, hours, minutes and seconds
    minutes, seconds = divmod(trip_time,60)
    hours, minutes = divmod(minutes,60)
    day_r, hours =  divmod(hours,24)
    weeks, day_r = divmod(day_r,7)
    month_r, weeks = divmod(weeks,4)
    year, month_r = divmod(month_r,12)

    if year > 1:
        print('\nThe total trip time for the selected data is: {} years, {} months, {} weeks, {} days, {} hours, {} minutes and {} seconds'.format(year, month_r, weeks, day_r, hours, minutes, seconds))
    elif month_r >1:
        print('\nThe total trip time for the selected data is: {} months, {} weeks, {} days, {} hours, {} minutes and {} seconds'.format(month_r, weeks, day_r, hours, minutes, seconds))
    elif weeks >1:
        print('\nThe total trip time for the selected data is: {} weeks, {} days, {} hours, {} minutes and {} seconds'.format(weeks, day_r, hours, minutes, seconds))
    elif day_r >1:
        print('\nThe total trip time for the selected data is: {} days, {} hours, {} minutes and {} seconds'.format(day_r, hours, minutes, seconds))
    else:
        print('\nThe total trip time for the selected data is: {} hours, {} minutes and {} seconds'.format(hours, minutes, seconds))

    # display mean travel time
    #calculates the trip duration
    mean_trip = round(df['Trip Duration'].mean())
    # breaks the mean trip duration down in hours, minutes and seconds
    m, s = divmod(mean_trip,60)
    if m > 60:
        min_mean, s_mean = divmod(mean_trip,60)
        h_mean, min_mean = divmod(min_mean,60)
        print('\nThe mean travel time for the selcetd data is: {} hours, {} minutes and {} seconds'.format(h_mean, min_mean, sec_mean))
    else:
        min_mean, sec_mean = divmod(mean_trip,60)
        print('\nThe mean travel time for the selcetd data is: {} minutes and {} seconds'.format(min_mean, sec_mean))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    """Args:
        bikeshare dataframe
    Returns:
        none"""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('\nThe number of user types are as follows: \n{}'.format(user_types))

    """no gender date captured in washington data error handler"""
    try:
        #retrive gender counts
        gender_type = df['Gender'] .value_counts()
        #retrive earliest birth year
        earliest_birth = int(df['Birth Year'].min())
        #retrive most recent birh year
        latest_birth = int(df['Birth Year'].max())
        #retrive common birt year
        common_birth = int(df['Birth Year'].mode()[0])

    except KeyError:
        #print error message
        print('\nThe Washington data does not contain information on Gender or Year of Birth')

    else:
        # Display counts of gender
        print('\nThe gender profile for the selected data are: \n{}' .format(gender_type))

        # Display earliest, most recent, and most common year of birth
        print('\nThe earliest recorded Year of Birth is: {}' .format(earliest_birth))
        print('\nThe most recent recorded Year of Birth is: {}' .format(latest_birth))
        print('\nThe most common reocorded Year of Birth is: {}' .format(common_birth))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def raw_data(df):
    """Allows user to display five rows of data from the selected csv file"""

    """Args:
        bikeshare dataframe
    Returns:
        none"""
    # print header and first file rows of data

    print(df.head())
    rows = 0
    #checks with user if more data is required and display next five rows, if not required then break.
    while True:
        more_data = input('\nWould you like to view the next five rows of raw data? Enter yes or no.\n')
        if more_data.lower()!='yes':
           break
        rows = rows + 5
        print(df.iloc[rows:rows+5])



def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        while True:
            view_data = input('\nWould you like to view the raw data? Data will be displayed five rows at a time. Enter yes or no.\n')
            if view_data.lower() !='yes':
               break
            raw_data(df)
            break

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()




"""Sources used to complete this project:

to count frequency
https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.value_counts.html

to concat to fields in DataFrame
https://www.datasciencemadesimple.com/concatenate-two-columns-dataframe-pandas-python-2/#:~:text=Concatenating%20two%20columns%20of%20the%20dataframe%20in%20pandas,columns%20of%20dataframe%20in%20pandas%20%28two%20string%20columns%29

to calculate travel times
https://docs.python.org/3/library/functions.html#divmod
https://www.w3schools.com/python/ref_func_divmod.asp#:~:text=Python%20divmod%20%28%29%20Function%201%20Definition%20and%20Usage.,by%20argument2%20%28divisor%29.%202%20Syntax%203%20Parameter%20Values

to print rows of dataframe
https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.iloc.html?highlight=iloc#pandas.DataFrame.iloc
https://pythonguides.com/get-first-n-rows-of-pandas-dataframe/"""
