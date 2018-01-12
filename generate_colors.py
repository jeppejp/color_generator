import grapefruit
import subprocess
import sys
#         black  red  green  yellow  blue  purple  cyan  white
# dark    0      1    2      3       4     5       6     7
# light   8      9    10     11      12    13      14    15

#         0      0    120    60      240   300     180   0

hues = [0, 0, 120, 60, 240, 300, 180, 0]
hues = hues*2

def write_html(colors, image, bg):
    with open('output.html', 'w') as fp:
        fp.write("<style>\n")
        for c in colors:
            fp.write("#%s {background-color: %s;}\n" % (c, colors[c]))
        fp.write(".block {width: 100px; height:100px; border: 1px solid black;float: left;}\n")
        fp.write("body {background-color: %s;}" %(bg))
        fp.write("img {margin: auto;}\n")
        fp.write("</style>\n")
        fp.write("<table><tr>\n")
        for i in range(0,8):
            fp.write("<td class=\"block\" id=\"color%s\"></td>" % (i))
        fp.write("</tr><td><img src=\"%s\" height=\"400\"></td></tr><tr>" % (image))
        for i in range(8,16):
            fp.write("<td class=\"block\" id=\"color%s\"></td>" % (i))
        fp.write("</tr></table>\n")

def extract_primary_color(image):
    cmd = "convert "+image+" -format %c -depth 8 histogram:info:-"
    out = subprocess.check_output(cmd.split())
    max_line = ""
    mx = 0
    for line in out.split("\n"):
        if len(line) > 30:
            cnt = line[:line.find(":")]
            val = int(cnt.strip())
            if val > mx:
                max_line = line
                mx = val
    ret = max_line[max_line.find("#"):]
    ret = ret[:ret.find(" ")]
    return ret
                
image = '720040_1.jpg'
image = sys.argv[1]
cols = {}

html_primary = extract_primary_color(image)
gcol = grapefruit.Color.NewFromHtml(html_primary)

(_, sat_primary, l_primary) = gcol.hsl

if l_primary < 0.5:
    l_dark = l_primary
    l_light = 1.0 - l_primary
else:
    l_dark = 1.0 - l_primary
    l_light = l_primary

if l_dark < 0.25:
    blah = l_dark
else:
    blah = 0.5-l_dark
#black
# 0.2
#    0.2  0.8
#    0.05 0.45 

white_light = 0.75 + blah
white_dark = 0.75 - blah
black_light = 0.25 + blah
black_dark = 0.25 - blah

lights = [l_dark]*8 + [l_light]*8
#white and black have sat =0
sats = [sat_primary]*16
sats[0] = 0
lights[0] = black_dark
sats[7] = 0 #white
lights[7] = white_dark
sats[8] = 0
lights[8] = black_light
sats[15] = 0 #white
lights[15] = white_light

for i in range(0,16):
    cols['color'+str(i)] = grapefruit.Color.NewFromHsl(hues[i], sats[i], lights[i]).html


write_html(cols, image, html_primary)
