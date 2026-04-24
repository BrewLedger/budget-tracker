import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import csv
import os

# Page config
st.set_page_config(page_title="Budget Tracker", page_icon="💰", layout="centered")

# Title and description
st.title("💰 Personal Budget Tracker")
st.markdown("""
> 🇸🇬 **Built for Singaporeans who want to take control of their finances!**  
> Track your income, monitor your expenses, and stay on top of your budget —  
> all in one simple and beautiful app! 💪📊
""")
st.divider()

# Initialize session state
if "expenses" not in st.session_state:
    st.session_state.expenses = []
if "income_saved" not in st.session_state:
    st.session_state.income_saved = False
if "income" not in st.session_state:
    st.session_state.income = 0.0

# Load saved expenses from CSV if exists
SAVE_FILE = "expenses.csv"
if os.path.exists(SAVE_FILE) and len(st.session_state.expenses) == 0:
    with open(SAVE_FILE, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) == 2:
                st.session_state.expenses.append((row[0], float(row[1])))

def save_expenses():
    with open(SAVE_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(st.session_state.expenses)

# Income section
st.header("💵 Monthly Income")
income_input = st.number_input("Enter your monthly income ($)",
                                min_value=0.0,
                                value=None,
                                placeholder="e.g. 3000")

if st.button("✅ Save Income"):
    if income_input and income_input > 0:
        st.session_state.income = income_input
        st.session_state.income_saved = True
        st.rerun()
    else:
        st.warning("⚠️ Please enter a valid income amount!")

if st.session_state.income_saved:
    st.success(f"✅ Income of **${st.session_state.income:,.2f}** saved successfully!")
    st.info(f"💵 Current saved income: **${st.session_state.income:,.2f}**")

st.divider()

# Expense section
st.header("📝 Add Expenses")
col1, col2 = st.columns(2)
with col1:
    expense_name = st.text_input("Expense name", placeholder="e.g. Rent, Food, Transport")
with col2:
    expense_amount = st.number_input("Amount ($)",
                                      min_value=0.0,
                                      value=None,
                                      placeholder="e.g. 500")

if st.button("➕ Add Expense"):
    if expense_name and expense_amount and expense_amount > 0:
        st.session_state.expenses.append((expense_name, expense_amount))
        save_expenses()
        st.rerun()
    else:
        st.warning("⚠️ Please enter both a name and amount!")

if st.button("🗑️ Clear All Expenses"):
    st.session_state.expenses = []
    if os.path.exists(SAVE_FILE):
        os.remove(SAVE_FILE)
    st.rerun()

st.divider()

# Summary and charts
income = st.session_state.income
if st.session_state.expenses and income > 0:
    total_expense = sum(amount for name, amount in st.session_state.expenses)
    balance = income - total_expense

    st.header("📊 Your Summary")
    col1, col2, col3 = st.columns(3)
    col1.metric("💵 Income", f"${income:,.2f}")
    col2.metric("💸 Expenses", f"${total_expense:,.2f}")
    col3.metric("🏦 Balance", f"${balance:,.2f}",
                delta=f"${balance:,.2f}",
                delta_color="normal" if balance >= 0 else "inverse")

    if balance < 0:
        st.error("🚨 You are overspending! Time to cut back on expenses.")
    elif balance < income * 0.2:
        st.warning("⚠️ You are spending more than 80% of your income. Be careful!")
    else:
        st.success("🎉 Great job! You are managing your budget well!")

    st.divider()

    # Pie chart
    st.subheader("🥧 Spending Breakdown")
    df = pd.DataFrame(st.session_state.expenses, columns=["Expense", "Amount"])
    fig_pie = px.pie(df, values="Amount", names="Expense",
                     title="Where is your money going?",
                     hole=0.4)
    st.plotly_chart(fig_pie, use_container_width=True)

    # Bar chart - Income vs Expenses vs Balance
    st.subheader("📊 Income vs Expenses Overview")
    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(
        x=["💵 Income", "💸 Total Expenses", "🏦 Balance"],
        y=[income, total_expense, balance],
        marker_color=["#2ecc71", "#e74c3c", "#3498db"],
        text=[f"${income:,.2f}", f"${total_expense:,.2f}", f"${balance:,.2f}"],
        textposition="auto"
    ))
    fig_bar.update_layout(title="Income vs Expenses vs Balance",
                          yaxis_title="Amount ($)")
    st.plotly_chart(fig_bar, use_container_width=True)

    # Expense list
    st.subheader("🧾 Expense List")
    for name, amount in st.session_state.expenses:
        st.write(f"• {name}: **${amount:,.2f}**")

    st.divider()

# Singapore budgeting tips section
st.header("📰 Why Budgeting Matters in Singapore")
st.markdown("*Key insights on personal finance for Singaporeans:*")
st.divider()

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🏠 Cost of Living")
    st.write("Singapore consistently ranks as one of the most expensive cities in the world. A solid budget helps you stay ahead of rising costs in housing, food and transport.")

    st.markdown("### 🌴 Retirement Planning")
    st.write("CPF alone may not be enough for a comfortable retirement. Budgeting now means more savings and investments for your future self.")

    st.markdown("### 🎓 Education Costs")
    st.write("From tuition fees to enrichment classes, education in Singapore is costly. Planning ahead ensures your children get the best without financial stress.")

with col2:
    st.markdown("### 🏥 Healthcare")
    st.write("Medical costs in Singapore are significant. Setting aside an emergency fund as part of your budget protects you and your family from unexpected bills.")

    st.markdown("### 📈 Growing Your Wealth")
    st.write("A good budget frees up money for investments in stocks, REITs, or savings plans — helping your money work harder for you.")

    st.markdown("### 💳 Avoiding Debt")
    st.write("Credit card debt and personal loans carry high interest rates in Singapore. Budgeting helps you spend within your means and stay debt free.")

st.divider()

st.markdown("### 💡 Singapore Budgeting Tips")
st.success("✅ Follow the **50/30/20 rule** — 50% needs, 30% wants, 20% savings")
st.info("📊 Use **CPF wisely** — understand your OA, SA and MA accounts")
st.warning("⚠️ **Emergency fund** — aim for at least 6 months of expenses saved")
st.error("🚨 **Avoid lifestyle inflation** — just because you earn more doesn't mean you should spend more")

st.divider()
st.caption("💰 Budget Tracker | Built with Python & Streamlit | By Ee Jer / BrewLedger")