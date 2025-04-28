import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF
import os

# Title
st.title("📊 Student Details Analysis Report")

# Upload CSV
uploaded_file = st.file_uploader("📥 Upload your Student CSV file", type=['csv'])

# Function to generate PDF report
def generate_pdf_with_charts(dataframe):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="Student Analysis Report", ln=True, align="C")
    pdf.ln(10)

    # Add student data
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Student Details", ln=True, align="L")
    for idx in range(len(dataframe)):
        student = dataframe.iloc[idx]
        line = f"{student.get('Name', 'N/A')} | {student.get('Department', 'N/A')} | {student.get('Course', 'N/A')} | {student.get('Marks', 'N/A')}"
        pdf.cell(200, 10, txt=line, ln=True, align="L")
    
    pdf.ln(10)

    # Add Summary Statistics
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Summary Statistics", ln=True, align="L")
    summary_stats = dataframe.describe().transpose()
    for column, row in summary_stats.iterrows():
        line = f"{column}: {row['mean']} (mean), {row['std']} (std), {row['min']} (min), {row['25%']} (25%), {row['50%']} (50%), {row['75%']} (75%), {row['max']} (max)"
        pdf.cell(200, 10, txt=line, ln=True, align="L")
    
    pdf.ln(10)

    # Department Chart
    if 'Department' in dataframe.columns:
        dept_counts = dataframe['Department'].value_counts()
        plt.figure(figsize=(6,4))
        dept_counts.plot(kind='bar', color='skyblue')
        plt.title('Number of Students per Department')
        plt.ylabel('Number of Students')
        plt.xticks(rotation=45)
        dept_chart_path = "/tmp/dept_chart.png"
        plt.tight_layout()
        plt.savefig(dept_chart_path)
        plt.close()
        
        pdf.add_page()
        pdf.cell(200, 10, txt="Department Distribution", ln=True, align="C")
        pdf.image(dept_chart_path, x=10, y=30, w=180)

    # Course Chart
    if 'Course' in dataframe.columns and 'Marks' in dataframe.columns:
        avg_marks = dataframe.groupby('Course')['Marks'].mean()
        plt.figure(figsize=(6,4))
        avg_marks.plot(kind='bar', color='lightgreen')
        plt.title('Average Marks per Course')
        plt.ylabel('Average Marks')
        plt.xticks(rotation=45)
        course_chart_path = "/tmp/course_chart.png"
        plt.tight_layout()
        plt.savefig(course_chart_path)
        plt.close()
        
        pdf.add_page()
        pdf.cell(200, 10, txt="Average Marks per Course", ln=True, align="C")
        pdf.image(course_chart_path, x=10, y=30, w=180)

    # Save PDF
    output_path = "/tmp/student_full_report.pdf"
    pdf.output(output_path)

    # Cleanup temporary images
    if os.path.exists(dept_chart_path):
        os.remove(dept_chart_path)
    if os.path.exists(course_chart_path):
        os.remove(course_chart_path)

    return output_path

# Check if file is uploaded and process it
if uploaded_file is not None:
    # Read CSV
    df = pd.read_csv(uploaded_file)
    st.success('✅ File Uploaded Successfully!')

    # Show data preview
    st.markdown("---")
    st.header("📂 Uploaded Student Data")
    st.dataframe(df)

    # Generate PDF report with charts
    st.markdown("---")
    if st.button('📄 Generate PDF Report'):
        pdf_file = generate_pdf_with_charts(df)
        
        # Allow the user to download the generated PDF
        with open(pdf_file, "rb") as f:
            st.download_button('⬇️ Download Full Report (with Charts)', f, file_name="student_full_report.pdf")
else:
    st.info('👆 Please upload a CSV file to get started.')
