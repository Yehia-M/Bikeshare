import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

months = ['jan','feb','mar','apr','may','jun','all']
days   = ['saturday','sunday','monday','tuesday','wednesday','thursday','friday','all']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    city_flag = True
    month_flag = True
    day_flag = True

    print('\nHello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while city_flag:
        city = input("\nChoose a city from (Chicago - New York - Washington):\n")
        if city.lower() in CITY_DATA:
            city_flag = False
        else:
            print("\nError: Enter one of the three cities")

    # get user input for month (all, january, february, ... , june)
    while month_flag:
        month = input("\nEnter the month in the same format as (Jan - Feb - Mar - Apr - May - Jun) or enter (all) to apply no month filter \n")
        if month.lower() in months:
            month_flag = False
        else:
            print("\nError: Enter the month in correct format")

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while day_flag:
        day = input("\nEnter the day of the week (Monday - Tuesday - ... - Sunday) or enter (all) to apply no day filter \n")
        if day.lower() in days:
            day_flag = False
        else:
            print("\nError: Enter the day again")

    print('-'*100)
    return city.lower(), month.lower(), day.lower()


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

    # extract hour, month and day of week from Start Time to create new columns
    df['hour'] = df['Start Time'].dt.hour
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.strftime("%A")

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = months.index(month) + 1
        # filter by month to create the new dataframe
        df = df.loc[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df.loc[df['day_of_week'] == day.title()]
    return df


def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if month == 'all':
        pop_month = df['month'].mode()[0]
    else:
        pop_month = month.title()
    print("\tThe most common month: \t\t{}".format(pop_month))

    # display the most common day of week
    if day == 'all':
        pop_day = df['day_of_week'].mode()[0]
    else:
        pop_day = day.title()
    print("\tThe most common day: \t\t{}".format(pop_day))

    # display the most common start hour
    popular_hour = df['hour'].mode()[0]
    print('\tThe most common start hour: \t{}\n'.format(popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('\tMost common start station: \t{}'.format(popular_start_station))

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('\tMost common end station: \t{}'.format(popular_end_station))

    # display most frequent combination of start station and end station trip
    popular_comb = (df['Start Station'] + ' => ' + df['End Station']).mode()[0]
    print('\tMost common combination: \t{}'.format(popular_comb))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_time = df['Trip Duration'].sum()
    #total_time = time_data.sum()
    print('\tTotal trip duration: \t\t{} seconds'.format(total_time))

    # display mean travel time
    mean_time = df['Trip Duration'].mean()
    print('\tMean of trip duration: \t\t{} seconds'.format(mean_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    number_of_users = df['User Type'].value_counts()
    print("Number of users : ")
    for idx in range(len(number_of_users)):
            users_no = number_of_users[idx]
            users_cat = number_of_users.index[idx]
            print("\tCategory {} - {} : \t{}".format(idx,users_cat,users_no))

    # Display counts of gender
    if city != 'washington':
        print("\nGender info : ")
        gender_info = df['Gender'].value_counts()
        for idx in range(len(gender_info)):
            users_no = gender_info[idx]
            users_cat = gender_info.index[idx]
            print("\t{} : \t{}".format(users_cat,users_no))

        print("\nBirth info : ")
        # Display earliest, most recent, and most common year of birth
        print("\tOldest Year of Birth: \t\t{}".format(int(df['Birth Year'].min())))
        print("\tMost Recent Year of Birth: \t{}".format(int(df['Birth Year'].max())))
        print("\tMost Common Year of Birth: \t{}".format(int(df['Birth Year'].mode()[0])))

    else:
        print("Gender and Birth info aren't available for this city")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def disp_5(df):
    disp_flag = True
    i = 0
    while disp_flag:
        user_in = input("Show 5 rows of raw data?: (Yes/No)\n")
        if user_in.lower() == 'yes' or user_in.lower() == 'y':
            print(df.iloc[i : i+ 5])
            i += 5
        else:
            disp_flag = False


def main():
    while True:
        city, month, day = get_filters()
        print("\t\tYou entered the following: City => {}, Month => {} and Day => {}".format(city.title(), month.title(), day.title()))
        print('-'*100)
        df = load_data(city, month, day)
        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
        disp_5(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
