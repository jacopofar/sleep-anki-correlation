from datetime import datetime
import json

import numpy as np
import matplotlib.pyplot as plt

ANKI_BINS = 40
SLEPT_HOURS = [str(x) for x in range(11)]
ANKI_PERF = [str(x / (ANKI_BINS / 4)) for x in range(ANKI_BINS)]


def main():
    counts = np.zeros((len(SLEPT_HOURS), len(ANKI_PERF)))
    sleep_hours = {}
    with open('sleeping_per_day.jsonl') as f:
        for line in f:
            # {"day": "2020-12-03", "sleeping_hours": [5, 6]}
            obj = json.loads(line)
            sleep_hours[obj['day']] = len(obj['sleeping_hours'])

    days = []
    hours_slept = []
    anki_perfs = []
    # NOTE: the file is sorted by date
    with open('anki_daily_performance.jsonl') as f:
        for line in f:
            # {"day": "2020-12-08", "avg_ease": 2.2988505747126435}
            obj = json.loads(line)
            if obj['day'] not in sleep_hours:
                continue
            perf = obj['avg_ease'] * ANKI_BINS / 4 - 1
            slept_that_day = int(sleep_hours[obj['day']])
            counts[slept_that_day][int(perf)] += 1

            days.append(obj['day'])
            hours_slept.append(slept_that_day)
            anki_perfs.append(perf * 4)
    correlation = np.corrcoef(hours_slept, anki_perfs)[0][1]
    print('Pearson correlation:', correlation)
    fig, ax = plt.subplots()
    im = ax.imshow(counts, cmap="magma")

    # We want to show all ticks...
    ax.set_xticks(np.arange(len(ANKI_PERF)))
    ax.set_yticks(np.arange(len(SLEPT_HOURS)))
    # ... and label them with the respective list entries
    ax.set_xticklabels(ANKI_PERF)
    ax.set_yticklabels(SLEPT_HOURS)

    # ignore values that never appear
    ax.set_xlim(1.5 * ANKI_BINS / 4, 3.5 * ANKI_BINS / 4)

    ax.set_ylabel('estimated sleep hours')
    ax.set_xlabel('average Anki ease for old cards')


    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
            rotation_mode="anchor")


    ax.set_title(f"Sleep and Anki performance correlation ({correlation:.4f})")
    fig.tight_layout()
    plt.gca().invert_yaxis()
    plt.show()


if __name__ == '__main__':
    main()
