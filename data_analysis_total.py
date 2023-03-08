import matplotlib.pyplot as plt
import numpy as np
import json


# Input the names of the users you would like to compare into this array, max of 5
USERS = ['User1', 'User2', 'User3', 'User4', 'User5']

with open('Data\\users_with_times.json', 'r') as f:
    raw_data = json.load(f)

def parse_time_data(name):
    data = raw_data[name]
    data = np.asarray(data, dtype=int)
    for i in range(len(data)):
        data[i] = int(data[i]/86400)
    return data

def get_message_data(data):
    messages = list(range(len(data)))
    messages = np.asarray(messages, dtype=int)
    for message in messages:
        message += 1
    return messages

def plot_data(name, x, y, color):
    plt.plot(x, y, label = name, color=color)

def calculate_fit_points(data, messages, degree, projection_length):
    coefficients = np.polyfit(data, messages, degree)
    x_fit = np.arange(0,projection_length, 0.5)
    slopes = coefficients[:-1]
    intercept = coefficients[-1]
    y_fit = []
    for x in x_fit:
        y_value = 0
        max_power = len(slopes)
        for i in range(len(slopes)):
            y_value += (x ** (max_power-i))*slopes[i]
        y_fit.append(y_value+intercept)
    return [x_fit, y_fit]

def plot_projection(name, fit, degree, color):
    plt.plot(fit[0], fit[1], '--', label = name+" ^"+str(degree)+" Projection", color=color)

def run(name, projection_length=1000, degrees=[1,2], color=(0,0,0,1)):
    data = parse_time_data(name)
    messages = get_message_data(data)
    plot_data(name, data, messages, color)
    for degree in degrees:
        color = (color[0], color[1], color[2], color[3]/3)
        plot_projection(name, calculate_fit_points(data, messages, degree, projection_length), degree, color)



colors = [(0,0,0,1),(0,0,1,1),(0,1,0,1),(1,0,0,1),(0.5,0.5,0,1)]

for i, user in enumerate(USERS):
    run(user, color=colors[i])


# Set the labels for the axes
plt.xlabel('Time from beginning of data (Days)')
plt.ylabel('Total Messages Sent')
plt.title('Telegram Data')

# add legend
plt.legend()

plt.xlim(0, 1000)
plt.ylim(0, 2500)

# display plot
plt.show()