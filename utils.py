from datetime import datetime
import pytz

IST = pytz.timezone('Asia/Kolkata')

def convert_to_ist(dt: datetime) -> datetime:
    return dt.astimezone(IST)
