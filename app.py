import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
cleaned_path = os.path.join(BASE_DIR, "Dataset", "cleaned_crime_data.csv")
forecast_path = os.path.join(BASE_DIR, "Dataset", "forecasted_crime_2021_2025.csv")



df = pd.read_csv(cleaned_path)
forecast_df = pd.read_csv(forecast_path)
forecast_df['ds'] = pd.to_datetime(forecast_df['ds'])

st.title("🇵🇰 Pakistan Crime Analytics & Forecasting System")
st.markdown("Explore crime trends (2010–2020) and forecasted crimes (2021–2025)")

# Sidebar
crime_list = df.columns[1:]
selected_crime = st.sidebar.selectbox("Select a Crime", crime_list)

# Line chart for trend
st.subheader(f"📈 Yearly Trend: {selected_crime}")
fig = px.line(df, x='Year', y=selected_crime, markers=True)
st.plotly_chart(fig, use_container_width=True)

# Forecast
st.subheader(f"🔮 Forecast (2021–2025): {selected_crime}")
crime_forecast = forecast_df[forecast_df["Crime Type"] == selected_crime]
fig2 = px.line(crime_forecast, x="ds", y="Predicted Cases", markers=True)
st.plotly_chart(fig2, use_container_width=True)

# Top crimes chart
st.subheader("🔥 Top 5 Crimes by Total Reports (2010–2020)")
top5 = df[crime_list].sum().sort_values(ascending=False).head(5)
st.bar_chart(top5)

# About
st.markdown("---")
st.caption("Built by Anas | Data Source: Government of Pakistan")

from generate_report import generate_pdf_report

generate_pdf_report(
    cleaned_path=r"C:\Users\DELL\Desktop\Pakistan Crime Analytics & Forecasting System\Dataset\cleaned_crime_data.csv",
    forecast_path=r"C:\Users\DELL\Desktop\Pakistan Crime Analytics & Forecasting System\Dataset\forecasted_crime_2021_2025.csv",
    output_path=r"C:\Users\DELL\Desktop\Pakistan Crime Analytics & Forecasting System\crime_report.pdf"
)
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from io import BytesIO
from datetime import datetime

def generate_pdf_download():
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "Pakistan Crime Analytics Report")
    c.setFont("Helvetica", 11)
    c.drawString(50, height - 80, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

    # Summary section
    top5 = df.drop("Year", axis=1).sum().sort_values(ascending=False).head(5)
    y = height - 130
    c.setFont("Helvetica-Bold", 13)
    c.drawString(50, y, "Top 5 Crimes (2010–2020):")
    y -= 20
    c.setFont("Helvetica", 11)
    for crime, val in top5.items():
        c.drawString(60, y, f"- {crime}: {int(val):,} cases")
        y -= 15

    # Forecast
    y -= 20
    c.setFont("Helvetica-Bold", 13)
    c.drawString(50, y, "Forecast for 2025:")
    y -= 20
    for crime in top5.index:
        pred = forecast_df[
            (forecast_df["Crime Type"] == crime) & 
            (forecast_df["ds"].dt.year == 2025)
        ]
        if not pred.empty:
            val = int(pred["Predicted Cases"].values[0])
            c.setFont("Helvetica", 11)
            c.drawString(60, y, f"- {crime}: {val:,} cases")
            y -= 15

    # Footer
    c.setFont("Helvetica-Oblique", 10)
    c.drawString(50, 40, "© 2025 Anas | Built with Python, Streamlit, Prophet, ReportLab")
    c.save()
    buffer.seek(0)
    return buffer

