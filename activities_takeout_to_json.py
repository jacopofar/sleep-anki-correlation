from html.parser import HTMLParser
import json
from zoneinfo import ZoneInfo

from datetime import datetime
# use a name that doesn't suck
parse_ts = datetime.strptime # NOQA


class ActivitiesHTMLParser(HTMLParser):
    def __init__(self, out):
        # necessary to initialize the parent class
        HTMLParser.__init__(self)
        # the description of the activity so far
        self.seen_data = []
        self.out = out

    def handle_data(self, data):
        try:
            ts = parse_ts(data, '%d.%m.%Y, %H:%M:%S MEZ').astimezone(ZoneInfo("Europe/Berlin"))
            print(ts)
            self.out.write(json.dumps(dict(
                timestamp=ts.isoformat(),
                description=self.seen_data
            )))
            self.out.write('\n')
            self.seen_data = []
        except ValueError:
            self.seen_data.append(data)


if __name__ == '__main__':
    with open('activities.jsonl', 'w') as fo:
        parser = ActivitiesHTMLParser(fo)
        parser.feed(open('MeineAktivitäten.html', 'rt').read())
    print('Done! Activities are stored in a JSONL file')
