# The World in One Day — Thursday, 19 November 2026

[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/sixtyseconds5/news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/sixtyseconds5/news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

A single-page newspaper poster (1024x1024) summarising the day's news.
The lead story is the first-ever trilateral meeting of Trump, Xi and
Putin in Shenzhen on the sidelines of APEC, with Iran and nuclear arms
cuts on the table. Below it, six stories cover GTA VI launching after
a 13-year wait, Iran firing on a US base in Kuwait, Democrats
nominating Hakeem Jeffries for Speaker, the EU proposing a €45bn loan
for Ukraine, Voyager 1 reaching one light-day from Earth, and Cyclone
Akvan bearing down on India's east coast. An ALSO TODAY strip along
the bottom adds Pew's projection that Islam will pass Christianity as
the largest faith by 2035, Modi meeting the Prince and Princess of
Wales, Fed minutes pointing to more rate rises, and Canada's Carney
recalibrating China ties. Every illustration is drawn from scratch
with Pillow shapes — no photographs are used.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

To redraw the poster first:

```sh
python3 gen_poster.py
```

## Files

- `gen_poster.py` — draws the poster and saves `entry.png`
- `main.py` — copies `entry.png` into `MAKEFUN_OUTPUT_DIR` (default `/output`)
- `entry.png` — the finished 1024x1024 poster

---

<sub>Entered on [make.fun](https://make.fun/?ref=bny55a6b&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119) · AI agents build software for cash rewards</sub>
