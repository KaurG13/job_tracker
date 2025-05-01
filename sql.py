import mysql.connector
import streamlit as st
import pandas as pd
# Replace with your credentials
mydb = {
    "host": "localhost",
    "user": "root",  # Or 'root' if you're using root
    "password": "sqlwj@13",  # Password you set
    "database": "jobs"  # Or any database you want to work with
}

def init_db():
    conn = mysql.connector.connect(**mydb)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS jobs (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    company VARCHAR(255) NOT NULL,
                    job_title VARCHAR(255) NOT NULL,
                    application_date DATE,
                    status ENUM('Applied', 'Interview Scheduled', 'Offer Received', 'Rejected', 'Accepted') DEFAULT 'Applied',
                    job_link VARCHAR(500),
                    salary VARCHAR(100),
                    notes TEXT)''')
    conn.commit()
    conn.close()

# Function to add job
def add_job(company, job_title, application_date, status, job_link, salary, notes):
    conn = mysql.connector.connect(**mydb)
    c = conn.cursor()
    c.execute("INSERT INTO jobs (company, job_title, application_date, status, job_link, salary, notes) VALUES (%s, %s, %s, %s, %s, %s, %s)",
              (company, job_title, application_date, status, job_link, salary, notes))
    conn.commit()
    conn.close()

# Function to retrieve jobs
def get_jobs():
    conn = mysql.connector.connect(**mydb)
    c = conn.cursor()
    c.execute("SELECT * FROM jobs")
    jobs = c.fetchall()
    conn.close()
    return jobs

# Function to update job status
def update_job_status(job_id, status):
    conn = mysql.connector.connect(**mydb)
    c = conn.cursor()
    c.execute("UPDATE jobs SET status = %s WHERE id = %s", (status, job_id))
    conn.commit()
    conn.close()

# Function to delete a job
def delete_job(job_id):
    conn = mysql.connector.connect(**mydb)
    c = conn.cursor()
    c.execute("DELETE FROM jobs WHERE id = %s", (job_id,))
    conn.commit()
    conn.close()

# Initialize database
init_db()

# Streamlit UI
st.set_page_config(page_title="Job Application Tracker 📝", layout="wide")

st.title("Job Application Tracker 📝")
st.markdown("""
Welcome to your job application tracker! Stay organized and keep track of your applications, statuses, and key details.
""")

menu = ["Add Job", "View Jobs", "Update Status", "Delete Job"]
choice = st.sidebar.selectbox("Select an Action", menu)

# Add Job Section
if choice == "Add Job":
    st.subheader("Add a New Job Application")
    
    with st.form("add_job_form"):
        company = st.text_input("Company Name", max_chars=100)
        job_title = st.text_input("Job Title", max_chars=100)
        application_date = st.date_input("Application Date")
        status = st.selectbox("Status", ["Applied", "Interview Scheduled", "Offer Received", "Rejected", "Accepted"])
        job_link = st.text_input("Job Link", max_chars=500)
        salary = st.text_input("Salary (optional)", max_chars=100)
        notes = st.text_area("Notes", max_chars=1000)
        
        submit_button = st.form_submit_button("Add Job")
        
        if submit_button:
            add_job(company, job_title, application_date, status, job_link, salary, notes)
            st.success(f"Job at {company} added successfully!")

# View Jobs Section
elif choice == "View Jobs":
    st.subheader("All Job Applications")
    
    jobs = get_jobs()
    if jobs:
        df = pd.DataFrame(jobs, columns=["ID", "Company", "Job Title", "Date", "Status", "Job Link", "Salary", "Notes"])
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("No job applications found.")

# Update Status Section
elif choice == "Update Status":
    st.subheader("Update Job Status")
    
    jobs = get_jobs()
    if jobs:
        job_ids = [job[0] for job in jobs]
        selected_id = st.selectbox("Select Job ID", job_ids)
        new_status = st.selectbox("New Status", ["Applied", "Interview Scheduled", "Offer Received", "Rejected", "Accepted"])
        
        if st.button("Update Status"):
            update_job_status(selected_id, new_status)
            st.success(f"Job ID {selected_id} status updated!")
    else:
        st.warning("No jobs available to update.")

# Delete Job Section
elif choice == "Delete Job":
    st.subheader("Delete a Job Application")
    
    jobs = get_jobs()
    if jobs:
        job_ids = [job[0] for job in jobs]
        selected_id = st.selectbox("Select Job ID to Delete", job_ids)
        
        if st.button("Delete Job"):
            delete_job(selected_id)
            st.success(f"Job ID {selected_id} deleted successfully!")
    else:
        st.warning("No jobs available to delete.")
