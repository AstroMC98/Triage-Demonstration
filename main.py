# SmartPulse Triage MVP Front-End for Echelon Presentation
# Primary Developer : Marc Jerrone Castro (marc@intelligentai.solutions)

# Basic Python Libraries
import os
import re
import json
import time
import yaml
import base64
import random
import datetime
import requests
from yaml.loader import SafeLoader

# Analytics and Processing Libraries
import anthropic
import numpy as np
import pandas as pd


# Web-Application Related Libraries
from PIL import Image
import streamlit as st
import default_session_state as dss
from st_click_detector import click_detector

# Filepaths
import filepaths as fp

# Sections
import sections as sctn
import prompts

# Import SVGs
# import svgs_strings as svg_str

import re

def load_or_create_dataframe(file_path, columns = None):
    """
    Load a DataFrame from a file if it exists, or create one from provided data.
    
    Args:
    - file_path (str): The file path where the DataFrame is or will be saved.
    - data (dict or list of dicts, optional): Data to create a new DataFrame if the file doesn't exist.
    
    Returns:
    - pd.DataFrame: The loaded or created DataFrame.
    """
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
    else:
        df = pd.DataFrame(columns=columns)
        df.to_csv(file_path, index=False)
        
    df['Reference ID'] = df['Reference ID'].astype(str)
    return df

def update_dataframe(file_path, new_data, columns = None):
    """
    Update an existing DataFrame with new data from a dictionary.
    
    Args:
    - file_path (str): The file path where the DataFrame is saved.
    - new_data (dict): Dictionary containing the new row data.
    
    Returns:
    - pd.DataFrame: The updated DataFrame.
    """
    # Load the existing DataFrame (or create a new one if not present)
    df = load_or_create_dataframe(file_path, columns=columns)
    
    # Convert the new data into a DataFrame row and append it
    new_row = pd.DataFrame([new_data])
    df = pd.concat([df, new_row], ignore_index=True)
    
    # Save the updated DataFrame back to the file
    df.to_csv(file_path, index=False)
    
    return df

def extract_information(text):
    # Use regular expressions to find content between the <interpretation> and <triage> tags
    interpretation_match = re.search(r'<interpretation>(.*?)<\/interpretation>', text, re.DOTALL)
    triage_match = re.search(r'<triage>(.*?)<\/triage>', text, re.DOTALL)
    
    # Extracted values or None if not found
    interpretation = interpretation_match.group(1).strip() if interpretation_match else None
    triage = triage_match.group(1).strip() if triage_match else None
    
    return {
        'interpretation': interpretation,
        'triage': triage
    }

def get_reference(txt):
    return str(abs(hash(txt)) % (10 ** 8))

def get_date_today():
    def get_day_with_suffix(day):
        if 11 <= day <= 13:  # Special case for 11th, 12th, and 13th
            return f"{day}th"
        elif day % 10 == 1:  # Ends in 1 (but not 11)
            return f"{day}st"
        elif day % 10 == 2:  # Ends in 2 (but not 12)
            return f"{day}nd"
        elif day % 10 == 3:  # Ends in 3 (but not 13)
            return f"{day}rd"
        else:
            return f"{day}th"
        
    # Get today's date
    today = datetime.datetime.today()

    # Format the date
    formatted_date = today.strftime(f"%A, %B {get_day_with_suffix(today.day)}, %Y")
    return formatted_date

def reset_states(states):
    for state in states:
        st.session_state[state] = dss.session_states[state]
        
def split_frame(input_df, rows):
        df = [input_df.loc[i : i + rows - 1, :] for i in range(0, len(input_df), rows)]
        return df
        
def app():
    
    st.set_page_config(
        page_title = "SmartPulse Triage",
        layout = "wide"
    )
    
    # Initilize Session States
    for key,default_value in dss.session_states.items():
        if key not in st.session_state:
            st.session_state[key] = default_value
    
    ClaudeClient = anthropic.Anthropic(
        # api_key=fp.claude_api_key,
        api_key = st.secrets['claude_api_key']
    )
    
    st.markdown(f"""
    {sctn.hero_css}
    {sctn.hero_section}
    """,unsafe_allow_html=True)
    
    input_portion = st.empty()
    error_placeholder = st.empty()
    triage_generated_placeholder = st.empty()
    saved_triage_placeholder = st.empty()
    with input_portion.container(border = True):
        user_input_column, space_col, user_objective_col = st.columns([0.4, 0.1, 0.4])
            
        with user_objective_col:
            task = st.radio(
                "**Select Tool**",
                ("Assign","Review"),
                horizontal=True,
                on_change=reset_states,
                args=(dss.generation_states,)
            )
            
            if task == "Assign":
                st.session_state['search_bar_disabled'] = True
            elif task =="Review":
                st.session_state['search_bar_disabled'] = False
                
            
        with user_input_column:
            st.session_state['search_bar_value'] = st.text_input(
            "**Reference ID Search:**",
            disabled = st.session_state['search_bar_disabled']
            )
            
        st.markdown("""
        <hr class="hr hr-blurry-templates"/>
        """,unsafe_allow_html=True)
        
        if task == "Assign":
            st.session_state['search_bar_disabled'] = True
            with st.form(key = "PatientCall", border = False):
                
                patient_info_col, patient_condition_col = st.columns([0.3, 0.7])
                
                with patient_condition_col:
                    condition_of_patient = st.text_area("**Patient Condition**")
                    addtl_info_patient = st.text_area("**Relevant Additional Information**")
                
                with patient_info_col:
                    name_of_patient = st.text_input("**Name of Patient**")
                    contact_of_patient = st.text_input("**Contact Number**")
                    age_of_patient = st.text_input("**Age of Patient**")
                    
                def request_triage_func():
                    st.session_state["assign_patient_metadata_name"] = name_of_patient
                    st.session_state["assign_patient_metadata_contactno"] = contact_of_patient
                    st.session_state['assign_patient_age'] = age_of_patient
                    
                    def categorize_value(value):
                        ranges = [
                            (5, "0-5"), (10, "6-10"), (15, "11-15"), (20, "16-20"),
                            (30, "21-30"), (40, "31-40"), (50, "41-50"), (60, "51-60"),
                            (70, "61-70"), (80, "71-80")
                        ]
                        
                        for upper_bound, category in ranges:
                            if value <= upper_bound:
                                return category
                        return "Over 80"
                    
                    st.session_state['assign_patient_bracket'] = categorize_value(int(age_of_patient))
                    
                    if not condition_of_patient:
                        st.session_state['assign_patient_condition'] = ''
                    else:
                        st.session_state['assign_patient_condition'] = condition_of_patient
                        
                    if not addtl_info_patient:
                        st.session_state['assign_patient_additional_information'] = 'No additional info'
                        condition_text = f"{age_of_patient} - {condition_of_patient}"
                    else:
                        st.session_state['assign_patient_additional_information'] = addtl_info_patient
                        condition_text = f"{age_of_patient} - {condition_of_patient}({addtl_info_patient})"

                    response = ClaudeClient.beta.prompt_caching.messages.create(
                        model="claude-3-5-sonnet-20240620",
                        max_tokens=1500,
                        temperature=0,
                        system=[
                            {
                                "type": "text",
                                "text": prompts.historical_interpretations,
                                "cache_control": {"type": "ephemeral"}
                            }
                        ],
                        messages=[
                                {
                                    "role": "user",
                                    "content": [
                                        {
                                            "type": "text",
                                            "text": prompts.user_prompt_p1,
                                            "cache_control": {"type": "ephemeral"}
                                        },
                                        {
                                            "type": "text",
                                            "text": prompts.user_prompt_p2.format(condition=condition_text)
                                        }
                                    ]
                                },
                            ]
                    )
                    
                    customer_response = response.content[0].text.strip()
                    st.session_state['assign_generated_triage'] = customer_response
                
                if st.form_submit_button("Request Triage Suggestion", use_container_width=True,):
                    request_triage_func()
                    # try:
                    #     request_triage_func()
                    # except:
                    #     error_placeholder.error("Invalid Inputs")
                    
        elif task == "Review":
            st.session_state['search_bar_disabled'] = False
            
            # Load Data
            df = load_or_create_dataframe(fp.DATA_DIR.joinpath("TriageDatabase.csv"))
            
            # Filter the DataFrame only if there's a value in the search bar
            search_value = str(st.session_state.get('search_bar_value', ""))
            if search_value:
                df = df[df["Reference ID"].str.contains(search_value)]
                
            pages = split_frame(df, 10)
            
            total_pages = (
                int(len(df)/10) if int(len(df)>10) > 0 else 1
            )
            
            data_table_section = st.empty()
            bottom_menu_columns = st.columns([4,1,1])
            
            with bottom_menu_columns[2]:
                current_page = st.number_input(
                    "Page", min_value= 1, max_value=total_pages, step = 1
                )
                
            with bottom_menu_columns[0]:
                st.markdown(f"Page **{current_page}** of **{total_pages}** ")
            
            with data_table_section.container():
                st.markdown(sctn.triage_review_section_header,unsafe_allow_html=True)
                if pages:
                    for _, row in pages[current_page-1].iterrows():
                        with st.expander(f"**Triage Reference ID #{row['Reference ID']}**", expanded = True):
                            st.markdown(f"""
                                {sctn.triage_scheduled_results.format(
                                        referenceID = row["Reference ID"],
                                        dateOfrequest = row["Request Date"],
                                        patientName = row["Patient Name"],
                                        contactNumber = row["Contact Number"],
                                        ageBracket = row["Age Bracket"],
                                        condition = row["Condition"],
                                        addtlInfo = row["Additional Info"],
                                        triage = row['Triage'],
                                        triageNotes = row['Triage Notes']
                                    )
                                }
                                """, unsafe_allow_html=True)
                else:
                    st.error("No entry found.")
        
    if st.session_state['assign_generated_triage']:
        results = extract_information(st.session_state['assign_generated_triage'])
        interpret_suggestion = results['interpretation']
        triage_suggestion = results['triage']
        
        with triage_generated_placeholder.container(border = True):
            refid = get_reference(f"{st.session_state['assign_patient_metadata_name']}-{st.session_state['assign_patient_metadata_contactno']}-{datetime.datetime.now()}")
            date_today = get_date_today()
            st.markdown(f"""
            {sctn.triage_generate_results.format(
                    referenceID = refid,
                    dateOfrequest = date_today,
                    patientName = st.session_state['assign_patient_metadata_name'],
                    contactNumber = st.session_state['assign_patient_metadata_contactno'],
                    ageBracket = st.session_state['assign_patient_bracket'],
                    condition = st.session_state['assign_patient_condition'],
                    addtlInfo = st.session_state['assign_patient_additional_information']
                )
            }
            """, unsafe_allow_html=True)
            
            col_full,_ = st.columns([1,0.0001])
            with col_full:
                st.write(f"**Interpretation** : \n\n{interpret_suggestion}")
                    
            list_of_triages = [
                "GP Face to Face",
                "GP Remote",
                "Clinical Pharmacist Face to Face",
                "Remote Clinical Pharmacist",
                "Nurse Face to Face",
                "Nursing Associate Face to Face"
            ]
            
            lcol, rcol = st.columns ([0.30, 0.70])
            with lcol:
                final_triage = st.selectbox("**Triage Designation:**",
                                            list_of_triages,
                                            list_of_triages.index(triage_suggestion)) 
            with rcol:
                triage_notes = st.text_area("**Notes**:")
                
            if st.button("Submit Triage Appointment", use_container_width=True):
                triage_db_columns = [
                    "Reference ID",
                    "Request Date",
                    "Patient Name",
                    "Contact Number",
                    "Age",
                    "Age Bracket",
                    "Condition",
                    "Additional Info",
                    "Interpretation",
                    "Triage",
                    "Triage Notes"
                ]
                
                new_data = dict(zip(triage_db_columns,[
                    refid,
                    date_today,
                    st.session_state['assign_patient_metadata_name'],
                    st.session_state['assign_patient_metadata_contactno'],
                    st.session_state['assign_patient_age'],
                    st.session_state['assign_patient_bracket'],
                    st.session_state['assign_patient_condition'],
                    st.session_state['assign_patient_additional_information'],
                    interpret_suggestion,
                    final_triage,
                    "No Notes" if not triage_notes else triage_notes
                ]))
                
                update_dataframe(file_path=fp.DATA_DIR.joinpath("TriageDatabase.csv"),
                                 new_data = new_data,
                                 columns = triage_db_columns)
                
                saved_triage_placeholder.success("Triage Submitted!", icon = "✅")
    
    
    st.markdown("""
    <style>
        .customize-section {
            color : #444444;
            padding : 10px 0;
            scroll-margin-top : 77px;
            overflow : clip;
        }
        
        .customize-container {
            --bs-gutter-x : 1.5rem;
            --bs-gutter-y : 0;
            width : 100%;
            padding-right : 0.75rem;
            padding-left :  0.75rem;
            margin-right : auto;
            margin-left : auto;
        }
        
        .customize-section-title h2 {
            font-size : 14px;
            font-weight : 500;
            padding : 0;
            line-height : 1px;
            margin : 0;
            letter-spacing : 1.5px;
            text-transform : uppercase;
            color : color-mix(in srgb, #444444, transparent 50%);
            position : relative;
            font-family : "Raleway", sans-serif;
        }
        
        .customize-section-title h2::after {
            content : "";
            width : 120px;
            height : 1px;
            display : inline-block;
            background : #2197bd;
            margin : 4px 10px;
        }
        
        .customize-section-title p {
            color : #2a2c39;
            margin : 0;
            font-size : 16px;
            font-weight : 700;
            text-transform : uppercase;
            font-family : "Raleway", sans-serif;
            display : block;
            unicode-bidi : isolate;
        }
        .row-generate {
            display: flex;
            flex-wrap: wrap;
            margin-right: -15px;
            margin-left: -15px;
        }
        
        ul {
            list-style: none;
            padding-left: 0;
            margin: 0;
        }
        
        /* Column Layout */
        .col-6 {
            width: 50%;
            padding-right: 15px;
            padding-left: 15px;
            box-sizing: border-box;
        }

        /* Full Width Column */
        .col-12 {
            width: 100%;
            padding-right: 15px;
            padding-left: 15px;
            box-sizing: border-box;
        }
        
        /* Custom Styling for Invoice From Section */
        .invoice-from {
            text-align: right;
        }

        /* Section Title Styling */
        .customize-section-title h2 {
            font-size: 14px;
            font-weight: 500;
            letter-spacing: 1.5px;
            text-transform: uppercase;
            color: #444444;
            margin: 0;
            padding: 0;
        }
        
        .customize-section-title p {
            color: #2a2c39;
            font-size: 16px;
            font-weight: 700;
            text-transform: uppercase;
            margin: 0;
        }

        /* General Styles for Containers */
        .customize-container {
            width: 100%;
            padding-right: 0.75rem;
            padding-left: 0.75rem;
            margin-right: auto;
            margin-left: auto;
            box-sizing: border-box;
        }

        /* Invoice Details */
        .invoice-details {
            margin-top: 25px;
        }
        
        .well {
            padding-top: 20px;
            padding-bottom : 20px;
            padding-left : 5px;
            padding-right : 5px;
            margin-bottom: 20px;
            background-color: #f5f5f5;
            border: 1px solid #e3e3e3;
            border-radius: 4px;
        }

        .mb0 {
            margin-bottom: 0;
        }
        
        /* Label Styles */
        .label {
            display: inline;
            padding: .2em .6em .3em;
            font-size: 75%;
            font-weight: 700;
            line-height: 1;
            color: #fff;
            text-align: center;
            white-space: nowrap;
            vertical-align: baseline;
            border-radius: .25em;
        }

        .label-danger {
            background-color: #d9534f;
        }

        .label-success {
            background-color: #28a745;
        }

        /* Flexbox utilities (for alignment) */
        .d-flex {
            display: flex;
        }
        
        .justify-content-between {
            justify-content: space-between;
        }

        .justify-content-end {
            justify-content: flex-end;
        }

        .align-items-start {
            align-items: flex-start;
        }
    </style>
    """,unsafe_allow_html=True)
        
    st.markdown("""
    <style>
    
    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-radius : 20px;
        padding-left : 20px;
        padding-right : 20px;
        padding-top : 15px;
        padding-bottom : 15px;
    }
    
    button[kind="secondaryFormSubmit"] {
        border-radius : 10px;
        background-color : #2197bd;
        color : #fff;
        font-family : "Montserrat", sans-serif;
        font-weight : 500;
        font-size : 16px;
        letter-spacing : 1px;
    }
    
    button[kind="secondaryFormSubmit"]:hover {
        border-radius : 10px;
        background-color : color-mix(in srgb, #2197bd, transparent 20%);
        border-color : #176984;
        color : #fff;
        font-family : "Montserrat", sans-serif;
        font-weight : 500;
        font-size : 16px;
        letter-spacing : 1px;
    }
    
    button[kind="secondaryFormSubmit"]:focus:not(:active) {
        background-color : color-mix(in srgb, #2197bd, transparent 5%);
        border-color : #176984;
        color : #fff;
    }
    div[data-testid="stToolbar"] {
        visibility: hidden;
        height: 0%;
        position: fixed;
    }
    div[data-testid="stDecoration"] {
        visibility: hidden;
        height: 0%;
        position: fixed;
    }
    div[data-testid="stStatusWidget"] {
        visibility: hidden;
        height: 0%;
        position: fixed;
    }
    #MainMenu {
        visibility: hidden;
        height: 0%;
    }
    header {
        visibility: hidden;
        height: 0%;
    }
    footer {
        visibility: hidden;
        height: 0%;
    }
    
    .stAppViewBlockContainer {
        padding-top : 0rem;
        padding-bottom : 0.5rem;
    }
    </style>
    """,unsafe_allow_html=True)
    
if __name__ == "__main__":
    app()