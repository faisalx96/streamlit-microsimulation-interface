import streamlit as st
import time
import random
import threading
from utils.openai_client import get_population_projection

def show_ui():
    if st.session_state.get('generating_projection', False):
        show_chatgpt_dialog(st.session_state.user_prompt)
    else:
        with st.sidebar.expander("Custom Scenarios", expanded=False):
            user_prompt = st.text_area("Enter scenario details:", height=100)
            generate_button = st.button("Generate Projection")

        if generate_button:
            if not user_prompt:
                st.sidebar.warning("Please enter scenario details.")
            else:
                st.session_state.generating_projection = True
                st.session_state.user_prompt = user_prompt
                st.rerun()

def show_chatgpt_dialog(user_prompt):
    with st.spinner("Generating population projection..."):
        progress_bar = st.progress(0)
        year_display = st.empty()
        status_display = st.empty()
        thread_result = {"df": None, "completed": False, "error": None}

        def api_call():
            try:
                thread_result["df"] = get_population_projection(user_prompt)
            except Exception as e:
                thread_result["error"] = str(e)
            finally:
                thread_result["completed"] = True

        api_thread = threading.Thread(target=api_call)
        api_thread.start()

        simulate_progress(progress_bar, year_display)

        api_thread.join()

        if thread_result["error"]:
            st.error(f"Failed to generate projection: {thread_result['error']}")
        elif thread_result["df"] is not None:
            st.session_state.generated_df = thread_result["df"]
            year_display.success("Projection completed!")
            progress_bar.progress(1.0)
            time.sleep(1)
        else:
            st.error("Failed to generate projection. Please try again.")

    st.session_state.generating_projection = False
    if 'user_prompt' in st.session_state:
        del st.session_state.user_prompt
    st.rerun()

def simulate_progress(progress_bar, year_display):
    start_year, end_year = 2024, 2100
    total_years = end_year - start_year
    base_wait = 0.4
    max_variation = 0.1

    for i in range(total_years):
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