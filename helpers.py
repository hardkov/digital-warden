def get_hour(frame):
  return f"{frame['year']}_{frame['month']}_{frame['day']}_{frame['hour']}"

def get_frames_by_hours(frames):
  if len(frames) == 0:
    return []
    
  current_hour = get_hour(frames[0])
  current_idx = 0
  frames_by_hours = [{"hour": current_hour, "frames": []}]

  for frame in frames:
    hour = get_hour(frame)

    if hour == current_hour:
      frames_by_hours[current_idx]['frames'].append(frame)
    else:
      frames_by_hours.append({"hour": hour, "frames": [frame]})
      current_idx += 1
      current_hour = hour

  return frames_by_hours

