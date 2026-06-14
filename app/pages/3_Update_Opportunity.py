#Updated by MuaazAsifKhan
from __future__ import annotations

import streamlit as st
from auth import check_login, require_admin
from queries import get_all_opportunities, get_opportunity_by_id, update_opportunity

check_login()
require_admin()

st.header('Update Opportunity')

df = get_all_opportunities()
options = df.apply(lambda r: f"{r['opportunity_id']} - {r['company_name']} | {r['job_title']}", axis=1).tolist()
id_map = {opt.split(' - ')[0]: opt for opt in options}

choice = st.selectbox('Select Opportunity', options=['']+options)
if choice:
    opp_id = int(choice.split(' - ')[0])
    record = get_opportunity_by_id(opp_id)
    if record:
        with st.form('update_form'):
            company_name = st.text_input('Company Name', value=record.get('company_name',''))
            job_title = st.text_input('Job Title', value=record.get('job_title',''))
            category = st.selectbox('Category', ['Data Science','Artificial Intelligence','Web Development','Cyber Security','Other'], index=0)
            city = st.text_input('City', value=record.get('city',''))
            country = st.text_input('Country', value=record.get('country','Pakistan'))
            work_mode = st.selectbox('Work Mode', ['Remote','Onsite','Hybrid'], index=0)
            required_skills = st.text_area('Required Skills', value=record.get('required_skills',''))
            salary_min = st.number_input('Salary Min', min_value=0, value=int(record.get('salary_min') or 0))
            salary_max = st.number_input('Salary Max', min_value=0, value=int(record.get('salary_max') or 0))
            currency = st.selectbox('Currency', ['PKR','USD'], index=0)
            experience_level = st.selectbox('Experience Level', ['Fresh','Junior','Mid-Level','Senior'], index=0)
            application_deadline = st.date_input('Application Deadline', value=record.get('application_deadline'))
            status = st.selectbox('Status', ['Open','Closed','Expired','Shortlisted'], index=0)
            source_link = st.text_input('Source Link', value=record.get('source_link',''))
            submitted = st.form_submit_button('Update')
            if submitted:
                data = {
                    'company_name': company_name,
                    'job_title': job_title,
                    'category': category,
                    'city': city,
                    'country': country,
                    'work_mode': work_mode,
                    'required_skills': required_skills,
                    'salary_min': salary_min if salary_min>0 else None,
                    'salary_max': salary_max if salary_max>0 else None,
                    'currency': currency,
                    'experience_level': experience_level,
                    'application_deadline': application_deadline.strftime('%Y-%m-%d') if application_deadline else None,
                    'status': status,
                    'source_link': source_link,
                }
                update_opportunity(opp_id, data)
                st.success('Opportunity updated')


