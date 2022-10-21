'''
DUC Profile Creator App using Streamlit
Based on the DUC Schema version <TBD> at https://github.com/Digital-Use-Conditions/duc-schema
Please contact fjeanson@yahoo.com for more information
'''
import requests
from PIL import Image
from io import StringIO
import streamlit as st
import datetime
import pandas as pd
import json
import uuid

# Set web page metadata and menu content
st.set_page_config(page_title='DUC Profile Creator | by Datadex',
                   page_icon="🧊",
                   layout="centered",
                   initial_sidebar_state="auto",
                   menu_items={
                       'Get Help': 'mailto:fjeanson@yahoo.com',
                       'Report a bug': "mailto:fjeanson@yahoo.com",
                       'About': "DUC is the result of an international effort since 2020 to make clear statements about what research data and assets can or cannot be used and accessed for humans and machines."
                       })

# Load media content for this page
image_logo = Image.open('images/duc-logo.png')
st.image(image_logo)
st.title("Digital Use Conditions")
st.caption("Create a DUC profile .json file to define the conditions of use for your data or other assets. For more information please visit: https://github.com/Digital-Use-Conditions/duc-schema")

profileName = None
profileID = None
profileVersion = None
creationDate = None
updateDate = None
assets = None
assetName = None
assetDescription = None
assetURI = None
permissionMode = None
language = None

st.write('## Add optional fields')
if st.checkbox('Check to see optional fields'):
    if st.checkbox('Add a profile name'):
        profileName = st.text_input('Profile Name', key="profileName")
    if st.checkbox('Add a profile ID'):
        profileID = st.text_input('Profile ID', str(uuid.uuid4()), key="profileId")
        st.caption('A UUID v4 was created for your profile by default. Please change as necessary.')
    if st.checkbox('Add a profile version (ex: 1.0.0)'):
        profileVersion = st.text_input('Profile Version', key="profileVersion")
    if st.checkbox('Add a creation date'):
        creationDate = st.date_input('Creation date', datetime.datetime.now())
    if st.checkbox('Add an update date'):
        updateDate = st.date_input('Last updated', datetime.datetime.now())
    if st.checkbox('Add permission mode'):
        permissionMode = st.selectbox('Permission Mode', ('All unstated conditions are Forbidden', 'All unstated conditions are Permitted'), key='permissionMode')
    if st.checkbox('Add language'):
        language = st.text_input('Language', key='language')
    if st.checkbox('Add assets'):
        # TODO: add ability to add multiple assets
        assetName = st.text_input('Asset Name')
        assetDescription = st.text_input('Asset Description')
        assetURI = st.text_input('Asset formal model URI')
        assets = [{'assetName': assetName, 'assetURI': assetURI, 'assetDescription': assetDescription}]

st.write('## Define a new condition of use')
conditionTermLabel = st.text_input('Condition Term Label (ex: Disease specific research)', key='conditionTermLabel')
conditionTermURI = None
if st.checkbox('Add Condition Term URI'):
    conditionTermURI = st.text_input('Condition Term URI (ex: http://purl.obolibrary.org/obo/DUO_0000007)', key='conditionTermURI')
conditionDetailLabel = None
conditionDetailURI = None
conditionDetailValue = None
if st.checkbox('Add Condition Detail'):
    conditionDetailLabel = st.text_input('Condition Detail Label (ex: Month)', key='conditionDetailLabel')
    if st.checkbox('Add Condition Detail URI'):
        conditionDetailURI = st.text_input('Condition Detail URI (ex: http://purl.obolibrary.org/obo/UO_0000035)', key='conditionDetailURI')
    if st.checkbox('Add Condition Detail Value'):
        conditionDetailValue = st.text_input('Condition Detail Value (ex: 12)', key='conditionDetailValue')
# conditionRule = st.selectbox('Rule', ('No Requirement', 'Obligatory', 'Permitted', 'Forbidden'), key='rule')
conditionRule = st.select_slider('Select rule to apply', options=['No Requirement', 'Obligatory', 'Permitted', 'Forbidden'])
# conditionScope = st.selectbox('Scope', ('Whole of asset', 'Part of asset'), key='scope')
conditionScope = st.select_slider('Select scope', options=['Whole of asset', 'Part of asset'])

# Initiatlize df_conditions data frame and prevent override by events such as button press
if "df_conditions" not in st.session_state:
    st.session_state['df_conditions'] = pd.DataFrame(columns=['conditionTermLabel','conditionTermURI', 'conditionDetailLabel', 'conditionDetailURI', 'conditionDetailValue', 'conditionRule', 'conditionScope' ])

if st.button('Add this condition to the DUC profile'):
    condition = {}
    if conditionTermLabel == '':
        st.error('There\'s a missing Condition Term Label. At least one condition must be defined.', icon="🚨")
    else:
        condition.update({'conditionTermLabel': conditionTermLabel})
        condition.update({'conditionTermURI': conditionTermURI})
        condition.update({'conditionDetailLabel': conditionDetailLabel})
        condition.update({'conditionDetailURI': conditionDetailURI})
        condition.update({'conditionDetailValue': conditionDetailValue})
        condition.update({'conditionRule': conditionRule})
        condition.update({'conditionScope': conditionScope})
        condition_df = pd.DataFrame(condition, index=[0])
        # Add the condition to Streamlit's session_state storage
        st.session_state.df_conditions = pd.concat([st.session_state.df_conditions, condition_df], ignore_index=True)
        st.success('Your condition was added to this DUC profile.', icon="✅")

st.write('### List of added conditions')
st.table(st.session_state.df_conditions)

if st.button('Clear list of conditions (press twice)'):
    del st.session_state['df_conditions']
    st.session_state.df_conditions = pd.DataFrame(columns=['conditionTermLabel','conditionTermURI', 'conditionDetailLabel', 'conditionDetailURI', 'conditionDetailValue', 'conditionRule', 'conditionScope' ])

st.write('## Export DUC Profile')
def convert_df():
    json_doc = dict()
    json_doc.update({"$schema": "https://json-schema.org/draft/2020-12/schema"})
    json_doc.update({"$id": "https://github.com/Digital-Use-Conditions/duc-schema/blob/main/duc-schema.json"})
    if profileName: json_doc.update({"profileName": profileName})
    if profileID: json_doc.update({"profileID": profileID})
    if profileVersion: json_doc.update({"profileVersion": profileVersion})
    if creationDate: json_doc.update({"creationDate": str(creationDate)})
    if updateDate: json_doc.update({"lastUpdated": str(updateDate)})
    if assetName: json_doc.update({"assetName": assetName})
    if assetDescription: json_doc.update({"assetDescription": assetDescription})
    if assetURI: json_doc.update({"assetURI": assetURI})
    if permissionMode: json_doc.update({"permissionMode": permissionMode})
    if language: json_doc.update({"language": language})
    if assets: json_doc.update({"assets": assets})

    conditions_lst = []
    for index, row in st.session_state['df_conditions'].iterrows():
        condition_doc = dict()
        condition_doc.update({"conditionTermLabel": row['conditionTermLabel']})
        if row['conditionTermURI']: condition_doc.update({"conditionTermURI": row['conditionTermURI']})
        if row['conditionDetailLabel']: condition_doc.update({"conditionDetailLabel": row['conditionDetailLabel']})
        if row['conditionDetailURI']: condition_doc.update({"conditionDetailURI": row['conditionDetailURI']})
        if row['conditionDetailValue']: condition_doc.update({"conditionDetailValue": row['conditionDetailValue']})
        if row['conditionRule']: condition_doc.update({"rule": row['conditionRule']})
        if row['conditionScope']: condition_doc.update({"scope": row['conditionScope']})
        if len(condition_doc) > 0: conditions_lst.append(condition_doc)

    json_doc.update({'conditions': conditions_lst})
    return json.dumps(json_doc)

st.download_button(
    "Generate your DUC profile .json file",
    convert_df(),
    "duc-profile-"+datetime.datetime.now().isoformat()[:19]+".json",
    "text/json",
    key='download-json'
)

st.caption('Source code available here: https://github.com/FrancisJMR/duc-profile-creator')
st.caption('For questions or support please contact fjeanson@yahoo.com')
# TODO: let users upload a DUC profile JSON to enable UI based editing.
# uploaded_file = st.file_uploader("Load an existing DUC JSON profile file (.json)")
# if uploaded_file is not None:
#     stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
#     string_data = stringio.read()
#     # TODO: Parse string_data as DUC JSON profile
