
import streamlit as st
import pandas as pd

# Page settings
st.set_page_config(
    page_title="EMI Finance Dashboard",
    page_icon="💰",
    layout="wide"
)

# App heading
st.title("💰 EMI Finance Dashboard")
st.caption("Calculate your monthly loan payment and repayment schedule.")

st.divider()

# Input section
st.subheader("Enter Loan Details")

with st.form("loan_form"):
    loan = st.number_input(
        "Loan Amount (₹)",
        min_value=1,
        value=500000,
        step=10000
    )

    rate = st.number_input(
        "Annual Interest Rate (%)",
        min_value=0.0,
        value=8.5,
        step=0.5
    )

    months = st.number_input(
        "Loan Duration (months)",
        min_value=1,
        max_value=600,
        value=60,
        step=1
    )

    calculate = st.form_submit_button(
        "Calculate EMI",
        type="primary",
        use_container_width=True
    )

# Calculate after button click
if calculate:
    monthly_rate = rate / 1200

    if monthly_rate == 0:
        emi = loan / months
    else:
        emi = (
            loan * monthly_rate
            * (1 + monthly_rate) ** months
            / ((1 + monthly_rate) ** months - 1)
        )

    total_payment = emi * months
    total_interest = total_payment - loan

    # Dashboard summary
    st.divider()
    st.subheader("Your Loan Summary")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Monthly EMI",
        f"₹{emi:,.2f}"
    )

    col2.metric(
        "Total Interest",
        f"₹{total_interest:,.2f}"
    )

    col3.metric(
        "Total Repayment",
        f"₹{total_payment:,.2f}"
    )

    # Monthly repayment schedule
    st.divider()
    st.subheader("Monthly Repayment Schedule")

    balance = float(loan)
    schedule = []

    for month in range(1, int(months) + 1):
        interest = balance * monthly_rate
        principal = emi - interest

        # Adjust final payment for rounding
        if month == months:
            principal = balance
            payment = principal + interest
        else:
            payment = emi

        balance = max(0, balance - principal)

        schedule.append({
            "Month": month,
            "EMI (₹)": round(payment, 2),
            "Interest (₹)": round(interest, 2),
            "Principal (₹)": round(principal, 2),
            "Remaining Balance (₹)": round(balance, 2)
        })

    df = pd.DataFrame(schedule)

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    # Visual comparison
    st.subheader("Principal vs Interest")

    chart_data = df.set_index("Month")[
        ["Principal (₹)", "Interest (₹)"]
    ]

    st.bar_chart(chart_data)

    st.caption(
        "Estimate only. Actual lender charges and rounding may differ."
    )
