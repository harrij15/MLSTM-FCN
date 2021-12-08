import csv
import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('ggplot')

# Global variables
start_date = datetime.datetime(2000,6,1)
end_date = None

# Load CCHF alerts for country
def load_alerts():

    # Dictionary maps countries to dates
    alert_dict = dict()

    with open("CCHF - Total ProMED Archive.csv", encoding = 'utf-8') as csvfile:
        csvreader = csv.reader(csvfile)
        header = True
        for row in csvreader:
            if header:
                header = False
                continue

            country = row[2]
            coordinates = (int(row[3]),int(row[4]))
            date = datetime.datetime.strptime(row[8], '%Y-%m-%d %H:%M:%S')
            date = datetime.datetime(date.year,date.month,date.day)

            if country in alert_dict.keys():
                if coordinates in alert_dict[country].keys():
                    alert_dict[country][coordinates].append(date)
                else:
                    alert_dict[country][coordinates] = [date]
            else:
                alert_dict[country] = {coordinates: [date]}

    return alert_dict

def call_api(command):
    global start_date
    global end_date

    # Query NASA GES DISC database with authentication token
    token = ""

    if command == "temperature":
        data = "GLDAS_NOAH025_3H_2_1_Tair_f_inst"
    elif command == "precipitation":
        data = "GPM_3IMERGHH_06_precipitationCal"
    latitude = 30
    longitude = 69

    import copy
    time_start = copy.deepcopy(start_date)
    date_dict = dict()

    # Get around API limit by calling it one year at a time from start date
    while time_start < end_date:
        time_end = min(time_start + datetime.timedelta(days=365),end_date)

        headers = {
            'authorizationtoken': token,
        }

        params = (
            ('data', data),
            ('location', f'[{latitude},{longitude}]'),
            ('time', f'{time_start}/{time_end}'),
        )

        import requests
        response = requests.get('https://api.giovanni.earthdata.nasa.gov/timeseries', headers=headers, params=params)
        response = response.text.split('\n')[:-1]

        data_line = False
        for row in response:
            if 'Timestamp' in row:
                data_line = True
                continue

            if data_line:
                timestamp, value = row.split(',')

                date = timestamp.split(' ')[0].split('-')
                year, month, day = int(date[0]), date[1], date[2]

                if month[0] == '0':
                    month = int(date[1][1:])
                else:
                    month = int(date[1])

                if day[0] == '0':
                    day = int(date[2][1:])
                else:
                    day = int(date[2])

                date = datetime.datetime(year,month,day)

                if 'e' in value:
                    value = value.split('e')
                    value = float(value[0]) * pow(10,int(value[1][-1]))
                else:
                    value = int(value[0])

                if date in date_dict.keys():
                    date_dict[date].append(value)
                else:
                    date_dict[date] = [value]

        # Update start date
        time_start = time_end + datetime.timedelta(days=1)

    # Calculate averages
    for key in date_dict.keys():
        date_dict[key] = sum(date_dict[key])/len(date_dict[key])

    return date_dict

def create_binary_series(country_alerts):
    global start_date
    global end_date

    # Gather dates
    date_set = set()
    for location in country_alerts.keys():
        date_set = date_set.union(set(country_alerts[location]))
    alert_list = sorted(list(date_set))
    range_length = (alert_list[-1] - start_date).days

    # Generate date range
    date_range = [start_date + datetime.timedelta(days=x) for x in range(range_length+1)]
    end_date = date_range[-1]

    # Create binary series
    binary_series = []
    for date in date_range:
        binary_series.append((date,int(date in alert_list)))

    return binary_series

def generate_bar_chart(location_counts):
    import operator
    location_counts = sorted(location_counts,key=operator.itemgetter(0))
    locations = [x[0] for x in location_counts]
    counts = [x[1] for x in location_counts]
    location_pos = [i for i,_ in enumerate(locations)]

    plt.bar(location_pos, counts)
    plt.xlabel("Coordinates")
    plt.ylabel("Counts per Coordinate")
    plt.title("Coordinate Counts in Pakistan")
    plt.xticks(location_pos,locations)
    plt.show()

if __name__ == "__main__":

    # Gather alerts
    alerts = load_alerts()

    # Get stats for each country
    num_reports = dict()
    num_locations = dict()
    for country in alerts.keys():
        coordinates = alerts[country]
        num_locations[country] = len(coordinates.keys())

        report_cnt = 0
        for coordinate in coordinates.keys():
            report_cnt += len(coordinates[coordinate])
        num_reports[country] = report_cnt

    with open("Country Reports.csv","w",newline='') as report_file:
        csvwriter = csv.writer(report_file)
        csvwriter.writerow(["Country","Reports"])
        for country in num_reports.keys():
            csvwriter.writerow([country,num_reports[country]])

    with open("Country Locations.csv","w",newline='') as loc_file:
        csvwriter = csv.writer(loc_file)
        csvwriter.writerow(["Country","Locations"])
        for country in num_locations.keys():
            csvwriter.writerow([country,num_locations[country]])

    # Choose country
    country_alerts = alerts['Pakistan']

    # Get counts per location
    location_counts = []
    for key in country_alerts.keys():
        location_counts.append([key,len(country_alerts[key])])

    # Bounding box (Pakistan): (25, 66), (35, 66), (25, 73), (35, 73)
    # Center point and mode: (30, 69)
    # min x = 25, max x = 35, min y = 66, max y = 73

    # Bar charts of counts
    #generate_bar_chart(location_counts)
    with open("Reports per Location.csv","w",newline='') as loc_file:
        csvwriter = csv.writer(loc_file)
        csvwriter.writerow(["Location","Count"])
        for item in location_counts:
            location = item[0]
            count = item[1]
            csvwriter.writerow([location,count])

    # Construct time series of alerts
    binary_series = create_binary_series(country_alerts)

    # Plot binary series
    #plt.plot(binary_series)
    #plt.show()

    # Retrieve precipitation and temperature data
    temperatures = list(call_api("temperature").items())
    precipitation = list(call_api("precipitation").items())

    # Align date ranges
    end_date = min([binary_series[-1][0],temperatures[-1][0],precipitation[-1][0]])
    binary_series = [x for x in binary_series if x[0] <= end_date]
    temperatures = [x for x in temperatures if x[0] <= end_date]
    precipitation = [x for x in precipitation if x[0] <= end_date]

    assert(len(binary_series) == len(temperatures) and len(binary_series) == len(precipitation))

    # Build normal CSV
    import csv
    with open("data.csv","w",newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(["Date","Alert","Near Surface Air Temperature","Precipitation"])
        for i in range(len(binary_series)):
            date = binary_series[i][0].strftime("%m/%d/%Y")
            csvwriter.writerow([date,binary_series[i][1],temperatures[i][1],precipitation[i][1]])

    print("Done")




