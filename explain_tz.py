from datetime import datetime
import pytz

def explain_timezone_math():
    # Timestamp from user's data
    utc_timestamp_str = "2025-12-11T21:46:47.275850Z"
    
    # Parse as UTC
    utc_dt = datetime.fromisoformat(utc_timestamp_str.replace('Z', '+00:00'))
    
    # Convert to Asia/Kolkata
    ist_tz = pytz.timezone('Asia/Kolkata')
    ist_dt = utc_dt.astimezone(ist_tz)
    
    print(f"Raw UTC Timestamp: {utc_timestamp_str}")
    print(f"Parsed UTC Date:   {utc_dt.date()}")
    print(f"Converted IST Date:{ist_dt.date()}")
    print("-" * 30)
    
    if utc_dt.date() != ist_dt.date():
        print("CONCLUSION: The date CHANGES depending on the timezone.")
        print("In UTC, it is the 11th.")
        print("In IST, it is the 12th.")
    else:
        print("Dates are the same.")

if __name__ == "__main__":
    explain_timezone_math()
