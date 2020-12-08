from datetime import datetime, timedelta
import json
from zoneinfo import ZoneInfo

# the limits to the count of sleeping hours
# these limits are excluded by the range!
MIN_SLEEP_HOUR = 21
MAX_WAKE_HOUR = 9
# ignore activities before this timestamp
MIN_TS = datetime(2018, 1, 1, tzinfo=ZoneInfo("Europe/Berlin"))


def main():
    active_hours = {}
    with open('activities.jsonl') as fr:
        for line in fr:
            ts = datetime.fromisoformat(json.loads(line)['timestamp'])
            if ts < MIN_TS:
                continue
            ref_date = ts.date()
            # consider as non-sleep every hour in the range containg an activity
            # also assign the hours before midnight to the following day
            if ts.hour > MIN_SLEEP_HOUR:
                ref_date += timedelta(days=1)
            elif ts.hour > MAX_WAKE_HOUR:
                continue
            if ref_date not in active_hours:
                active_hours[ref_date] = set()
            active_hours[ref_date].add(ts.hour)

    with open('sleeping_per_day.jsonl', 'w') as fw:
        for day, active_hours in active_hours.items():
            sleeping_hours = []
            for h in range(24):
                if h < MAX_WAKE_HOUR or h > MIN_SLEEP_HOUR:
                    if h not in active_hours:
                        sleeping_hours.append(h)

            fw.write(json.dumps(dict(
                day=day.isoformat(),
                sleeping_hours=sleeping_hours,
            )))
            fw.write('\n')

if __name__ == '__main__':
    main()
