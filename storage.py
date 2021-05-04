saved_frames = []

def save_frame(date, encoded_frame):
    saved_frames.append({ "year": date.year, "month": date.month, "day": date.day, 
        "hour": date.hour, "src": f"data:image/jpg;base64,{encoded_frame}"})

def get_saved_frames():
    return saved_frames