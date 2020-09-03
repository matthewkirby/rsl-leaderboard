def pretty_placement(i):
    if i == 1:
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