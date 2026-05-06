# SYRO//RADIO

```
△ terminal-based radio for the machine mind
idm · synthwave · electronica · experimental · retrowave
```

<img width="644" height="296" alt="image" src="https://github.com/user-attachments/assets/540fe5d8-1ce5-4624-b703-e837b0146fae" />


---

## what is this

a terminal radio player that pulls free, ad-free streams from across the globe.  
no browser. no ads. no distractions. just signal.

built for studying, coding, and long nights staring at a screen.

---

## transmission sources

- **nightride.fm** — chillsynth · spacesynth · datawave · nightride
- **radio caprices** — idm
- **radio browser api** — worldwide idm, synthwave, electronica, experimental, retrowave, downtempo, atmospheric stations sorted by global vote count

---

## dependencies

```bash
sudo apt install mpv
pip3 install requests
```

> mpv handles the actual stream playback. requests talks to the radio browser api.

---

## usage

```bash
python3 radio.py
```

place `art.txt` and `radio.py` in the same folder.  
generate your own ascii art with:

```bash
sudo apt install jp2a
jp2a yourimage.png --width=38 --height=40 > art.txt
```

---

## controls

| key | action |
|-----|--------|
| `↑` `↓` | navigate stations |
| `page up` `page down` | jump 10 stations |
| `p` | transmit |
| `s` | silence |
| `q` | exit |

---

## how it works

1. on launch, pulls stations from [radio-browser.info](https://www.radio-browser.info) across 14 tags
2. filters out anything with vocals, lyrics, pop, rock, trance, house, edm, yoga, talk, news etc.
3. sorts remaining stations by global vote count
4. pins nightride.fm and radio caprices at the top
5. streams directly via mpv — no web player, no injected ads

---

## adding your own stations

find a direct stream url and add it to the `manual` list in `radio.py`:

```python
manual = [
    {"name": "Your Station", "url_resolved": "https://stream.url/stream.mp3", "bitrate": 128, "countrycode": "US", "votes": 9999},
    ...
]
```

stations in the manual list are always pinned to the top.

---

## filter logic


only passes through: idm · braindance · glitch · electronica · synthwave  
chillsynth · darksynth · retrowave · spacesynth · outrun · ambient · downtempo · atmospheric

---

## inspired by

- aphex twin
- nightride.fm
- hunter.fm
- the radio browser project
- too many late nights

---

## license

do whatever you want with it.  
just don't copy me

```
