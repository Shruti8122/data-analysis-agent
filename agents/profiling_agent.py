from ydata_profiling import ProfileReport

def generate_profile(df):
    profile = ProfileReport(df, minimal=True)
    profile.to_file("reports/report.html")