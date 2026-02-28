# diabetesPredictionModel.py

import modelFunctions

modelFunctions.clear_screen(2)
print("\nWelcome to the Diabetes Prediction Model!\n")

# step 1: load the data from a csv file
try:
    filename = modelFunctions.ask_for_filename()
    header, data = modelFunctions.load_csv(filename)
except FileNotFoundError:
    print("\nFile not found. Please make sure the file exists and is accessible.")
    exit(1)
    
print("\nColumns:", header)
print("\nFirst row:", data[0])
print("\nTotal rows:", len(data))

# step 2: separate x and y variable
y_index = modelFunctions.ask_for_y_index(header)
x_data, y_data = modelFunctions.separate_x_y(data, y_index)
print("\nFirst row of x_data:", x_data[0])
print("\nFirst value of y_data:", y_data[0])

# step 3: handle missing values (if any) 
# user will decide if (1) replace missing values with the median of the respective column 
# OR (2) remove the row with missing values
missing_handling_choice = modelFunctions.ask_for_missing_value_handling()
if missing_handling_choice == '1':
    x_data = modelFunctions.replace_missing_with_median(x_data)
elif missing_handling_choice == '2':
    x_data, y_data = modelFunctions.remove_rows_with_missing_values(x_data, y_data)


modelFunctions.clear_screen(2)
print("Preparing the data for computation...")
modelFunctions.clear_screen(2)
print("Data preparation completed!\n")

# clear the screen before moving to the next step
modelFunctions.clear_screen(1)


# step 4: computation
# 4.1 get the mean of each column in x_data as well as the y variable
x_means, y_mean = modelFunctions.compute_means(x_data, y_data)
# 4.2 compute for x - xmean and y - ymean
x_deviation, y_deviation = modelFunctions.compute_deviations(x_data, y_data, x_means, y_mean)
# 4.3 compute for the product of x_deviation and y_deviation
product_deviation = modelFunctions.compute_product_of_deviations(x_deviation, y_deviation)
# 4.4 compute for the square of x_deviation
squared_x_deviation = modelFunctions.compute_squared_x_deviation(x_deviation)
# 4.5 compute for the sum of product_deviation and squared_x_deviation
sum_product, sum_squared_x = modelFunctions.compute_sums(product_deviation, squared_x_deviation)
# 4.6 compute for the slope (m) and intercept (y)
slope, intercept = modelFunctions.compute_slope_intercept(sum_product, sum_squared_x, x_means, y_mean)
# 4.7 compute for the overall y-intercept
overall_intercept = modelFunctions.compute_overall_intercept(slope, x_means, y_mean)


modelFunctions.clear_screen(2)
print("Computing the model parameters...")
modelFunctions.clear_screen(2)
print("Computing the slopes and intercepts...")
modelFunctions.clear_screen(2)
print("Computing the overall intercept...")
modelFunctions.clear_screen(2)
print("Computation completed!")

# save slopes
timestamp = modelFunctions.generate_timestamp()
modelFunctions.save_slopes(slope, overall_intercept, header, y_index, timestamp)

# save training results
modelFunctions.save_training_results(x_data, y_data, slope, overall_intercept, header, y_index, timestamp)



# clear the screen before moving to the next step
print("\nModel training completed! Proceed with testing")
modelFunctions.clear_screen(1)


# step 5: test the model with new data
while True:
    x_row, result = modelFunctions.test_model_with_new_data(slope, overall_intercept, header)
    if x_row is not None:
        modelFunctions.save_test_result(header, x_row, result, timestamp)
    
    modelFunctions.clear_screen(2)
    again = input("\nDo you want to test another set of data? (y/n): ")
    if again.lower() != 'y':
        print("\nTerminating Program!")
        break

