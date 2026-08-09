from datetime import datetime
import os


CALENDAR_FOLDER = "calendar_events"

os.makedirs(CALENDAR_FOLDER, exist_ok=True)


def create_calendar_event(title, date, time):
    """
    Create a calendar event (.ics file)

    date format : YYYY-MM-DD
    time format : HH:MM (24-hour)
    """

    try:

        start = datetime.strptime(
            f"{date} {time}",
            "%Y-%m-%d %H:%M"
        )

        end = start.replace(hour=start.hour + 1)

        file_name = title.replace(" ", "_") + ".ics"

        file_path = os.path.join(
            CALENDAR_FOLDER,
            file_name
        )

        content = f"""BEGIN:VCALENDAR
VERSION:2.0
BEGIN:VEVENT
SUMMARY:{title}
DTSTART:{start.strftime('%Y/%m/%d T %H:%M00')}
DTEND:{end.strftime('%Y%m%dT%H%M00')}
END:VEVENT
END:VCALENDAR
"""

        with open(file_path, "w") as f:
            f.write(content)

        return f"Calendar event created successfully.\nSaved at: {file_path}"

    except Exception as e:

        return f"Calendar Error: {e}"