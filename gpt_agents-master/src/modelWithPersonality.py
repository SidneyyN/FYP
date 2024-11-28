import numpy as np
import pandas as pd
import openai
from openai import OpenAI
import json
import time
import pickle
import re
from messages import *
import os 
import hashlib

############
# OpenAI keys
### WARNING be careful not to push to any public repository
############
#key_test = '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'
key_test = 'sk-pLu23M1BtVJzdLYkWsfl4GqVRXr9Ncv_TAoDyUxOm3T3BlbkFJHZ4YPGvXzsy1hUxC1HI-e4eMEqi3X3wnxNwQkZ54gA'

openai.api_key = key_test 

client = OpenAI(
    api_key=key_test
)

##############
# System rules
##############
def f_negative_feedback(pe,noise_mean,noise_sd, seed=None):
    if seed is not None:
        np.random.seed(seed)
    pe_mean = np.mean(pe)
    epsilon = np.random.normal(noise_mean,noise_sd)
    return 20/21*(123-pe_mean) + epsilon

def f_positive_feedback(pe,noise_mean,noise_sd, seed=None):
    if seed is not None:
        np.random.seed(seed)
    #print(f"Seed used in feedback function: {seed}")
    pe_mean = np.mean(pe)
    epsilon = np.random.normal(noise_mean,noise_sd)
    return 20/21*(pe_mean+3) + epsilon

def earnings(pe,p):
    return np.maximum(1300-1300/49*(pe-p)**2,0)/2600

def f_bubbles(pe,noise_mean=3,noise_sd=1/4, r=0.05, seed=None):
    if seed is not None:
        np.random.seed(seed)
    y = np.random.normal(noise_mean,noise_sd)
    R = 1 + r
    pe_mean = np.mean(pe) 
    return (1/R) * pe_mean + y/R


##############
# functions for running llm-agents
##############

def initialize_records(n_steps, n_agents, seed, feedback, instruction_type='original_30-50w', fw_up_message=None, random_start=None):
    '''Set experiment type according to feedback and instruction_type
    set random seeds and arrays/lists in which experiment information will be recorded
    set continue simulation = True
    Also sets random array of seeds for each agents
    '''
    np.random.seed(seed)

    # assign random personalities 
    personalities = np.random.choice(['optimistic', 'cautious', 'neutral'], size=n_agents)

    # Set experiment type
    if feedback == 'pos':
        # f = f_positive_feedback
        f = lambda pe, noise_mean, noise_sd: f_positive_feedback(pe, noise_mean, noise_sd, seed)
    elif feedback == 'neg':
        # f = f_negative_feedback
        f = lambda pe, noise_mean, noise_sd: f_negative_feedback(pe, noise_mean, noise_sd, seed)
    elif feedback == 'bub':
        # f = f_bubbles
        f = lambda pe, noise_mean=3, noise_sd=1/4, r=0.05: f_bubbles(pe, noise_mean, noise_sd, r)
    else:
        print('feedback should be pos or neg')
        
    messages_list = [] # list of each agent's messages 
    
    if instruction_type == 'original_30-50w' and feedback == 'pos':
        for personality in personalities:
            restart_messages = restart_messages_original_pos_personality(personality)
            messages_list.append(restart_messages)
        init_message = initial_message
        fw_up_message = follow_up_message
        if random_start:
            init_message = initial_message_random
    elif instruction_type == 'original_30-50w' and feedback == 'neg':
        restart_messages = restart_messages_original_neg
        init_message = initial_message
        fw_up_message = follow_up_message
        if random_start:
            init_message = initial_message_random
    elif instruction_type == 'original_30-50w' and feedback == 'bub':
        restart_messages = restart_messages_original_bubbles
        init_message = initial_message_bubbles
        fw_up_message = follow_up_message_bubbles
        if random_start:
            init_message = initial_message_bubbles_random
    elif instruction_type == 'prompteng':
        restart_messages = restart_messages_prompteng
                
    
    # set array and lists for recording experiment information    
    p_array = np.full(n_steps, np.nan)
    pe_agents_time_array = np.full((n_agents, n_steps), np.nan) # array of agent's predictions over time
    rewards_agents_time_array =  np.full((n_agents, n_steps), np.nan) # array of agent's rewards over time

    if feedback == 'bub':
        # for bubbles there is + 1 since two prices are predicted at the begining
        pe_agents_time_array = np.full((n_agents, n_steps + 1), np.nan)
    
    # get length of instructions
    instructions_len = len(messages_list[0])
    
    # set seed and bool
    np.random.seed(seed)
    continue_simulation = True 

    # set array of seeds for each agent
    seeds_array = np.random.randint(0, 100000, size=(n_agents, n_steps))
    
    return f, p_array, pe_agents_time_array, rewards_agents_time_array, messages_list, \
        init_message, fw_up_message, continue_simulation, instructions_len, seeds_array, personalities
    
def except_json(reply):
    ''' Check whether reply is in the right format if not ask llm to introduce another reply
    attempt record the number of attempts to avoid infinite loop
    '''
    error = 'no error'
    try:
        reply_dict = json.loads(reply)
        got_reply = True
        return reply_dict, got_reply, error
        
    except json.JSONDecodeError as e:
        # commented out if it can be fixed with re
        # print("Error decoding JSON:", e)
        match = re.search(r'\{.*\}', reply, re.DOTALL)
        if match:
            json_part = match.group()
            try:
                #print("Error solved with re")
                reply_dict = json.loads(json_part)
                got_reply = True
                return reply_dict, got_reply, error
                
            except json.JSONDecodeError as e2:
                print("Error decoding JSON part:", e2)
                print('reply', reply)
                print('type reply', type(reply))
               
                got_reply = False
                error = 'json'
                return '', got_reply, error
        else:
            print("No JSON found in the reply.")
           
            got_reply = False
            return '',  got_reply, error

    except Exception as e:
        # This block will catch any other exceptions
        print("error reading json:", e)
       
        error = 'json'
        got_reply = False
        return '', got_reply, error
    
def get_agent_reply_and_errors(agent_messages, new_message, temperature, seed_gpt, instructions_len, memory, gpt_model, prints_on=True):
    '''Feeds messages to ChatGPT and gets reply of agent. 
    If no reply, returns the type of error, either no error, json, or openai
    the latter refers to an excess of tokens
    instructions_len: amount of messages that correspond to the instructions
    memory: amoung of previous messages (excluding instructions) fed into the system
    '''

    
    if memory == 0:
        # zero memory treated differently since [-0:] is all list
        agent_remembered_messages = agent_messages[:instructions_len]
    # if less time steps than memory have passed give all messages
    # Notice we've removed instructions that should always be remembered
    elif len(agent_messages) - instructions_len <= memory:
        agent_remembered_messages = agent_messages[:]
    else:
        # remember instructions and the last 'memory' steps
        agent_remembered_messages = agent_messages[:instructions_len] \
        + agent_messages[- memory:]
    
    # add new message to both the full list and remembered ones
    agent_messages.append({"role": "user", "content": new_message})
    agent_remembered_messages.append({"role": "user", "content": new_message})
    if prints_on:
        print(agent_messages[-1])
    try:
        # if model accepts seeding, place seed
        if gpt_model == "gpt-4-1106-preview" or gpt_model == "gpt-3.5-turbo-1106" :
            chat_completion = client.chat.completions.create(
                model=gpt_model, 
                messages=agent_remembered_messages,
                temperature=temperature,
                response_format= { 'type': "json_object" },
                seed = int(seed_gpt)
            )
        else:
           chat_completion = client.chat.completions.create(
                model=gpt_model, 
                messages=agent_remembered_messages,
                temperature=temperature
            ) 
        reply = chat_completion.choices[0].message.content
        # add reply to messages (remembered ones are local so not needed)
        agent_messages.append({"role": "assistant", "content": reply})
        # Check answer is in right format, increase attempt otherwise
        reply_dict, got_reply, error = except_json(reply)

    except Exception as e:
        if prints_on:
            print("Error in chat completion:", e)
            print(gpt_model)
        if "Error code: 400" in str(e):
            error = 'tokens_limit'
        if "Error code: 429" in str(e):
            if "Please try again in 20s" in str(e):
                error = 'timeout_limit'
            if "Please try again in 7m12s" in str(e):
                error = 'timeout_limit_day'
            if 'Please try again in 5.202s' in str(e):
                error = 'timeout_limit_6'
            # if the below works then it should be general for any time limit
            elif 'Please try again in' in str(e):
                print('entered')
                print(e)
                match = re.search(r"Please try again in (\d+)m?(\d+\.\d+|\d+)s", str(e))
        
                if match:
                    print('match found')
                    minutes = match.group(1) if match.group(1) else "0"  # Ensure minutes is at least "0" if not found
                    seconds = match.group(2)  # Seconds part, could be decimal
                    
                    # Convert minutes to seconds and sum with the seconds part
                    total_seconds = (int(minutes) * 60) + float(seconds) + 1
                    print('wait', total_seconds)
                    error = f'timeout_limit_{total_seconds}'
                    time.sleep(total_seconds)
                else:
                    print(e)
                    print(re.search(r"Please try again in (\d+)m?(\d+\.\d+|\d+)s", str(e)))
                    error = 'timeout_limit_unknown'

            elif "name 're' is not defined" in str(e):
                print("error")

        elif "Object of type int64 is not JSON serializable" in str(e):
            print('fail chat completion', gpt_model)
            print("reply ", chat_completion.choices[0].message.content)
        
            
        got_reply = False
        reply_dict = ''
    
    return reply_dict, got_reply, error, agent_messages
            
def get_agent_reply(agent_messages, new_message, temperature, seed_gpt, continue_simulation, instructions_len, memory, gpt_model, \
                    new_message_json=new_message_json,prints_on=True,time_step=None,feedback=None):
    '''Calls get_agent_reply_and_errors and handles errors. If json error, asks for new reply
    if there is an error that is not json, but on timeout it will wait 20 seconds
    if the error is token limit then will stop simulation with  
    continue_simulation = False

    If all is good, it will return price, let simulation continue and updated agent_messages

    time_step and feedback are needed for bubbles
    '''
    # continue_simulation becomes false when an agent runs out of tokens or an agent exceed json attempts
    got_reply = False # becomes true when agent gives reply in json format
    
    attempt = 0 # attempts in getting a json format answer
    
    while continue_simulation == True and got_reply == False and attempt <= 3:
        
        reply_dict, got_reply, error, agent_messages \
            = get_agent_reply_and_errors(agent_messages, new_message, temperature, seed_gpt, \
                                         instructions_len, memory, gpt_model, prints_on=prints_on)
        
        if error == 'json':
            attempt += 1
            # NOTE watch out for bugs in overwritting this
            new_message = new_message_json
            
        elif error == 'tokens_limit':
            print('tokens exceeded, ending simulation')
            continue_simulation = False
            pe = None
        
        elif error == 'timeout_limit':
            print('timeout limit: waiting 20 seconds')
            time.sleep(20)

        elif error == 'timeout_limit_6':
            print('timeout limit: waiting 6 seconds')
            time.sleep(6)
            
        elif error == 'timeout_limit_day':
            print('timeout limit: waiting 7m12s seconds')
            time.sleep(433)
        elif error == 'timeout_limit_unknown':
            # wait 20s just to be sure
            time.sleep(20)

        elif 'timeout' in error:
            pass
        elif error == 'no error':
            pass
        else:
            print('different error')
            print(error)

            
        
    if got_reply:
        if feedback == 'bub' and time_step == 0:
            pe1 = float(reply_dict['predictedValue1'])
            pe2 = float(reply_dict['predictedValue2'])
            pe = [pe1, pe2]
            
        else:
            pe = float(reply_dict['predictedValue'])
        
        
    if attempt > 2:
        print("end simulation since an agent is not answering in JSON for more than 3 times")
        continue_simulation = False
        pe = None
    
    return pe, continue_simulation, agent_messages

def make_df_results(p_array, pe_agents_time, rewards_agents_time, personalities):
    ''' takes arrays with experiment data and makes a dataframe in long format
    '''
    n_steps = len(p_array)
    n_agents = pe_agents_time.shape[0]

    data = {
        'time_step': [],
        'agent_id': [],
        'predicted_price': [],
        'actual_price': [],
        'rewards': [],
        'personality': []
    }

    for t in range(n_steps):
        for agent in range(n_agents):
            data['time_step'].append(t)
            data['agent_id'].append(agent)
            data['predicted_price'].append(pe_agents_time[agent, t])
            data['actual_price'].append(p_array[t])
            data['rewards'].append(rewards_agents_time[agent, t])
            data['personality'].append(personalities[agent])

    return pd.DataFrame(data)

def ensure_directory_exists(path):
    # check if the directory exists 
    if not os.path.exists(path):
        # create directory if it doesn't exist
        os.makedirs(path)
        print(f"Directory created at {path}")
    else:
        print(f"Directory already exists at: {path}")

def save_results(df, messages_list, temperature, memory, feedback, instruction_type, expmnt_num, seed, \
                 n_steps, n_agents, gpt_model, path_exp):
    ''' take the dataframe in long format as well as message list and saves in csv and pkl files
    with names corresponding to information of the experiment
    # NOTE for now seed of gpt is passed as num (when seed can be given)
    '''
    # replace . with - for float variables (temp and gptmodel)
    temp_str = str(temperature).replace('.', '-')
    gpt_str = str(gpt_model).replace('.', '-')

    if gpt_model == "gpt-4-1106-preview" or gpt_model == "gpt-3.5-turbo-1106":
        #num = seed
        num = f"{expmnt_num}_seed_{seed}"
    else:
        num = expmnt_num
    
    # save csv with data
    ensure_directory_exists(path_exp)
    
    csv_filename = path_exp + 'expmnt_results_{}_{}_num_{}_temp_{}_memory_{}_ntime_{}_nagents_{}_model_{}.csv'\
        .format(feedback, instruction_type, num, temp_str, memory, n_steps, n_agents, gpt_str)
    
    #df.to_csv(csv_filename, index=False)

    try:
        df.to_csv(csv_filename, index=False)
        print(f"CSV saved successfully to {csv_filename}")
    except Exception as e:
        print(f"Error while saving CSV: {e}")
        raise
    
    # save messages in pkl file
    pickle_filename = path_exp + 'expmnt_messages_{}_{}_num_{}_temp_{}_memory_{}_ntime_{}_nagents_{}_model_{}.pkl'\
        .format(feedback, instruction_type, num, temp_str, memory, n_steps, n_agents, gpt_str)
    
    # with open(pickle_filename, 'wb') as file:
    #     pickle.dump(messages_list, file)

    try:
        with open(pickle_filename, 'wb') as f:
            pickle.dump(messages_list, f)
        print(f"Pickle file saved successfully to {pickle_filename}")
    except Exception as e:
        print(f"Error while saving pickle file: {e}")
        raise


    print(f"Saving pickle to: {pickle_filename}")

    # TODO save messaged in text file
    
#     # save agents responses in text
#     txt_filename = path_exp + 'expmnt_messages_{}_{}_num_{}_temp_{}_ntime_{}_nagents_{}.txt'\
#     .format(feedback, instruction_type, expmnt_num, temp_str, n_steps, n_agents)
    

#     with open(txt_filename, 'w') as file:
#         for message in messages:
#             file.write(str(message) + '\n')

def generate_fingerprint(params):
    params_string = str(params)
    return hashlib.md5(params_string.encode()).hexdigest()

def run_experiment(seed, expmnt_num, noise_mean, noise_sd, temperature, memory, gpt_model="gpt-3.5-turbo", n_steps=1, n_agents=1,
                   feedback='neg', instruction_type='original_30-50w', random_start=False, prints_on=True,\
                   save_res_bool=True, path_exp='../results/experiments/'):
    
    '''Function that puts everything together to run the experiment
    seed, expmnt_num are to track random variation due to system and gpt (note gpt cannot be seeded)
    # UPDATE now seed is also passed to gpt to seed it
    noise_mean(float), noise_sd(float) refer to the stochasticity of market
    temperature(float): is the temprature of the llm
    memory(int): number of time steps context (reasoning) is fed into model previous to t.s.
    n_steps(int), n_agents(int): number of time steps and agents
    feedback(str): market type
    instruction_type(str): type of instructions, including how many words the response is
    prints_on(boolean), save_res_bool(boolen):whehter we enable prints and save results
    path_exp(str): place where results are saved
    '''

    # Set the global seed for reproducibility
    np.random.seed(seed)

    # Generate fingerprint
    params = {
        "feedback": feedback,
        "n_agents": n_agents,
        "n_steps": n_steps,
        "noise_mean": noise_mean,
        "noise_sd": noise_sd,
        "seed": seed
    }
    fingerprint = generate_fingerprint(params)
    print("Experiment Fingerprints:", fingerprint)
   
    f, p_array, pe_agents_time, rewards_agents_time, \
    messages_list, initial_message, follow_up_message,\
    continue_simulation, instructions_len, seeds_array, personalities = initialize_records(n_steps, n_agents, \
                                            seed, feedback, instruction_type=instruction_type, random_start=random_start)

    for t in range(n_steps):
        pe_agents = np.full(n_agents, np.nan) # within time step agents prediction
        
        for i in range(n_agents):
            if prints_on:  print(f" \n Time: {t}, agent: {i}, personality: {personalities[i]} \n")
            seed_gpt = seeds_array[i, t]

            # Set the seed for agent-specific randomness
            # np.random.seed(seed_gpt)
            # print(f"Agent {i}, Time {t}: RNG State = {np.random.get_state()}")

            if t == 0:
                new_message = initial_message
            else:
                total_rewards = np.sum(rewards_agents_time[i, :t])
                # Format array info as a string so that numbers are separated by commas in text
                # include one more for bubbles
                if feedback == 'bub':
                    agent_predictions = ', '.join(map(str, pe_agents_time[i, :t + 1])) 
                else:
                    agent_predictions = ', '.join(map(str, pe_agents_time[i, :t])) 
                p_string = ', '.join(map(str, p_array[:t])) 
                
                # use the market information to give the follow-up message
                # NOTE time step is fed as t+1, since in instructions first time step is 1
                ## Here add if for bubbles and update bubble message
                if feedback == 'bub':
                    new_message = follow_up_message.format(t+1, str(p_array[t-1]), str(pe_agents_time[i, t-1]), p_string, agent_predictions, total_rewards)

                
                else:
                    new_message = follow_up_message.format(t+1, p_string, agent_predictions, total_rewards)
            
            agent_messages = messages_list[i] # get agents context
            
            # get agents's answer
            pe, continue_simulation, agent_messages = get_agent_reply(agent_messages, new_message, temperature, seed_gpt,\
                                                        continue_simulation, instructions_len, memory, gpt_model,\
                                                        new_message_json=new_message_json, prints_on=prints_on,time_step=t, feedback=feedback)
            messages_list[i] = agent_messages # this line might be redundant but jic

            if prints_on:
                print(agent_messages[-1])
            
            if continue_simulation == False: break

            # add information to arrays
            if feedback == 'bub':
                if t == 0:
                    pe_agents_time[i, t] = pe[0]
                    # Check with Cars it is indeed the +1
                    pe_agents_time[i, t + 1] = pe[1]
                    pe_agents[i] = pe[1]
                    ### Note this should be defined (q cars)
                    # pe_agents_prev[i] = pe[0]
                else:
                    pe_agents_time[i, t + 1] = pe
                    pe_agents[i] = pe
                    ### Note this should be defined (q cars)
                    # pe_agents_prev[i] = pe[0]
                    
            else:
                pe_agents[i] = pe
                pe_agents_time[i, t] = pe
           
        # Compute the current time step price according to agent predictions
        
        # p = np.round(f(pe_agents, noise_mean,noise_sd, seed=seed), 2)
        # Since f is now a lambda that includes the seed, the seed will be passed automatically when f is invoked.
        p = np.round(f(pe_agents, noise_mean, noise_sd), 2)
        #print(f"Feedback function result (p): {p}")
        p_array[t] = p

        # Calculate rewards and add it to each agent list
        # NOTE Ask cars? for bubbles should be -1?
        if feedback == 'bub':
            rewards = np.round(earnings(pe_agents, p), 2)
        else:
            rewards = np.round(earnings(pe_agents, p), 2)
        rewards_agents_time[:,t] = rewards # NOTE check dimensions
        
        #time.sleep(20)
        
    if save_res_bool:
        
        df = make_df_results(p_array, pe_agents_time, rewards_agents_time, personalities)
        if random_start:
            save_results(df, messages_list, temperature, memory, feedback, instruction_type + "randstart", expmnt_num, seed, \
                  n_steps, n_agents, gpt_model, path_exp) 
        else:
            save_results(df, messages_list, temperature, memory, feedback, instruction_type, expmnt_num, seed, \
                  n_steps, n_agents, gpt_model, path_exp)    

    return  p_array, pe_agents_time, rewards_agents_time, messages_list

