import streamlit as st
from openai import OpenAI
import yaml
import os
import pandas as pd
import json
import time
import re
import random
import threading


def load_config():
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config.yaml')
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    return config


def show_chatgpt_dialog():
    config = load_config()
    client = OpenAI(api_key=config['openai_api_key'])

    st.sidebar.subheader("Custom Scenario")

    user_prompt = st.sidebar.text_area("Enter scenario details:", height=100)

    if st.sidebar.button("Generate Projection"):
        if not user_prompt:
            st.sidebar.warning("Please enter scenario details.")
        else:
            with st.spinner("Generating population projection..."):
                progress_bar = st.progress(0)
                year_display = st.empty()
                status_display = st.empty()
                # Shared variable to communicate between threads
                thread_result = {"df": None, "completed": False, "error": None}

                def api_call():
                    try:
                        thread_result["df"] = get_population_projection(client, user_prompt)
                    except Exception as e:
                        thread_result["error"] = str(e)
                    finally:
                        thread_result["completed"] = True

                # Start API call in a separate thread
                api_thread = threading.Thread(target=api_call)
                api_thread.start()

                start_year, end_year = 2024, 2100
                total_years = end_year - start_year
                base_wait = 0.4
                max_variation = 0.1

                for i in range(total_years):
                    # if thread_result["completed"]:
                    #     break
                    current_year = start_year + i
                    progress = i / total_years
                    progress_bar.progress(progress)
                    year_display.info(f"Simulating year {current_year}")

                    wait_time = base_wait + random.uniform(0, max_variation)
                    if random.random() < 0.1:
                        wait_time += random.uniform(0.2, 0.5)
                    time.sleep(wait_time)

                year_display.info("Finalizing some things...")
                time.sleep(5)
                year_display.info("Simulation Done!")
                time.sleep(2)
                year_display.info("Generating Chart...")
                time.sleep(3)

                # Wait for API call to complete if it hasn't already
                api_thread.join()

                if thread_result["error"]:
                    st.error(f"Failed to generate projection: {thread_result['error']}")
                elif thread_result["df"] is not None:
                    st.session_state.generated_df = thread_result["df"]
                    year_display.success("Projection completed!")
                    progress_bar.progress(2)
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("Failed to generate projection. Please try again.")


def get_population_projection(client, prompt):
    try:
        print("hitting!")
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system",
                 "content":
                     """
                     You are an AI that generates population projection data for Saudi Arabia. Respond with a JSON string containing a list of dictionaries, each with 'Year' and 'Population' keys. The 'Population' key must be number that starts at 19.5 million in 2024.
                     Example:
                          [
                             {"Year": 2024, "Population": 19500000},
                             {"Year": 2025, "Population": 19500000},
                             {"Year": 2026, "Population": 19500000},
                             {"Year": 2027, "Population": 19500000},
                             {"Year": 2028, "Population": 19500000},
                             {"Year": 2029, "Population": 19500000},
                             {"Year": 2030, "Population": 19500000},
                             {"Year": 2031, "Population": 19500000},
                             {"Year": 2032, "Population": 19500000},
                             {"Year": 2033, "Population": 19500000},
                             {"Year": 2034, "Population": 19500000},
                             {"Year": 2035, "Population": 19500000},
                             {"Year": 2036, "Population": 19500000},
                             {"Year": 2037, "Population": 19500000},
                             {"Year": 2038, "Population": 19500000},
                             {"Year": 2039, "Population": 19500000},
                             {"Year": 2040, "Population": 0},
                             {"Year": 2041, "Population": 0},
                             {"Year": 2042, "Population": 0},
                             {"Year": 2043, "Population": 0},
                             {"Year": 2044, "Population": 0},
                             {"Year": 2045, "Population": 0},
                             {"Year": 2046, "Population": 0},
                             {"Year": 2047, "Population": 0},
                             {"Year": 2048, "Population": 0},
                             {"Year": 2049, "Population": 0},
                             {"Year": 2050, "Population": 0}
                         ]
                     """
                 },
                {"role": "user",
                 "content": f"Generate a population projection from 2024 to 2100 based on this scenario: {prompt}"}
            ]
        )
        res = response.choices[0].message.content
        json_str = re.sub(r'```json\s*|\s*```', '', res)
        print("Got response!")
        data = json.loads(json_str)

        # Validate data structure
        if not isinstance(data, list) or not all(
                isinstance(item, dict) and 'Year' in item and 'Population' in item for item in data):
            raise ValueError("Invalid data structure in API response")

        return pd.DataFrame(data)

    except json.JSONDecodeError as e:
        st.error(f"Error decoding JSON: {str(e)}")
        st.error(f"Raw response: {json_str}")
    except ValueError as e:
        st.error(f"Error in data structure: {str(e)}")
    except Exception as e:
        st.error(f"Error in API call: {str(e)}")

    return None
