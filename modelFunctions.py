#FUNCTION DEFINITIONS


# function no.1
# load csv source into the program 
def load_csv(filename):
    data = []
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    header = lines[0].strip().split(',')
    
    for line in lines[1:]:
        values = line.strip().split(',')
        row = [float(v) for v in values]
        data.append(row)
    
    return header, data



# function no.2
# ask for the filename of the csv file to load
def ask_for_filename():
    filename = input("\nEnter the filename of the Historical Data to load: ")
    filename = filename.strip() 
    filename = filename + '.csv' if not filename.endswith('.csv') else filename
    return filename



# function no. 3
# separate x and y variable
def separate_x_y(data, y_index):
    x_data = []
    y_data = []
    for row in data:
        x_row = row[:y_index] + row[y_index+1:]
        x_data.append(x_row)
        y_data.append(row[y_index])
    return x_data, y_data



# function no. 4
# ask for the index of the y variable 
def ask_for_y_index(header):
    print("\nColumns:")
    for i, col in enumerate(header):
        print(f"{i}: {col}")
    y_index = int(input("Enter the index of the independent variable (y): "))
    return y_index




# function no. 5
# replace missing values with the median of the respective column
# remove rows with missing values
def get_column(x_data, col_index):
    return [row[col_index] for row in x_data]

def compute_median(column):
    sorted_col = sorted(column)
    n = len(sorted_col)
    mid = n // 2
    if n % 2 == 0:
        return (sorted_col[mid - 1] + sorted_col[mid]) / 2
    else:
        return sorted_col[mid]

def replace_missing_with_median(x_data):
    num_features = len(x_data[0])
    for j in range(num_features):
        column = get_column(x_data, j)
        # treat 0 as missing for this dataset
        non_zero = [v for v in column if v != 0]
        median = compute_median(non_zero)
        for i in range(len(x_data)):
            if x_data[i][j] == 0:
                x_data[i][j] = median
    return x_data

def remove_rows_with_missing_values(x_data, y_data):
    cleaned_x = []
    cleaned_y = []
    for i in range(len(x_data)):
        if 0 not in x_data[i]:
            cleaned_x.append(x_data[i])
            cleaned_y.append(y_data[i])
    return cleaned_x, cleaned_y



# function no. 6
# ask user how to handle missing values
def ask_for_missing_value_handling():
    print("\nHow would you like to handle missing values?")
    print("1: Replace missing values with the median of the respective column")
    print("2: Remove rows with missing values")
    choice = input("Enter your choice (1 or 2): ")
    return choice


import time
# function no. 7
# wait for user input and clear the screen before moving to the next step
def clear_screen(num):
    import os
    if num == 1:
        if os.name == 'nt':
            input("Press Enter to continue...")
            os.system('cls')
        else:        
            input("Press Enter to continue...")
            os.system('clear') 
    if num == 2:
        if os.name == 'nt':
            time.sleep(1)
            os.system('cls')
        else:        
            os.system('clear')    

    
        
# function no. 8
# compute the mean of each column in x_data as well as the y variable
def compute_means(x_data, y_data):
    n = len(x_data)
    num_features = len(x_data[0])
    
    x_means = []
    for j in range(num_features):
        col_sum = 0
        for i in range(n):
            col_sum += x_data[i][j]
        x_means.append(col_sum / n)
    
    y_mean = sum(y_data) / n
    
    return x_means, y_mean



# function no. 9
# compute for x - x_mean and y - y_mean
def compute_deviations(x_data, y_data, x_means, y_mean):
    n = len(x_data)
    num_features = len(x_data[0])

    x_deviation = []
    for i in range(n):
        row = []
        for j in range(num_features):
            row.append(x_data[i][j] - x_means[j])
        x_deviation.append(row)

    y_deviation = [y_data[i] - y_mean for i in range(n)]

    return x_deviation, y_deviation



# function no. 10
# compute for the product of x_deviation and y_deviation (x - x_mean) * (y - y_mean)
def compute_product_of_deviations(x_deviation, y_deviation):
    n = len(x_deviation)
    num_features = len(x_deviation[0])

    product_deviation = []
    for i in range(n):
        row = []
        for j in range(num_features):
            row.append(x_deviation[i][j] * y_deviation[i])
        product_deviation.append(row)

    return product_deviation



# function no. 11
# compute for the square of x_deviation (x - x_mean)^2
def compute_squared_x_deviation(x_deviation):
    n = len(x_deviation)
    num_features = len(x_deviation[0])

    squared_x_deviation = []
    for i in range(n):
        row = []
        for j in range(num_features):
            row.append(x_deviation[i][j] ** 2)
        squared_x_deviation.append(row)

    return squared_x_deviation



# function no. 12
# compute for the sum of product_deviation and squared_x_deviation
def compute_sums(product_deviation, squared_x_deviation):
    num_features = len(product_deviation[0])

    sum_product = []
    sum_squared_x = []

    for j in range(num_features):
        col_sum_product = 0
        col_sum_squared = 0
        for i in range(len(product_deviation)):
            col_sum_product += product_deviation[i][j]
            col_sum_squared += squared_x_deviation[i][j]
        sum_product.append(col_sum_product)
        sum_squared_x.append(col_sum_squared)

    return sum_product, sum_squared_x



# function no. 13
# compute for the slope (m) and intercept (y)
# m = sum(x - x_mean)(y - y_mean) / sum(x - x_mean)^2
def compute_slope_intercept(sum_product, sum_squared_x, x_means, y_mean):
    num_features = len(sum_product)

    slope = []
    intercept = []
    for j in range(num_features):
        m = sum_product[j] / sum_squared_x[j]
        b = y_mean - (m * x_means[j])
        slope.append(m)
        intercept.append(b)

    return slope, intercept



# function no. 14
# compute for the overall y-intercept
# b = y_mean - (m1*x_mean1 + m2*x_mean2 + ... + mn*x_meann)
def compute_overall_intercept(slope, x_means, y_mean):
    total = 0
    for j in range(len(slope)):
        total += slope[j] * x_means[j]
    overall_intercept = y_mean - total
    return overall_intercept



# function no. 15
# test the model with new data
# print out all the columns and ask user to input values for each column 
def predict(x_row, slope, overall_intercept):
    y_pred = overall_intercept
    for j in range(len(slope)):
        y_pred += slope[j] * x_row[j]
    if y_pred >= 0.5:
        return 1
    else:
        return 0
    
def print_result(result):
    print("\nPrediction Result")
    if result == 1:
        print("  Prediction: WITH Diabetes (1)\n\n")
    else:
        print("  Prediction: NO Diabetes (0)\n\n")

def test_manual(slope, overall_intercept, header):
    print("\nEnter the following values for the patient:")
    x_row = []
    for i in range(len(slope)):
        value = float(input(f"  {header[i]}: "))
        x_row.append(value)
    result = predict(x_row, slope, overall_intercept)
    print_result(result)
    return x_row, result  # return so it can be saved

def test_from_csv(slope, overall_intercept, header):
    filename = input("Enter the CSV filename to load test data from: ")
    filename = filename.strip()
    filename = filename + '.csv' if not filename.endswith('.csv') else filename
    try:
        _, data = load_csv(filename)
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
        return None, None
    
    time.sleep(1)
    print(f"\nFound {len(data)} row(s) in '{filename}'. Running predictions...\n")
    all_rows = []
    all_results = []
    for i, x_row in enumerate(data):
        if len(x_row) > len(slope):
            x_row = x_row[:len(slope)]
        result = predict(x_row, slope, overall_intercept)
        time.sleep(0.5)
        print(f"  Row {i+1}: {x_row}")
        print_result(result)
        all_rows.append(x_row)
        all_results.append(result)
        print()
    return all_rows, all_results  # return all rows and results

def test_model_with_new_data(slope, overall_intercept, header):
    clear_screen(2)
    print("\n--- Test the Model with New Data ---")
    print("  [1] Manually type in values")
    print("  [2] Load from an existing CSV file")
    choice = input("Enter your choice (1 or 2): ")
    if choice == '1':
        return test_manual(slope, overall_intercept, header)
    elif choice == '2':
        return test_from_csv(slope, overall_intercept, header)
    else:
        print("Invalid choice.")
        return None, None


    
# function no. 16
# ask user if they want to save the test results to a csv file
def save_test_result(header, x_row, result, timestamp):
    save_choice = input("\nDo you want to save this test result? (y/n): ")
    if save_choice.lower() != 'y':
        return

    base_name = input("\nEnter the base name for the results file (e.g., diabetes_model): ")
    base_name = base_name.strip().replace(' ', '_')
    result_filename = f"{base_name}_results_{timestamp}.csv"

    try:
        with open(result_filename, 'r') as f:
            write_header = False
    except FileNotFoundError:
        write_header = True

    with open(result_filename, 'a') as f:
        if write_header:
            # use first row to determine number of columns
            first_row = x_row[0] if isinstance(x_row[0], list) else x_row
            col_headers = ','.join(header[:len(first_row)]) + ',Prediction\n'
            f.write(col_headers)

        # handle both single row and list of rows
        if isinstance(x_row[0], list):
            for row, res in zip(x_row, result):
                row_values = ','.join([str(v) for v in row]) + f',{res}\n'
                f.write(row_values)
        else:
            row_values = ','.join([str(v) for v in x_row]) + f',{result}\n'
            f.write(row_values)

    print(f"Result saved to '{result_filename}' successfully!")
    
    
def generate_timestamp():
    import time
    t = time.localtime()
    return f"{t.tm_year}{t.tm_mon:02}{t.tm_mday:02}_{t.tm_hour:02}{t.tm_min:02}{t.tm_sec:02}"



# function no. 17
# save feature slopes to csv
def save_slopes(slope, overall_intercept, header, y_index, timestamp):
    save_choice = input("\nDo you want to save the slopes? (y/n): ")
    if save_choice.lower() != 'y':
        return

    base_name = input("Enter a base name for the files (e.g., diabetes_model): ")
    base_name = base_name.strip().replace(' ', '_')

    filename = f"{base_name}_feature_slopes_{timestamp}.csv"

    x_headers = [header[j] for j in range(len(header)) if j != y_index]
    with open(filename, 'w') as f:
        f.write("Feature,Slope\n")
        for j in range(len(slope)):
            f.write(f"{x_headers[j]},{slope[j]}\n")
        f.write(f"Overall Intercept,{overall_intercept}\n")

    print(f"Feature slopes saved to '{filename}' successfully!")
    
    
# function no. 18
# save training results to csv
# runs the model against all training rows and saves actual vs predicted
def save_training_results(x_data, y_data, slope, overall_intercept, header, y_index, timestamp):
    save_choice = input("\nDo you want to save the training results? (y/n): ")
    if save_choice.lower() != 'y':
        return

    base_name = input("Enter the base name for the files (e.g., diabetes_model): ")
    base_name = base_name.strip().replace(' ', '_')

    filename = f"{base_name}_training_results_{timestamp}.csv"

    with open(filename, 'w') as f:
        # write header
        x_headers = [header[j] for j in range(len(header)) if j != y_index]
        col_headers = ','.join(x_headers) + ',Actual,Predicted\n'
        f.write(col_headers)

        # write each row with actual and predicted
        correct = 0
        for i in range(len(x_data)):
            predicted = predict(x_data[i], slope, overall_intercept)
            actual = int(y_data[i])
            if predicted == actual:
                correct += 1
            row_values = ','.join([str(v) for v in x_data[i]])
            f.write(f"{row_values},{actual},{predicted}\n")

    accuracy = (correct / len(x_data)) * 100
    print(f"Training results saved to '{filename}' successfully!")
    print(f"  Model Accuracy on Training Data: {accuracy:.2f}%")
