import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu 
from numerize.numerize import numerize
import query
import time

st.set_page_config(page_title= "Dashboard",page_icon="🌎", layout="wide")
st.subheader("🔔 Insurance Descriptive Analytics")
st.markdown("##")


Result = query.view_all_data()
df = pd.DataFrame(Result,columns= ["Policy","Expiry","Location","State","Region","Investment","Construction","Business Type","Earthquake","Flood","Rating","id"])

# Side bar
st.sidebar.title("Insurance Analytics")

# Switcher
st.sidebar.header("Filter")
region = st.sidebar.multiselect(
    "Select Region",
    options = df["Region"].unique(),
    default = df["Region"].unique(),
)
location = st.sidebar.multiselect(
    "Select Location",
    options = df["Location"].unique(),
    default = df["Location"].unique(),
)
construction = st.sidebar.multiselect(
    "Select Construction",
    options = df["Construction"].unique(),
    default = df["Construction"].unique(),
)

df_selection = df.query(
    "Region == @region & Location == @location & Construction == @construction"
)

def Home():
    with st.expander("Tabular"):
        showData = st.multiselect('Filter: ',df_selection.columns,default=[])
        st.write(df_selection[showData])
    # Compute top analytics
    total_investment = float(df_selection["Investment"].sum())
    investment_mean = float(df_selection["Investment"].mean())
    investment_median = float(df_selection["Investment"].median())
    rating = float(df_selection["Rating"].sum())

    total1,total2,total3,total4 = st.columns(4,gap = 'medium')
    with total1:
        st.info('Total Investment',icon = "💰")
        st.metric(label = "Sum",value = f"{total_investment:,.0f}",help = f"""  Total investment: {total_investment} """)

    with total2:
        st.info('Avg Investment',icon = "💰")
        st.metric(label = "Mean",value = f"{investment_mean:,.0f}",help = f"""  Average investment: {investment_mean} """)
    
    with total3:
        st.info('Base Income',icon = "📌")
        st.metric(label = "Median",value = f"{investment_median:,.0f}",help = f"""  Base Income: {investment_median} """)

    with total4:
        st.info('Overall Rating',icon = "📌")
        st.metric(label = "Sum",value = numerize(rating),help = f"""  Total Rating: {rating} """)

    st.markdown("""---""")

# Graphs

def graphs():
    total_investment = int(df_selection["Investment"].sum())
    averageRating = int(round(df_selection["Rating"].mean(),2))

    # Simpe bar graph
    investment_by_business_type = (
        df_selection.groupby("Business Type").count()[["Investment"]].sort_values(by = "Investment")
    )
    fig_investment = px.bar(
        investment_by_business_type,
        x = "Investment",
        y = investment_by_business_type.index,
        orientation="h",
        title = "Investment by Business Type",
        color_discrete_sequence= ["#0083b8"] *len(investment_by_business_type),
        template="plotly_dark",
    )

    fig_investment.update_layout(
    plot_bgcolor = "rgba(0,0,0,0)",
    xaxis = (dict(showgrid = False))
    )


    # Simpe line graph
    investment_state = df_selection.groupby(by = ["State"]).count()[["Investment"]]
    fig_state = px.line(
        investment_state,
        x = investment_state.index,
        y = "Investment",
        orientation="v",
        title = "Investment by State",
        color_discrete_sequence= ["#0083b8"] *len(investment_state),
        template="plotly_dark",
    )
    fig_state.update_layout(
    xaxis = dict(tickmode = "linear"),
    plot_bgcolor = "rgba(0,0,0,0)",
    yaxis = (dict(showgrid = False))
    )

    left, right = st.columns(2)
    left.plotly_chart(fig_investment, use_continer_width = True)
    right.plotly_chart(fig_state, use_continer_width = True)

def Progressbar():
    st.markdown(""" <style>.stProgress > div > div > div > div {background-image: linear-gradient(to right, #99ff9, #FFFF00)}</style>""",unsafe_allow_html = True)
    target = 3000000000
    current = df_selection["Investment"].sum()
    percent = round((current/target*100))
    mybar = st.progress(0)

    if percent > 100:
        st.subheader("Target done !")
    else:
        st.write("You have ",percent,"% ","of ",format(target, 'd'))
        for i in range(percent):
            time.sleep(0.1)
            mybar.progress(i+1, text = "Target Percentage")

def sideBar():
    with st.sidebar:
        selected = option_menu(
            menu_title="Main Menu",
            options=["Home","Progress"],
            icons = ["house","eye"],
            menu_icon="cast",
            default_index = 0
        )
    if selected == "Home":
            st.subheader(f"{selected}")
            Home()
            graphs()
    if selected == "Progress":
            st.subheader(f"{selected}")
            Progressbar()
            graphs() 
sideBar()
         

st.markdown("""
    <style>
        /* Background color */
        body {
            background-color: #f0f2f6 !important;
        }

        /* Sidebar styling */
        section[data-testid="stSidebar"] {
            background-color: #e0e0e0 !important;
        }

        /* Metrics box */
        div[data-testid="metric-container"] {
            background-color: #ffffff !important;
            border-radius: 10px !important;
            padding: 10px !important;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.1) !important;
        }

        /* Buttons */
        .stButton>button {
            background-color: #0083b8 !important;
            color: white !important;
            border-radius: 10px !important;
        }

        .stButton>button:hover {
            background-color: #005f7a !important;
        }
    </style>
""", unsafe_allow_html=True)

