from datetime import datetime as dt

def pretty_placement(i):
    if i is None:
        return '&ndash;'
    elif i == 1:
        return "<div class=\"first-place\">1st</div>"
    elif i == 2:
        return "<div class=\"second-place\">2nd</div>"
    elif i == 3:
        return "<div class=\"third-place\">3rd</div>"
    else:
        return f"{i}th"

def should_i_plural(string, i):
    if string == 'Finish':
        return f"{i} {string}" if i == 1 else f"{i} {string}es"
    elif string == 'Race':
        return f"{i} {string}" if i == 1 else f"{i} {string}s"


def name_with_link(player):
    url = f"https://racetime.gg/user/{player.id}"
    return f"<a href={url} class=\"a-table\">{player.display_name}</a>"


def format_delta(num):
    div = "<div class=\"positive-delta\">" if num >= 0 else "<div class=\"negative-delta\">"
    return div+'+'+str(num)+"</div>" if num >= 0 else div+str(num)+"</div>"

def slug_with_link(slug):
    url = f"https://racetime.gg/ootr/{slug}"
    return f"<a href={url} class=\"a-table\">{slug}</a>"

def pretty_finish_time(raw_time):
    """ This function is super jank, but it works *shrug* """
    if raw_time is None:
        return 'Forfeit'
    
    h, m, s = "", "", ""
    counth, countm, counts = False, False, False
    for c in raw_time:
        if c == 'T':
            counth = True
            continue
        elif c == 'H':
            counth = False
            countm = True
            continue
        elif c == 'M':
            countm = False
            counts = True
            continue
        elif c == 'S':
            break
    
        if counth:
            h += c
        elif countm:
            m += c
        elif counts:
            s += c
        
    return f"{int(h)}:{str(int(m)).zfill(2)}:{str(int(float(s))).zfill(2)}"

def pretty_race_date(raw_date):
    date = dt.fromisoformat(raw_date[:-1])
    return date.strftime("%B %d, %Y")