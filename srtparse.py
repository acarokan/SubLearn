from srt import parse

def get_subtitles(filename):
    with open(filename,"r") as f:
        data = parse(f.read())
    return data