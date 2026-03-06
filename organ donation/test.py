import streamlit as st
import hashlib
import csv
import os
from AppBlockchain import Blockchain, process_csv_and_update_blockchain
from LoadDB import CSVToSQLite
from EDA import ExploratoryDataAnalysis

# Constants for file paths
FILE_NAME = "organ_donation.csv"

# st.markdown(
#         f"""
#         <style>
#         [data-testid="stSidebar"] {{
#             background-color: {"#56c6e2"};
#             color: {"#dd6565"};
#         }}
#         </style>
#         """,
#         unsafe_allow_html=True)

st.markdown(
    f"""
        <style>
        .stApp {{
            background-color: {"#56c6e2"};
        }}
        </style>
        """,
    unsafe_allow_html=True
)

st.title("SECURE ORGAN DONATION SYSTEM BLOCKCHAIN-BASED DATA AUTHENTICATION AND ANALYTICAL INSIGHTS ")
st.image("Images/coverpage copy.png")

st.markdown(
    """
    <style>
    .white-text {
        color: black;
        font-size: 16px;
    }
    </style>
    <div class="white-text">
    ## About the Organ Donation App
    The **Organ Donation App** is a comprehensive platform designed to facilitate organ donation and requests while ensuring transparency, security, and data privacy. This app serves as a bridge between donors, recipients, and administrators, making the process of organ matching efficient and reliable.

    ### Key Features:
    - **Donor Registration:** 
        - Donors can register and provide details such as their blood type, available organs, and medical history.
        - User data is securely stored using **blockchain technology** to ensure transparency and immutability.
    - **Organ Request Matching:** 
        - Recipients can request organs by specifying their needs (e.g., organ type, blood type, age preferences).
        - The app uses advanced matching algorithms to find the most suitable donors based on the criteria provided.
    - **Admin Dashboard for EDA:**
        - Administrators have access to an **Exploratory Data Analysis (EDA)** dashboard for analyzing the data trends and ensuring quality in the donation system.
    - **Data Storage and Security:**
        - All donor and recipient information is stored securely in an **SQLite database**, ensuring data is private and protected.

    ### Why Choose This Platform?
    - **Transparency:** Leveraging blockchain for immutable records.
    - **Accessibility:** Easy-to-use interface for donors, recipients, and administrators.
    - **Reliability:** Advanced data handling ensures accurate matches.
    - **Social Impact:** Aims to save lives by making organ donation seamless and efficient.

    ### How It Works:
    1. **Registration:** 
        - Donors and recipients sign up by providing relevant details, including medical history.
        - Admins can log in for administrative tasks and data analysis.
    2. **Organ Matching:**
        - Recipients can search for organs by entering specific criteria.
        - The system matches donors and recipients based on compatibility.
    3. **Data Analytics:** 
        - Admins can analyze donation trends, identify areas for improvement, and monitor system performance.

    ### Get Started:
    - New users can **Register** to become a donor.
    - Existing users can **Log In** to request an organ or update their details.
    - Admins can access the **Admin Dashboard** for management and analysis.

    ---
    Organ donation is a life-saving act of kindness. Together, we can make a difference. Start your journey today!
    </div>

    """,
    unsafe_allow_html=True

)


# Function to create CSV file if it doesn't exist


def sidebar_information():
    """
    Display detailed information about the technologies used in the app: Blockchain, SQLite3, and Data Analytics.
    """
    st.sidebar.title("About the Technologies")

    # Blockchain Section
    st.sidebar.subheader("🔗 Blockchain")
    st.sidebar.image("Images/s4.png", caption="Domain Overview", use_column_width=True)
    st.sidebar.markdown("""
    Blockchain is a **decentralized and immutable ledger** used in this application to ensure the security, 
    transparency, and integrity of data. By storing donation records on the blockchain:
    - The data is tamper-proof and verifiable.
    - Users can trust the authenticity of organ donation records.
    - It fosters transparency and prevents fraud in the system.
    """)

    # SQLite3 Section
    st.sidebar.subheader("📂 SQLite3 Database")
    st.sidebar.image("Images/s2.png", caption="Domain Overview", use_column_width=True)
    st.sidebar.markdown("""
    SQLite3 is a lightweight, serverless **relational database management system (RDBMS)**. 
    It is used in this app for:
    - **Data Storage:** Storing donor, recipient, and admin records.
    - **Querying Data:** Efficiently retrieving and managing user details.
    - **Ease of Use:** SQLite3 is compact and ideal for this application since it doesn't require a separate server.
    """)

    # Data Analytics Section
    st.sidebar.subheader("📊 Data Analytics")
    st.sidebar.image("Images/s3.png", caption="Domain Overview", use_column_width=True)
    st.sidebar.markdown("""
    The app includes a robust **Exploratory Data Analysis (EDA)** dashboard for administrators. Using tools like 
    **Pandas**, **Seaborn**, and **Matplotlib**, the EDA features provide:
    - **Data Visualization:** Univariate, bivariate, and multivariate analysis to explore trends.
    - **Insights:** Identify patterns in donor and recipient data to improve the matching process.
    - **Decision-Making:** Aid administrators in enhancing the organ donation process through data-driven insights.
    """)

    # Final Message
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Empowering Organ Donation with Technology 🚀")


sidebar_information()


def create_csv():
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["id", "name", "age", "blood_type", "organs", "contact_info", "password", "location",
                             "chronic_diseases", "infectious_diseases", "cancer_history", "current_medications"])


# User Registration Function
def register_user():
    st.title("Organ Donation Registration")

    # Collecting user details
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=1)
    blood_type = st.selectbox("Blood Type", ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])
    organs = st.multiselect("Organs Available for Donation", ["Heart", "Liver", "Kidney", "Lung", "Pancreas"])
    contact_info = st.text_input("Contact Information")
    password = st.text_input("Password", type="password")
    location = st.text_input("Location (City, Country)")

    # Medical Details
    chronic_diseases = st.selectbox("Chronic Diseases",
                                    ["None", "Diabetes", "Hypertension", "Asthma", "Heart Disease", "Kidney Disease",
                                     "Liver Disease"])
    infectious_diseases = st.selectbox("Infectious Diseases",
                                       ["None", "HIV", "Hepatitis B", "Hepatitis C", "Tuberculosis", "Syphilis"])
    cancer_history = st.selectbox("Cancer History",
                                  ["None", "Breast Cancer", "Liver Cancer", "Lung Cancer", "Colon Cancer",
                                   "Prostate Cancer", "Leukemia"])
    current_medications = st.selectbox("Current Medications",
                                       ["None", "Immunosuppressants", "Blood Pressure Meds", "Diabetic Medications",
                                        "Painkillers", "Antibiotics", "Cholesterol Meds"])

    if st.button("Register"):
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        # Open CSV and append user data
        with open(FILE_NAME, mode='a', newline='') as file:
            writer = csv.writer(file)
            user_id = sum(1 for _ in open(FILE_NAME))  # Simple ID generation by counting rows
            writer.writerow([user_id, name, age, blood_type, ",".join(organs), contact_info, hashed_password,
                             location, chronic_diseases, infectious_diseases, cancer_history, current_medications])

            blockchain = Blockchain()

            # Process the CSV file and update the blockchain once
            process_csv_and_update_blockchain(FILE_NAME, blockchain)
            csv_to_sqlite = CSVToSQLite()
            csv_to_sqlite.upload_csv(FILE_NAME)

        st.success("Registration Successful!")


# User Login Function
def login_user():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    st.title("Login")
    name = st.text_input("Name")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        # Search for user in CSV
        with open(FILE_NAME, mode='r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header row
            user_found = False
            for row in reader:
                if row[1] == name and row[6] == hashed_password:
                    st.session_state.logged_in = True
                    st.session_state.user = row  # Store user data in session state
                    user_found = True
                    break

        if user_found:
            st.session_state.user_name = name  # Store the username in session state
            st.success("Login Successful!")
        else:
            st.error("User not found. Please register or check your credentials.")


def login_admin():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'is_admin' not in st.session_state:
        st.session_state.is_admin = False

    # Check if the admin is already logged in
    if st.session_state.is_admin:
        st.success("You are already logged in as Admin.")
        eda = ExploratoryDataAnalysis("organ_donation.csv")
        eda.run()  # Call the ExploratoryDataAnalysis function if logged in as admin
        return  # Skip admin login UI if logged in as admin

    st.title("Admin Login")
    name = st.text_input("Name")
    password = st.text_input("Password", type="password")

    # Hardcoded credentials
    correct_username = "admin"
    correct_password = "password"

    if st.button("Login"):
        if name == correct_username and password == correct_password:
            st.session_state.logged_in = True
            st.session_state.is_admin = True  # Mark as admin
            st.session_state.user_name = name  # Store the username in session state
            st.success(f"Login Successful! Welcome {name}")

            # Call the ExploratoryDataAnalysis class after successful login
            eda = ExploratoryDataAnalysis("organ_donation.csv")
            eda.run()
        else:
            st.error("Invalid username or password. Please try again.")


def display_logged_in_user():
    if 'logged_in' in st.session_state and st.session_state.logged_in:
        if 'user_name' in st.session_state:
            st.write(f"Logged in as: {st.session_state.user_name}")
        # if 'is_admin' in st.session_state and st.session_state.is_admin:
        #     st.write("Logged in as Admin.")
    else:
        st.write("You are not logged in.")


# Organ Request Function with Enhanced Matching
def request_organ():
    if 'logged_in' in st.session_state and st.session_state.logged_in:
        st.title("Request an Organ")

        # Collecting user input for organ request
        organ_needed = st.multiselect("Organs Needed", ["Heart", "Liver", "Kidney", "Lung", "Pancreas"])
        blood_type = st.selectbox("Blood Type", ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])
        min_age = st.number_input("Minimum Age", min_value=1)
        max_age = st.number_input("Maximum Age", min_value=1)

        if st.button("Search for Match"):
            matches = []

            # Search for matches in the CSV
            with open(FILE_NAME, mode='r') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header row
                for row in reader:
                    if (any(organ in row[4] for organ in organ_needed) and
                            row[3] == blood_type and
                            min_age <= int(row[2]) <= max_age and
                            row[0] != st.session_state.user[0]):  # Exclude the current user
                        matches.append(row)

            # Sort matches by similarity (age difference)
            sorted_matches = sorted(matches, key=lambda match: abs(int(match[2]) - int(st.session_state.user[2])))

            # Display matches
            if sorted_matches:
                st.success(f"{len(sorted_matches)} Match(es) Found!")
                for match in sorted_matches:
                    st.write("Name:", match[1])
                    st.write("Age:", match[2])
                    st.write("Blood Type:", match[3])
                    st.write("Organs Available:", match[4])
                    st.write("Contact Info:", match[5])
                    st.write("Location:", match[7])
                    st.write("Chronic Diseases:", match[8])
                    st.write("Infectious Diseases:", match[9])
                    st.write("Cancer History:", match[10])
                    st.write("Current Medications:", match[11])
                    st.write("---")
            else:
                st.warning("No match found.")
    else:
        st.warning("Please log in to request an organ.")


# Main Streamlit App Entry
def main():
    st.sidebar.title("Organ Donation App")

    # Sidebar option for user to choose between Register, Login, or Admin
    choice = st.sidebar.selectbox("Select Option", ["Register", "Login", "Admin"])

    # Ensure CSV file exists
    create_csv()

    if choice == "Register":
        register_user()

    elif choice == "Admin":
        login_admin()
        display_logged_in_user()

    elif choice == "Login":
        login_user()
        if 'logged_in' in st.session_state and st.session_state.logged_in:
            request_organ()
        else:
            st.warning("Please log in to request an organ.")


if __name__ == "__main__":
    main()
