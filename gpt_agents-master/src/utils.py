import os
import datetime 
import pandas as pd 

# def check_existing_file(path_exp, expmnt_num, feedback, instruction_type, temperature, memory, n_steps, n_agents, gpt_model):
#     temp_str = temp_str = str(temperature).replace('.', '-')
#     gpt_str = str(gpt_model).replace('.', '-')
#     file_name = f"expmnt_results_{feedback}_{instruction_type}_num_{expmnt_num}_temp_{temp_str}_memory_{memory}_ntime_{n_steps}_nagents_{n_agents}_model_{gpt_str}.csv"
#     file_path = os.path.join(path_exp, file_name)

#     # Check if the file exists
#     if os.path.exists(file_path):
#         print(f"File {file_name} already exists.")
#         # Increase exp_number 
#         # TODO do this recursively to guarantee there is not overlap
#         expmnt_num += 1
#         print(f"Changing experiment number to {expmnt_num}, double check this is okay")
#         return expmnt_num
#     else:
#         print(f"File {file_name} does not exist. Safe to proceed.")
#         return expmnt_num

def check_existing_file(path_exp, expmnt_num, feedback, instruction_type, temperature, memory, n_steps, n_agents, gpt_model):
    # Convert the base directory to an absolute path
    path_exp = os.path.abspath(path_exp)
    print(f"Checking files in absolute path: {path_exp}")
    
    # Sanitize parameters for the filename
    temp_str = str(temperature).replace('.', '-')
    gpt_str = str(gpt_model).replace('.', '-')
    
    # Construct the filename and its absolute path
    file_name = f"expmnt_results_{feedback}_{instruction_type}_num_{expmnt_num}_temp_{temp_str}_memory_{memory}_ntime_{n_steps}_nagents_{n_agents}_model_{gpt_str}.csv"
    file_path = os.path.join(path_exp, file_name)

    # Check if the file exists
    print(f"Looking for file: {file_path}")
    if os.path.exists(file_path):
        print(f"File {file_name} already exists.")
        expmnt_num += 1
        print(f"Changing experiment number to {expmnt_num}, double check this is okay.")
        return expmnt_num
    else:
        print(f"File {file_name} does not exist. Safe to proceed with experiment number {expmnt_num}.")
        return expmnt_num

def create_batch_folder(persona, base_path="../results/experiments/"):
    """Creates a single folder for storing a batch of experiments."""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")  # Unique batch ID
    batch_folder = os.path.join(base_path, f"experiment_batch_{timestamp}_{persona.replace(' ', '_')}")  # Persona in filename
    
    if not os.path.exists(batch_folder):
        os.makedirs(batch_folder)
        print(f"Created batch experiment folder: {batch_folder}")
    
    return batch_folder  # Return the path for use in multiple experiments

def consolidate_experiment_results(folder_path, output_file):
    all_data = []

    # Normalize the folder path to avoid mix of slashes
    folder_path = os.path.abspath(folder_path)

    for file in os.listdir(folder_path):
        if file.endswith(".csv"):
            file_path = os.path.join(folder_path, file)
            try:
                df = pd.read_csv(file_path)  # Read CSV instead of Excel

                # Debugging step: Print columns found
                print(f"\nReading file: {file_path}")  # Ensure correct file path
                print("Columns in file:", df.columns.tolist())

                # Ensure necessary columns exist
                required_columns = {'time_step', 'agent_id', 'predicted_price', 'actual_price'}
                if not required_columns.issubset(df.columns):
                    print(f"Skipping {file}: Missing required columns")
                    continue  # Skip this file

                all_data.append(df[['time_step', 'agent_id', 'predicted_price', 'actual_price']])

            except Exception as e:
                print(f"Error reading {file_path}: {e}")

    
    if all_data:
        combined_df = pd.concat(all_data, ignore_index = True)

        # Group by time_step and agent_id to compute the mean per agent per time step across experiments
        final_summary = combined_df.groupby(["time_step", "agent_id"]).agg(
            mean_predicted_price=('predicted_price', 'mean'),
            mean_actual_price=('actual_price', 'mean')
        ).reset_index()

        output_file = os.path.join(folder_path, output_file)

        final_summary.to_csv(output_file, index = False)
        print(f"Consolidated data saved to {output_file}")
    else: 
        print("No valid data found")


def consolidate_experiment_variance(folder_path, output_file):
    """
    Reads through all CSV files in a folder and consolidates the variance of predicted price 
    and actual price for each time step per agent across all experiments.
    
    Parameters:
    folder_path (str): Path to the folder containing the CSV files.
    output_file (str): Name of the output file to save results.
    """
    all_data = []

    # Normalize the folder path to avoid mix of slashes
    folder_path = os.path.abspath(folder_path)

    for file in os.listdir(folder_path):
        if file.endswith(".csv"):
            file_path = os.path.join(folder_path, file)
            try:
                df = pd.read_csv(file_path)  # Read CSV

                # Debugging step: Print columns found
                print(f"\nReading file: {file_path}")  # Ensure correct file path
                print("Columns in file:", df.columns.tolist())

                # Ensure necessary columns exist
                required_columns = {'time_step', 'agent_id', 'predicted_price', 'actual_price'}
                if not required_columns.issubset(df.columns):
                    print(f"Skipping {file}: Missing required columns")
                    continue  # Skip this file

                all_data.append(df[['time_step', 'agent_id', 'predicted_price', 'actual_price']])

            except Exception as e:
                print(f"Error reading {file_path}: {e}")

    if all_data:
        combined_df = pd.concat(all_data, ignore_index=True)

        # Group by time_step and agent_id to compute variance per agent per time step
        final_summary = combined_df.groupby(["time_step", "agent_id"]).agg(
            variance_predicted_price=('predicted_price', 'var'),
            variance_actual_price=('actual_price', 'var')
        ).reset_index()

        output_path = os.path.join(folder_path, output_file)

        final_summary.to_csv(output_path, index=False)
        print(f"Variance data saved to {output_path}")
    else:
        print("No valid data found")
