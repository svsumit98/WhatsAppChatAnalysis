import re
import pandas as pd


def preprocess(data):
    # Pattern to match date-time strings
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'

    # Extract messages and dates
    message = re.split(pattern, data)[1:]  # Skip the first invalid split
    dates = re.findall(pattern, data)

    # Ensure matching length
    if len(message) != len(dates):
        raise ValueError("Mismatch between extracted dates and messages.")

    # Create DataFrame
    df = pd.DataFrame({'user_message': message, 'date': dates})

    # Parse dates
    try:
        df['date'] = pd.to_datetime(df['date'], format='%m/%d/%y, %H:%M - ', errors='coerce')
    except Exception as e:
        print(f"Date parsing error: {e}")
        return pd.DataFrame()  # Return empty DataFrame on failure

    # Filter out rows with invalid dates
    df = df.dropna(subset=['date'])

    # Split user messages into user and message
    users = []
    messages = []
    for msg in df['user_message']:
        entry = re.split(r'([\w\W]+?):\s', msg, maxsplit=1)
        if len(entry) > 1:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)

    # Add additional date components
    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    period=[]
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period']=period

    return df
