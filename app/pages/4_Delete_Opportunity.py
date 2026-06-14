#Updated by MuaazAsifKhan 
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import streamlit as st
from queries import get_all_opportunities, get_opportunity_by_id, delete_opportunity

st.header('Delete Opportunity')

# Get all opportunities
df = get_all_opportunities()

# Create options for dropdown
options = df.apply(
    lambda r: f"{r['opportunity_id']} - {r['company_name']} | {r['job_title']}", 
    axis=1
).tolist()

choice = st.selectbox('Select Opportunity to delete', [''] + options)

if choice:
    opp_id = int(choice.split(' - ')[0])
    
    record = get_opportunity_by_id(opp_id)
    if record:
        st.subheader("Opportunity to Delete")
        st.json(record)  # or st.dataframe(record) / st.write(record)
        
        st.warning('⚠️ This action cannot be undone!')
        
        if st.button('Delete Opportunity', type="primary"):
            delete_opportunity(opp_id)
            st.success(f'Opportunity {opp_id} deleted successfully!')
            st.rerun()  # Refresh the page
