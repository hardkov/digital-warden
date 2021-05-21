from datetime import date
from numpy import split

def parse_frames(frames):
  if len(frames) == 0:
    return []
    
  current_date = date.fromtimestamp(frames[0]["created_at"])
  current_idx = 0
  frames_by_date = [{"date": str(current_date), "frames": []}]

  for frame in frames:
    new_date = date.fromtimestamp(frame["created_at"])

    if new_date == current_date:
      frames_by_date[current_idx]["frames"].append(frame)
    else:
      frames_by_date.append({"date": str(new_date), "frames": [frame]})
      current_idx += 1
      current_date = new_date

  return frames_by_date

