from datetime import datetime
import json

import numpy as np
import matplotlib.pyplot as plt


HOURS = [str(x) for x in range(49)]
WEEKDAYS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']


def main():
    counts = np.zeros((len(WEEKDAYS), len(HOURS)))
    with open('activities.jsonl') as f:
        for line in f:
            ts = datetime.fromisoformat(json.loads(line)['timestamp'])
            counts[ts.weekday()][ts.hour * 2 + round(ts.minute / 30)] += 1

    fig, ax = plt.subplots()
    im = ax.imshow(counts, cmap="magma")

    # We want to show all ticks...
    ax.set_yticks(np.arange(len(WEEKDAYS)))
    ax.set_xticks(np.arange(len(HOURS)))
    # ... and label them with the respective list entries
    ax.set_yticklabels(WEEKDAYS)
    ax.set_xticklabels([int(h)/2 for h in HOURS])

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")

    ax.set_title("activities per weekday and hour")
    fig.tight_layout()
    plt.show()


if __name__ == '__main__':
    main()
