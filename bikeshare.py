import pandas as pd

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('See data for: chicago / new york city / washington\n').lower()
    while city != 'chicago' and city != 'new york city' and city != 'washington':
        print('Enter a valid city name')
        city = input('Would you like to see data for: chicago / new york city / washington\n').lower()

    # get user input for month (all, january, february, ... , june)
    month = input('Filter the data by: month (type january or february or march or april or may or june) / all (for no filter)\n').lower()
    while month != 'january' and month != 'february' and month != 'march' and month != 'april' and month != 'may' and month != 'june' and month != 'all':
        print('Enter a valid month name')
        month = input('Filter the data by: month (type january or february or march or april or may or june) / all (for no filter)\n').lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('Filter the data by: day (type monday or tuesday or wednesday or thursday or friday or saturday or sunday) / all (for no filter)\n').lower()
    while day != 'monday' and day != 'tuesday' and day != 'wednesday' and day != 'thursday' and day != 'friday' and day != 'saturday' and day != 'sunday' and day != 'all':
        print('Enter a valid day name')
        day = input('Filter the data by: day (type monday or tuesday or wednesday or thursday or friday or saturday or sunday) / all (for no filter)\n').lower()

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

    # convert the Start Time and End Time columns to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    # extract month and day of week and hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
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

    # display the most common month
    popular_month = df['month'].mode()[0]
    print('Most Popular month:', popular_month)

    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print('Most Popular day of week:', popular_day)

    # display the most common start hour
    popular_hour = df['hour'].mode()[0]
    print('Most Popular Start Hour:', popular_hour)

    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('Most Popular Start Station:', popular_start_station)

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('Most Popular End Station:', popular_end_station)

    # display most frequent combination of start station and end station trip
    # by creating a new 'trip' column which is composed by the 'Start Station' and the 'End Station' strings attached with 'to' in between
    df['trip'] = df['Start Station'] +' to '+ df['End Station']
    popular_trip = df['trip'].mode()[0]
    print('Most Popular trip:', popular_trip)

    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    #creates a new 'travel_time' column which is the 'End Time' column less the 'Start Time' column
    df['travel_time'] = df['End Time'] - df['Start Time']

    # display total travel time
    print('Total travel time:', df['travel_time'].sum())

    # display mean travel time
    print('Mean travel time:', df['travel_time'].mean())

    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('Display counts of user types:\n', user_types,'\n')

    # Display counts of gender
    x = 'Gender' in df
    if x == False:
        print('Gender not available for washington')
    else:
        gender_types = df['Gender'].value_counts()
        print('Display counts of gender:\n', gender_types,'\n')

    # Display earliest, most recent, and most common year of birth
    y = 'Birth Year' in df
    if y == False:
        print('Year of birth not available for washington')
    else:
        print('Earliest year of birth:', df['Birth Year'].min())
        print('Most recent year of birth:', df['Birth Year'].max())
        print('Most common year of birth:', df['Birth Year'].mode()[0])

    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)


        raw_data = input('\nWould you like to see 5 lines of raw data? Enter yes or no.\n')
        number_of_lines = 5
        while raw_data.lower() == 'yes':
            print(df.head(number_of_lines))
            number_of_lines += 5
            raw_data = input('\nWould you like to see 5 lines of raw data? Enter yes or no.\n')

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
