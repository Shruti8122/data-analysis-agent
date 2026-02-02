from ydata_profiling import ProfileReport
import os

def generate_profile(df):
    os.makedirs("reports", exist_ok=True)
    profile = ProfileReport(df, minimal=True)
    profile.to_file("reports/report.html")
