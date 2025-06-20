from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import pandas as pd
from datetime import datetime
import os

def generate_pdf_report(cleaned_path, forecast_path, output_path="crime_report.pdf"):
    df = pd.read_csv(cleaned_path)
    forecast = pd.read_csv(forecast_path)

    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "📄 Pakistan Crime Analytics Report")

    c.setFont("Helvetica", 11)
    c.drawString(50, height - 80, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    c.drawString(50, height - 100, "Data source: Government Crime Data (2010–2020)")

    c.setFont("Helvetica-Bold", 13)
    c.drawString(50, height - 140, "🔍 Top 5 Reported Crimes (2010–2020):")
    top5 = df.drop("Year", axis=1).sum().sort_values(ascending=False).head(5)

    y = height - 160
    c.setFont("Helvetica", 11)
    for crime, value in top5.items():
        c.drawString(60, y, f"- {crime}: {int(value):,} cases")
        y -= 15

    c.setFont("Helvetica-Bold", 13)
    c.drawString(50, y - 20, "📈 Forecast Highlights (2021–2025):")
    y -= 40
    for crime in top5.index:
        predicted = forecast[
            (forecast["Crime Type"] == crime) & 
            (forecast["ds"].str.startswith("2025"))
        ]
        if not predicted.empty:
            cases = int(predicted["Predicted Cases"].values[0])
            c.drawString(60, y, f"- {crime} (2025 forecast): {cases:,} cases")
            y -= 15

    c.setFont("Helvetica-Bold", 13)
    c.drawString(50, y - 20, "🧠 Clustering Insight:")
    c.setFont("Helvetica", 11)
    c.drawString(60, y - 40, "- Similar crime types were grouped using KMeans + PCA.")
    c.drawString(60, y - 55, "- Theft-related crimes were clustered due to rising frequency.")
    c.drawString(60, y - 70, "- Murder & Dacoity showed distinct declining behavior.")

    c.setFont("Helvetica-Oblique", 10)
    c.drawString(50, 40, "© 2025 Anas | Built with Python, Streamlit, Prophet, ReportLab")

    c.save()
    print(f"✅ PDF report saved as: {output_path}")
