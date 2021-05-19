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


  # current_hour = get_hour(frames[0])
  # current_idx = 0
  # frames_by_hours = [{"hour": current_hour, "frames": []}]

  # for frame in frames:
  #   hour = get_hour(frame)

  #   if hour == current_hour:
  #     frames_by_hours[current_idx]['frames'].append(frame)
  #   else:
  #     frames_by_hours.append({"hour": hour, "frames": [frame]})
  #     current_idx += 1
  #     current_hour = hour

  # return frames_by_hours

