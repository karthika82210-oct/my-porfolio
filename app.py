import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Cybersecurity Login Logs Analyzer",
    layout="wide"
)

# -----------------------------
# CUSTOM CSS STYLE
# -----------------------------
st.markdown("""
<style>

.main {
    background-color: #0E1117;
}

h1, h2, h3 {
    color: #00C8FF;
    text-align: center;
}

.stButton>button {
    background-color: #00C8FF;
    color: black;
    border-radius: 8px;
    font-weight: bold;
}

.stMetric {
    background-color: #1E222A;
    padding: 15px;
    border-radius: 10px;
    text-align: center;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# LOGIN CREDENTIALS
# -----------------------------
USER = "admin"
PASS = "admin123"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


# -----------------------------
# LOGIN FUNCTION
# -----------------------------
def login():

    st.title("🔐 Cybersecurity Login Logs Dashboard")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        if username == USER and password == PASS:
            st.session_state.logged_in = True
            st.success("Login Successful")

        else:
            st.error("Invalid Credentials")


# -----------------------------
# DASHBOARD FUNCTION
# -----------------------------
def dashboard():

    st.title("🛡 Cybersecurity Login Logs Analysis")

    st.write("Monitor login activity and detect suspicious login attempts.")

    # Sidebar
    st.sidebar.title("🔐 Security Panel")

    menu = st.sidebar.radio(
        "Navigation",
        ["Dashboard", "Suspicious Activity", "Raw Logs"]
    )

    file = st.file_uploader("Upload Login Logs CSV", type=["csv"])

    if file is not None:

        df = pd.read_csv(file)

        # -----------------------------
        # DASHBOARD PAGE
        # -----------------------------
        if menu == "Dashboard":

            st.subheader("📊 System Overview")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("Total Logins", len(df))

            with col2:
                st.metric("Unique Users", df["username"].nunique())

            with col3:
                st.metric("Unique IPs", df["ip_address"].nunique())

            st.divider()

            # Login status chart
            status_chart = px.pie(
                df,
                names="status",
                title="Login Success vs Failed"
            )

            st.plotly_chart(status_chart, use_container_width=True)

            # Top users chart
            user_chart = px.bar(
    df["username"].value_counts().head(10),
    title="Top Users Login Attempts",
    color_discrete_sequence=["#2EC4B6"]
)

            st.plotly_chart(user_chart, use_container_width=True)

        # -----------------------------
        # SUSPICIOUS ACTIVITY PAGE
        # -----------------------------
        elif menu == "Suspicious Activity":

            st.subheader("🚨 Suspicious Activity Detection")

            failed = df[df["status"] == "failed"]

            suspicious = (
                failed.groupby("ip_address")
                .size()
                .reset_index(name="failed_attempts")
                .sort_values("failed_attempts", ascending=False)
            )

            st.warning("⚠ Multiple failed login attempts detected!")

            st.dataframe(suspicious)

            # Chart
            attack_chart = px.bar(
    suspicious.head(10),
    x="ip_address",
    y="failed_attempts",
    title="Top Suspicious IP Addresses",
    color_discrete_sequence=["grey"]
)

            st.plotly_chart(attack_chart, use_container_width=True)

        # -----------------------------
        # RAW LOGS PAGE
        # -----------------------------
        elif menu == "Raw Logs":

            st.subheader("📋 Raw Login Logs")

            st.dataframe(df)

    else:
        st.info("Please upload a login logs CSV file to begin analysis.")


# -----------------------------
# APP ROUTER
# -----------------------------
if st.session_state.logged_in:
    dashboard()
else:
    login()

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("""
---
<center>Cybersecurity Login Logs Analyzer </center>
""", unsafe_allow_html=True)