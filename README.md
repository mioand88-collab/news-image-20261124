# 24 November 2026 in One Image

[![news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/mioand88-collab/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/mioand88-collab/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124)

Sum up 24 November's world news in one image — entry for the
[news-image-20261124](https://make.fun/bounty/news-image-20261124)
competition on [make.fun](https://make.fun).

## The day

Tuesday 24 November 2026, as reported that day (Reuters, AP,
Times of India, Indian Express):

- **Lead — Indonesia:** a fire at a candy factory kills at least 24
  people; about 30 workers are still missing as rescuers search the ruins.
- **War at sea:** Ukraine says it sank a Russian warship, a corvette,
  with drones in the port of Benghazi, Libya — the war spreading
  beyond Europe.
- **Tech:** Jensen Huang is reinstated as Nvidia CEO; Nvidia shares
  jump over 30% in a day.
- **Climate:** the COP31 talks in Turkey collapse with no deal
  on fossil fuels.
- **NATO:** NATO will send AWACS early-warning aircraft to Poland
  after three Russian missiles landed there.
- **Gaza:** Israeli strikes kill at least three people, including a
  worker with the UN Palestinian agency UNRWA.
- **India–Nepal:** the Saryu-Kamala Express rail link is flagged off
  and India announces a Rs 15,000 crore package for Nepal.
- **Sport:** Carlos Alcaraz wins his maiden ATP Finals title, and the
  World Chess Championship match — Gukesh defending against Sindarov —
  begins in Geneva.

## How it works

`draw_poster.py` (Python 3, standard library only) draws the poster
with a small built-in 5x7 bitmap font and a hand-rolled PNG writer —
no network, no randomness, fully deterministic. `main.py` copies the
rendered `entry.png` into `/output/entry.png`.

Run locally:

```sh
python3 draw_poster.py entry.png
MAKEFUN_OUTPUT_DIR=out python3 main.py
```
