import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import matplotlib.animation as animation

## Load sea level data
df = pd.read_csv(r"C:\Users\amali\OneDrive - Aalborg Universitet\semester 6\data\data_til_Amalie.csv")

# Rename column to 'idk6' if it was previously named differently
df = df.rename(columns={'value': 'idk6'})
df['idk6'] = pd.to_numeric(df['idk6'], errors='coerce')
df['year'] = pd.to_numeric(df['year'], errors='coerce')
df.dropna(inplace=True)  # Drop rows with NaNs

# Forecast based on feelings the next 8 years
def simple_forecast(df, increase=1.2, years=8):
    data = df.to_dict('records')
    last_year = data[-1]['year']
    last_value = data[-1]['idk6']
    for i in range(1, years + 1):
        data.append({'year': last_year + i, 'idk6': last_value * increase ** i})
    return pd.DataFrame(data)

df = simple_forecast(df)

# Find indices of max and third highest values
max_value_index = df['idk6'].idxmax()
max_value = df.loc[max_value_index, 'idk6']

# To find the third highest value, sort and select appropriately
sorted_indices = df['idk6'].sort_values(ascending=False).index
third_highest_index = sorted_indices[3]  # Zero-based index; [2] is third element
third_highest_value = df.loc[third_highest_index, 'idk6']

# Create scatter plot
fig, ax = plt.subplots()
scatter = ax.scatter(df['year'], df['idk6'])

# Set x-label and y-label
ax.set_xlabel('Year')
ax.set_ylabel('Change in °C from 1951-1980 baseline ')

# Setup annotation box for the highest value
image_path = r"C:\Users\amali\OneDrive - Aalborg Universitet\semester 6\data\we are fucked.jpg"
image = plt.imread(image_path)
imagebox = OffsetImage(image, zoom=0.2)
ab_max = AnnotationBbox(imagebox, (df.loc[max_value_index, 'year'], max_value),
                        xybox=(50., 50.),
                        xycoords='data',
                        boxcoords="offset points",
                        pad=0.5,
                        arrowprops=dict(arrowstyle="->"))
ab_max.set_visible(False)

# Setup annotation box for the third highest value
image_path_1 = r"C:\Users\amali\OneDrive - Aalborg Universitet\semester 6\data\its_getting_hot.png"
image_1 = plt.imread(image_path_1)
imagebox_1 = OffsetImage(image_1, zoom=0.2)
ab_third_highest = AnnotationBbox(imagebox_1, (df.loc[third_highest_index, 'year'], third_highest_value),
                                  xybox=(-50., 50.),
                                  xycoords='data',
                                  boxcoords="offset points",
                                  pad=0.5,
                                  arrowprops=dict(arrowstyle="->"))
ab_third_highest.set_visible(False)

# Hover function to show annotation on mouseover
def hover(event):
    vis_max = ab_max.get_visible()
    vis_third = ab_third_highest.get_visible()
    if event.inaxes == ax:
        cont, ind = scatter.contains(event)
        if cont:
            index = ind['ind'][0]
            if index == max_value_index:
                ab_max.set_visible(True)
                ax.add_artist(ab_max)
            else:
                ab_max.set_visible(False)
            
            if index == third_highest_index:
                ab_third_highest.set_visible(True)
                ax.add_artist(ab_third_highest)
            else:
                ab_third_highest.set_visible(False)
                
            fig.canvas.draw_idle()
        else:
            if vis_max:
                ab_max.set_visible(False)
            if vis_third:
                ab_third_highest.set_visible(False)
            fig.canvas.draw_idle()

# Connect the hover event
fig.canvas.mpl_connect('motion_notify_event', hover)

# Show the plot
plt.show()
