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
    