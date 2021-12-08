import csv

def generate_week_string(week_data):
    output_str = ""
    for day in week_data:
        output_str += str(day) + "|"
    return output_str[:-1]

if __name__ == "__main__":

    # Retrieve data
    new_header = []
    x = []
    y = []
    with open("data.csv","r",newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        header = True
        for row in csvreader:
            if header:
                for i in range(2,len(row)):
                    x.append([])
                    new_header.append(row[i])
                new_header.append(row[1])
                header = False
                continue

            for i in range(2,len(row)):
                x[i-2].append(row[i])
            y.append(row[1])

    # Create weekly sequence data
    seq_data = []
    tw = 7
    for variable in x:
        sublist = []
        for i in range(len(variable)-7):
            sublist.append(variable[i:i+tw])
        seq_data.append(sublist)

    # Remove first week of y for consistency
    y = y[tw:]

    # Create dataset splits
    import numpy as np
    X_train, X_test, y_train, y_test = [], [], [], []
    split_index = int(len(seq_data[0])*0.7)
    for variable in seq_data:
        train, test = variable[:split_index+1], variable[split_index+1:]
        X_train.append(train)
        X_test.append(test)

    X_train = np.array(X_train).astype(float)
    X_test = np.array(X_test).astype(float)

    X_train = X_train.reshape(X_train.shape[1],X_train.shape[0],tw)
    X_test = X_test.reshape(X_test.shape[1],X_test.shape[0],tw)

    y_train, y_test = np.array(y[:split_index+1]).astype(int), np.array(y[split_index+1:]).astype(int)

    # Save .npy files for MALSTM-FCN
    path = "MALSTM-FCN/data/CCHF/"
    np.save(path + "X_train.npy",X_train)
    np.save(path + "X_test.npy",X_test)
    np.save(path + "y_train.npy",y_train)
    np.save(path + "y_test.npy",y_test)

    # Build time series CSV
    #tw = 7
    #with open("ts.csv","w",newline='') as csvfile:
        #csvwriter = csv.writer(csvfile)
        #csvwriter.writerow(new_header)
        #for i in range(tw,len(y)):

            ## Construct row
            #row = []
            #for variable in x:
                #week_data = variable[i-7:i]
                #week_str = generate_week_string(week_data)
                #row.append(week_str)
            #row.append(y[i])

            #csvwriter.writerow(row)

    print("Done")
