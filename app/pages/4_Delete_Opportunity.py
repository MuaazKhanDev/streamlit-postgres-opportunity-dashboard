#Updated by MuaazAsifKhan 
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import streamlit as st
from auth import check_login, require_admin
from queries import get_all_opportunities, get_opportunity_by_id, delete_opportunity

check_login()
require_admin()

st.header('Delete Opportunity')

df = get_all_opportunities()
options = df.apply(lambda r: f"{r['opportunity_id']} - {r['company_name']} | {r['job_title']}", axis=1).tolist()
choice = st.selectbox('Select Opportunity to delete', options=['']+options)
if choice:
    opp_id = int(choice.split(' - ')[0])
    record = get_opportunity_by_id(opp_id)
    if record:
        st.info(record)
        st.warning('This action cannot be undone')
        confirm = st.checkbox('I confirm I want to delete this record')
        if confirm:
            if st.button('Delete'):
                delete_opportunity(opp_id)
                st.success('Record deleted')


