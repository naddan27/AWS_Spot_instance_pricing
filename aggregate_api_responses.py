import os
import pandas as pd
import numpy as np
from datetime import date

headers = ["Feature", "Availability Region", "Instance", "Operating System", "Price", "Time"]
all_files = os.listdir("./api_responses")
dfs = [pd.read_csv("./api_responses/" + x, delimiter = "\t", names = headers) for x in all_files]

def get_average_spot_price_per_availability_region(df):
    availability_regions = np.unique(df["Availability Region"])
    availability_regions.sort()
    
    instance, region = df["Availability Region"][0][:-1], df["Instance"][0]
    zones, average_prices = [], []
    for x in availability_regions:
        subset = df[df["Availability Region"] == x]
        average_price = np.mean(subset["Price"])
        zones.append(x[-1])
        average_prices.append(average_price)
    return [instance, region, zones, average_prices, np.mean(average_prices)]

def build_df(information):
    unique_instances = np.unique([x[1] for x in information])
    
    data = []
    for unique_instance in unique_instances:
        elements_with_instance = [x for x in information if x[1] == unique_instance]
        
        for el in elements_with_instance:
            specific_instance = el[1]
            specific_region = el[0]
            
            for i, (az, p) in enumerate(zip(el[2], el[3])):
                if i == 0:
                    data.append([specific_instance, specific_region, az, round(p, 3), round(el[4], 3)])
                else:
                    data.append([specific_instance, specific_region, az, round(p, 3), ""])
    
    data = np.array(data)
    remove_repeats(data)
    
    return pd.DataFrame(data = data, columns = ["Instance", "Region", "Availability Zone", "Average Price", "Average Price Across Zones"])

def remove_repeats(array):
    for i in range(2):
        column = array[:, i]
        new_column = []
        
        old_value = "filler"
        for x in column:
            if x == old_value:
                new_column.append("")
            else:
                new_column.append(x)
                old_value = x
        array[:,i] = new_column

information = [get_average_spot_price_per_availability_region(x) for x in dfs]
summary = build_df(information)
today = date.today()
today_str = today.strftime("%m_%d_%Y")
summary.to_csv("./cost_summary_" + today_str + ".csv")