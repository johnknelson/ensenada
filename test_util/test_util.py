import numpy as np

def calculate_potential_gains(history_dataframe):
    # Grab just the costs
    dfToList = history_dataframe['open'].tolist()

    potential_gains = 0
    previous_price = dfToList[0];

    # Iterate through all opening prices starting with the second
    for opening_price in dfToList[1:]:
        difference = opening_price - previous_price
        if(difference > 0):
            potential_gains += difference
        previous_price = opening_price

    return potential_gains

# takes a numpy array
def add_to_ticker_history_np(history, value, history_length):
    # Add element
    appended_array = np.append(history, value)

    # If size is greater than desired history length, remove first element
    if (appended_array.size > history_length):
        np.delete(appended_array, 0)

    return appended_array

# takes a vanilla python array
def add_to_ticker_history(history, value, history_length):
    # Add element
    history.append(value)

    # If size is greater than desired history length, remove first element
    if (len(history) > history_length):
        history.pop(0)