import pandas as pd
import scipy.stats
import streamlit as st
import time

# Initialize stateful variables
if 'experiment_no' not in st.session_state:
    st.session_state['experiment_no'] = 0

if 'df_experiment_results' not in st.session_state:
    st.session_state['df_experiment_results'] = pd.DataFrame(columns=['no', 'iterations', 'mean'])

st.header('Tossing a Coin')

# Create a placeholder for the chart
chart_placeholder = st.empty()

def toss_coin(n):
    # Simulate coin tosses
    trial_outcomes = scipy.stats.bernoulli.rvs(p=0.5, size=n)

    mean = None
    outcome_no = 0
    outcome_1_count = 0

    # Update the chart in real-time
    for r in trial_outcomes:
        outcome_no += 1
        if r == 1:
            outcome_1_count += 1
        mean = outcome_1_count / outcome_no
        chart_placeholder.line_chart([mean])
        time.sleep(0.05)

    return mean

# User input for number of trials
number_of_trials = st.slider('Number of trials?', 1, 1000, 10)
start_button = st.button('Run')

if start_button:
    st.write(f'Running the experiment of {number_of_trials} trials.')
    st.session_state['experiment_no'] += 1
    mean = toss_coin(number_of_trials)
    
    # Append the results to the DataFrame
    st.session_state['df_experiment_results'] = pd.concat([
        st.session_state['df_experiment_results'],
        pd.DataFrame(data=[[st.session_state['experiment_no'], number_of_trials, mean]],
                     columns=['no', 'iterations', 'mean'])
    ], ignore_index=True)

# Display the DataFrame with experiment results
st.write(st.session_state['df_experiment_results'])
