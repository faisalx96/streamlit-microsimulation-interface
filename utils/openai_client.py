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
                 "content": """
                 You are an AI that generates population projection data for Saudi Arabia.
                 Respond with a JSON string containing a list of dictionaries, each with 'Year' and 'Population' keys.
                 The 'Population' key must be number that starts at 19 million in 2024.
                 
                 This is the baseline population projection that you should alter:
                 Year     Population
                2024  19000000
                2025  19406030
                2026  19714210
                2027  20011560
                2028  20311190
                2029  20616900
                2030  20907790
                2031  21194120
                2032  21461070
                2033  21754620
                2034  22014350
                2035  22296500
                2036  22555850
                2037  22823940
                2038  23088990
                2039  23361640
                2040  23613580
                2041  23882620
                2042  24126960
                2043  24351920
                2044  24582960
                2045  24839650
                2046  25068410
                2047  25286530
                2048  25519470
                2049  25735880
                2050  25949820
                2051  26153690
                2052  26369150
                2053  26558580
                2054  26740600
                2055  26927940
                2056  27112050
                2057  27285900
                2058  27465070
                2059  27630180
                2060  27786930
                2061  27935510
                2062  28060150
                2063  28189160
                2064  28311710
                2065  28427420
                2066  28535530
                2067  28638130
                2068  28767520
                2069  28874870
                2070  28965310
                2071  29039600
                2072  29118450
                2073  29208510
                2074  29279950
                2075  29344550
                2076  29400790
                2077  29433280
                2078  29491230
                2079  29554310
                2080  29591740
                2081  29652540
                2082  29716380
                2083  29774140
                2084  29830570
                2085  29893270
                2086  29935260
                2087  29962810
                2088  30003090
                2089  30062750
                2090  30112340
                2091  30153190
                2092  30181880
                2093  30228240
                2094  30253700
                2095  30283150
                2096  30294930
                2097  30315450
                2098  30325330
                2099  30321150
                2100  30023040
                 """},
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