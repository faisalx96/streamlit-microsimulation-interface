import json
import re
import pandas as pd
import streamlit as st
from openai import OpenAI
import yaml
import os

def load_config():
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config.yaml')
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    return config

config = load_config()
client = OpenAI(api_key=config['openai_api_key'])

def get_population_projection(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system",
                 "content": "You are an AI that generates population projection data for Saudi Arabia. Respond with a JSON string containing a list of dictionaries, each with 'Year' and 'Population' keys. The 'Population' key must be number that starts at 19.5 million in 2024."},
                {"role": "user",
                 "content": f"Generate a population projection from 2024 to 2100 based on this scenario: {prompt}"}
            ]
        )
        res = response.choices[0].message.content
        json_str = re.sub(r'```json\s*|\s*```', '', res)
        data = json.loads(json_str)

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