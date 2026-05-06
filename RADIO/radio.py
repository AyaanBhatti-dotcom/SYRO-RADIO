import subprocess
import requests
import random
import curses

def load_art():
    try:
        with open("art.txt", "r") as f:
            lines = f.readlines()
        return [line.rstrip() for line in lines]
    except:
        return []

def fetch_stations(tag, limit=20):
    try:
        servers = ["de1.api.radio-browser.info", "nl1.api.radio-browser.info", "at1.api.radio-browser.info"]
        base = random.choice(servers)
        url = f"https://{base}/json/stations/bytag/{tag}"
        r = requests.get(url, params={"limit": limit, "hidebroken": True, "order": "votes"}, timeout=5)
        return r.json()
    except:
        return []

def filter_stations(stations):
    blocked_keywords = [
        "yoga", "meditation", "sleep", "spa", "nature sounds", "christian",
        "gospel", "talk", "news", "sport", "dance", "party", "pop", "hip hop",
        "hiphop", "rap", "country", "reggae", "latin", "vocal", "vocals",
        "singer", "lyrics", "top 40", "hits", "charts", "comedy", "podcast",
        "audiobook", "children", "kids", "religious", "worship", "praise",
        "rock", "metal", "punk", "rnb", "r&b", "soul", "blues", "folk",
        "indie", "alternative", "grunge", "disco", "funk", "techno", "trance",
        "house", "edm", "dubstep", "drum and bass", "dnb", "trap",
        "jazz vocals", "smooth jazz", "bossa nova", "flamenco", "opera",
        "musical", "broadway", "classical", "piano", "neoclassical", "jazz",
        "lofi", "lo-fi", "study", "focus", "nature", "acoustic",
        "minimalism", "postminimal", "generative", "microsound",
        "dark ambient", "drone", "chillout"
    ]

    allowed = []
    seen_urls = set()
    seen_names = set()

    for s in stations:
        name = s.get("name", "").lower()
        tags = s.get("tags", "").lower()
        combined = name + " " + tags
        url = s.get("url_resolved") or s.get("url", "")
        bitrate = int(s.get("bitrate", 0))

        if not url:
            continue
        if url in seen_urls:
            continue
        if name in seen_names:
            continue
        if any(b in combined for b in blocked_keywords):
            continue
        if bitrate == 0:
            continue

        allowed.append(s)
        seen_urls.add(url)
        seen_names.add(name)

    return allowed

def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(False)
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_CYAN, -1)
    curses.init_pair(2, curses.COLOR_GREEN, -1)
    curses.init_pair(3, curses.COLOR_WHITE, -1)
    curses.init_pair(4, curses.COLOR_YELLOW, -1)
    curses.init_pair(5, curses.COLOR_MAGENTA, -1)

    art_lines = load_art()

    stdscr.clear()
    stdscr.addstr(0, 0, "SYRO//RADIO — scanning global frequencies...", curses.color_pair(5))
    stdscr.refresh()

    tags = [
        "idm", "braindance", "glitch", "electronica",
        "experimental", "synthwave", "chillsynth", "darksynth",
        "retrowave", "spacesynth", "outrun", "ambient",
        "downtempo", "atmospheric"
    ]

    raw = []
    for tag in tags:
        raw += fetch_stations(tag, limit=20)

    stations = filter_stations(raw)
    stations.sort(key=lambda s: int(s.get("votes", 0)), reverse=True)
    stations = stations[:56]

    manual = [
        {"name": "Nightride.fm — ChillSynth", "url_resolved": "https://stream.nightride.fm/chillsynth.mp3",  "bitrate": 320, "countrycode": "US", "votes": 9999},
        {"name": "Nightride.fm — SpaceSynth", "url_resolved": "https://stream.nightride.fm/spacesynth.mp3",  "bitrate": 320, "countrycode": "US", "votes": 9999},
        {"name": "Nightride.fm — DataWave",   "url_resolved": "https://stream.nightride.fm/datawave.mp3",    "bitrate": 320, "countrycode": "US", "votes": 9999},
        {"name": "Nightride.fm — NightRide",  "url_resolved": "https://stream.nightride.fm/nightride.mp3",   "bitrate": 320, "countrycode": "US", "votes": 9999},
        {"name": "Radio Caprices — IDM",      "url_resolved": "http://79.111.14.76:8000/idm",                "bitrate": 128, "countrycode": "RU", "votes": 9999},
    ]

    stations = manual + stations

    if not stations:
        stdscr.addstr(2, 0, "No stations found. Check your connection.")
        stdscr.getch()
        return

    current = 0
    offset = 0
    playing = False
    process = None
    status = "ready"

    while True:
        stdscr.clear()
        h, w = stdscr.getmaxyx()

        art_width = 42
        divider_col = art_width + 1
        list_col = divider_col + 2
        list_width = w - list_col - 1

        for i, line in enumerate(art_lines):
            if i >= h - 1:
                break
            try:
                stdscr.addstr(i, 0, line[:art_width], curses.color_pair(5))
            except:
                pass

        for row in range(h - 1):
            try:
                stdscr.addstr(row, divider_col, "│", curses.color_pair(5))
            except:
                pass

        row = 0
        sep = "─" * list_width

        try:
            stdscr.addstr(row, list_col, "△  SYRO//RADIO"[:list_width], curses.color_pair(5)); row += 1
            stdscr.addstr(row, list_col, "idm · synthwave · electronica · experimental"[:list_width], curses.color_pair(1)); row += 1
            stdscr.addstr(row, list_col, sep[:list_width], curses.color_pair(5)); row += 1
        except:
            pass

        list_rows = h - row - 4
        if list_rows < 1:
            list_rows = 1

        if current < offset:
            offset = current
        elif current >= offset + list_rows:
            offset = current - list_rows + 1

        for i in range(offset, min(offset + list_rows, len(stations))):
            s = stations[i]
            name = s.get("name", "Unknown")
            bitrate = s.get("bitrate", "?")
            country = s.get("countrycode", "??")
            is_current = i == current
            is_playing = is_current and playing
            prefix = "▶ " if is_current else "  "
            marker = " ◉" if is_playing else ""
            line = f"{prefix}{i+1:02}. {name} [{country}] [{bitrate}k]{marker}"

            if is_playing:
                color = curses.color_pair(2)
            elif is_current:
                color = curses.color_pair(4)
            else:
                color = curses.color_pair(3)

            try:
                stdscr.addstr(row, list_col, line[:list_width], color)
            except:
                pass
            row += 1

        try:
            scroll_info = f"[{current+1}/{len(stations)}]"
            stdscr.addstr(row, list_col, sep[:list_width], curses.color_pair(5)); row += 1
            status_line = f"{'◉ ' + status if playing else status}"
            stdscr.addstr(row, list_col, status_line[:list_width], curses.color_pair(1)); row += 1
            stdscr.addstr(row, list_col, sep[:list_width], curses.color_pair(5)); row += 1
            stdscr.addstr(row, list_col, f"[↑↓] nav  [p] play  [s] stop  [q] quit  {scroll_info}"[:list_width], curses.color_pair(5))
        except:
            pass

        stdscr.refresh()
        key = stdscr.getch()

        if key == ord('q'):
            if process:
                process.terminate()
            break
        elif key == curses.KEY_UP:
            current = (current - 1) % len(stations)
        elif key == curses.KEY_DOWN:
            current = (current + 1) % len(stations)
        elif key == curses.KEY_PPAGE:
            current = max(0, current - 10)
        elif key == curses.KEY_NPAGE:
            current = min(len(stations) - 1, current + 10)
        elif key == ord('p'):
            if process:
                process.terminate()
            url = stations[current].get("url_resolved") or stations[current].get("url")
            name = stations[current].get("name", "Unknown")
            country = stations[current].get("countrycode", "??")
            status = f"transmitting: {name} [{country}]"
            process = subprocess.Popen(
                ["mpv", "--no-video", "--really-quiet",
                 "--cache=yes",
                 "--cache-secs=10",
                 "--demuxer-max-bytes=50M",
                 "--demuxer-readahead-secs=10",
                 url],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            playing = True
        elif key == ord('s'):
            if process:
                process.terminate()
                process = None
            playing = False
            status = "signal lost — press [p] to retransmit"

if __name__ == "__main__":
    curses.wrapper(main)
