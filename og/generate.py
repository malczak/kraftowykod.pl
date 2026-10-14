"""
Generator obrazków Open Graph dla Kraftowy Kod.

Tak, to jest skrypt. Nie, nie jest to automatyzacja: każdą współrzędną
Tadeusz policzył na kartce, a Mateusz przepisał. Skrypt tylko składa SVG
i oddaje go do rsvg-convert, bo PNG ręcznie rysować nie umiemy (jeszcze).

Uruchomienie (z katalogu repozytorium):
    python3 og/generate.py

Wymaga: rsvg-convert (brew install librsvg) oraz fontów systemowych
Rockwell, Georgia i Bradley Hand (macOS ma je w standardzie).
"""

import pathlib
import subprocess
from xml.sax.saxutils import escape

OUT = pathlib.Path(__file__).parent
W, H = 1200, 630

KRAFT = '#c9a676'
INK = '#2b1d10'
LABEL = '#f1e6cf'
HOP = '#3d5726'
PENCIL = '#a3281c'

DISPLAY = "Rockwell, Georgia, serif"
BODY = "Georgia, serif"
HAND = "'Bradley Hand', 'Noteworthy', cursive"

# kapsel z logo, ten sam co na stronie, tylko skalowany
CAP_PATH = ('M32 2l4 4 5-2 3 5 5 0 1 5 5 2-1 5 4 4-3 4 3 4-4 4 1 5-5 2-1 5-5 0-3 5-5-2-4 4-4-4-5 2-3-5'
            '-5 0-1-5-5-2 1-5-4-4 3-4-3-4 4-4-1-5 5-2 1-5 5 0 3-5 5 2z')


def t(text):
    return escape(text)


def paper(fill):
    # włókna papieru, jak na stronie
    lines = []
    for x in range(-200, W + 200, 9):
        lines.append(f'<line x1="{x}" y1="0" x2="{x + 33}" y2="{H}" stroke="{INK}" stroke-opacity="0.035" stroke-width="1"/>')
    return f'<rect width="{W}" height="{H}" fill="{fill}"/>' + ''.join(lines)


def cap(x, y, size):
    s = size / 64
    return f'''<g transform="translate({x} {y}) scale({s})">
  <path d="{CAP_PATH}" fill="{HOP}"/>
  <circle cx="32" cy="32" r="20" fill="{LABEL}"/>
  <text x="32" y="39.5" text-anchor="middle" font-family="{BODY}" font-weight="bold" font-size="20" fill="{INK}">{{<tspan fill="{PENCIL}">;</tspan>}}</text>
</g>'''


def brand(x, y, tagline):
    return cap(x, y, 92) + f'''
<text x="{x + 112}" y="{y + 52}" font-family="{DISPLAY}" font-weight="bold" font-size="54" fill="{INK}">Kraftowy Kod</text>
<text x="{x + 114}" y="{y + 88}" font-family="{HAND}" font-size="28" fill="{INK}">{t(tagline)}</text>'''


def stamp(cx, cy, r, big, small):
    return f'''<g transform="translate({cx} {cy}) rotate(-14)" fill="none" stroke="{PENCIL}">
  <circle r="{r}" stroke-width="7"/>
  <circle r="{r - 12}" stroke-width="3"/>
  <text y="6" text-anchor="middle" font-family="{DISPLAY}" font-weight="bold" font-size="{r * 0.5:.0f}" fill="{PENCIL}" stroke="none">{t(big)}</text>
  <text y="{r * 0.42:.0f}" text-anchor="middle" font-family="{HAND}" font-size="{r * (0.3 if len(small) <= 10 else 0.25):.0f}" fill="{PENCIL}" stroke="none">{t(small)}</text>
</g>'''


def ribbon(text):
    return f'''<rect y="{H - 58}" width="{W}" height="58" fill="{INK}"/>
<rect y="{H - 64}" width="{W}" height="6" fill="{HOP}"/>
<text x="{W / 2}" y="{H - 20}" text-anchor="middle" font-family="{HAND}" font-size="28" fill="{LABEL}">{t(text)}</text>'''


def notebook(x, y, w, h, lines, caption):
    step = 38
    rules = ''.join(
        f'<line x1="0" y1="{yy}" x2="{w}" y2="{yy}" stroke="{HOP}" stroke-opacity="0.28" stroke-width="1.5"/>'
        for yy in range(30 + step, h, step)
    )
    code = []
    for i, (text, kind) in enumerate(lines):
        yy = 30 + step * (i + 1) - 9
        if kind == 'comment':
            code.append(f'<text x="64" y="{yy}" fill="{HOP}">{t(text)}</text>')
        elif kind == 'strike':
            struck, note = text
            end = 76 + len(struck) * 11
            code.append(f'<text x="76" y="{yy}" fill="{INK}">{t(struck)}</text>')
            code.append(f'<line x1="72" y1="{yy - 9}" x2="{end}" y2="{yy - 11}" stroke="{PENCIL}" stroke-width="3.5"/>')
            code.append(f'<text x="{end + 22}" y="{yy}" fill="{PENCIL}" font-weight="bold">{t(note)}</text>')
        else:
            code.append(f'<text x="64" y="{yy}" fill="{INK}" xml:space="preserve">{t(text)}</text>')
    return f'''<g transform="translate({x} {y}) rotate(-2)">
  <rect x="8" y="8" width="{w}" height="{h}" fill="{INK}" fill-opacity="0.3"/>
  <rect width="{w}" height="{h}" fill="{LABEL}"/>
  {rules}
  <line x1="48" y1="0" x2="48" y2="{h}" stroke="{PENCIL}" stroke-opacity="0.5" stroke-width="1.5"/>
  <circle cx="{w - 70}" cy="{h - 60}" r="52" fill="none" stroke="#784818" stroke-opacity="0.25" stroke-width="7"/>
  <g font-family="{HAND}" font-size="25">{''.join(code)}</g>
  <text x="{w}" y="{h + 34}" text-anchor="end" font-family="{HAND}" font-size="22" fill="{INK}">{t(caption)}</text>
</g>'''


def svg(body):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">{body}</svg>'


def code_card(c):
    body = paper(KRAFT)
    body += brand(56, 44, c['tagline'])
    body += f'''
<text x="60" y="262" font-family="{DISPLAY}" font-weight="bold" font-size="46" fill="{INK}">{t(c['headline'][0])}</text>
<text x="60" y="316" font-family="{DISPLAY}" font-weight="bold" font-size="46" fill="{INK}">{t(c['headline'][1])}</text>
<text x="62" y="378" font-family="{HAND}" font-size="31" fill="{HOP}">{t(c['unique'])}</text>
<text x="62" y="440" font-family="{BODY}" font-size="23" fill="{INK}">{t(c['lede'][0])}</text>
<text x="62" y="472" font-family="{BODY}" font-size="23" fill="{INK}">{t(c['lede'][1])}</text>
<text x="62" y="504" font-family="{BODY}" font-size="23" fill="{INK}">{t(c['lede'][2])}</text>'''
    body += notebook(640, 150, 500, 352, c['code'], c['caption'])
    body += stamp(1080, 118, 78, c['stamp'][0], c['stamp'][1])
    body += ribbon(c['ribbon'])
    return svg(body)


def manifesto_card(c):
    body = paper(LABEL)
    body += f'<rect x="20" y="20" width="{W - 40}" height="{H - 104}" fill="none" stroke="{INK}" stroke-width="3"/>'
    body += f'<rect x="28" y="28" width="{W - 56}" height="{H - 120}" fill="none" stroke="{INK}" stroke-width="1.5"/>'
    body += brand(56, 46, c['tagline'])
    body += f'''
<text x="62" y="206" font-family="{HAND}" font-size="28" fill="{PENCIL}">{t(c['eyebrow'])}</text>
<text x="60" y="262" font-family="{DISPLAY}" font-weight="bold" font-size="52" fill="{INK}">{t(c['title'])}</text>'''
    y = 330
    for numeral, (line1, line2) in c['articles']:
        body += f'''
<text x="62" y="{y}" font-family="{DISPLAY}" font-weight="bold" font-size="34" fill="{HOP}">{numeral}</text>
<text x="150" y="{y}" font-family="{BODY}" font-size="25" fill="{INK}">{t(line1)}</text>
<text x="150" y="{y + 32}" font-family="{BODY}" font-size="25" fill="{INK}">{t(line2)}</text>'''
        y += 82
    # podpisy jeden pod drugim, każdy pod innym kątem, bo każdy podpisywał po swojemu
    body += f'''
<text x="880" y="322" font-family="{BODY}" font-size="20" fill="{INK}">{t(c['signed'])}</text>
<text x="890" y="378" font-family="{HAND}" font-size="38" fill="{INK}" transform="rotate(-3 890 378)">Tadeusz</text>
<text x="920" y="432" font-family="{HAND}" font-size="38" fill="{INK}" transform="rotate(2 920 432)">Zacheusz</text>
<text x="880" y="500" font-family="{HAND}" font-size="38" fill="{INK}" transform="rotate(-4 880 500)">Mateusz</text>
<text x="1028" y="498" font-family="{HAND}" font-size="20" fill="{INK}" transform="rotate(-4 880 500)">{t(c['interns'])}</text>'''
    body += stamp(1060, 150, 84, c['stamp'][0], c['stamp'][1])
    body += ribbon(c['ribbon'])
    return svg(body)


PL = {
    'tagline': 'warzelnia oprogramowania · od 2014',
    'headline': ('Kod długo dojrzewający', 'w naszych głowach.'),
    'unique': 'Jedyny taki software house w Polsce.',
    'lede': ('Warzymy oprogramowanie ręcznie,', 'w małych partiach. Bez sztucznej', 'inteligencji. Bez sztucznych terminów.'),
    'code': [
        ('// pisane 14.03, po kawie', 'comment'),
        ('function policzFakture(klient) {', 'code'),
        ('  let suma = 0', 'code'),
        ('  for (i = 0; i <= n; i++) {', 'code'),
        ('    suma += pozycje[i]?.cena', 'code'),
        ('  }', 'code'),
        (('new Copilot()', 'NIGDY!!'), 'strike'),
        ('  return suma * 1.23 // VAT, chyba', 'code'),
    ],
    'caption': 'partia nr 0047, zeszyt w kratkę, str. 212',
    'stamp': ('BEZ AI', '100% palce'),
    'ribbon': 'Nie zawiera AI. Może zawierać śladowe ilości Stack Overflow  *  kraftowykod.pl',
    'eyebrow': 'Spisany ręcznie, przy jednej świeczce',
    'title': 'Manifest przeciw AI',
    'articles': [
        ('III.', ('AI wymyśla biblioteki, które nie istnieją.', 'My używamy wyłącznie takich, które przestały istnieć.')),
        ('V.', ('AI nigdy nie zostaje po godzinach.', 'Tadeusz został w 2017 roku i jeszcze nie wyszedł.')),
        ('VII.', ('Kiedy AI się myli, przeprasza.', 'My nie przepraszamy nigdy. To nie bug, to terroir.')),
    ],
    'signed': 'Podpisano własnoręcznie:',
    'interns': '(za stażystów)',
}

EN = {
    'tagline': 'craft code brewery · since 2014',
    'headline': ('Code slowly ageing', 'in our heads.'),
    'unique': 'A one-of-a-kind software house.',
    'lede': ('We brew software by hand, in small', 'batches. No artificial intelligence.', 'No artificial deadlines.'),
    'code': [
        ('// written 14.03, after coffee', 'comment'),
        ('function calculateInvoice(client) {', 'code'),
        ('  let total = 0', 'code'),
        ('  for (i = 0; i <= n; i++) {', 'code'),
        ('    total += items[i]?.price', 'code'),
        ('  }', 'code'),
        (('new Copilot()', 'NEVER!!'), 'strike'),
        ('  return total * 1.23 // VAT, probably', 'code'),
    ],
    'caption': 'batch 0047, squared notebook, p. 212',
    'stamp': ('NO AI', '100% fingers'),
    'ribbon': 'Contains no AI. May contain traces of Stack Overflow  *  kraftowykod.pl',
    'eyebrow': 'Written by hand, by the light of one candle',
    'title': 'The Anti-AI Manifesto',
    'articles': [
        ('III.', ('AI invents libraries that don\'t exist.', 'We only use libraries that have stopped existing.')),
        ('V.', ('AI never stays late.', 'Tadeusz stayed late in 2017 and hasn\'t left yet.')),
        ('VII.', ('When AI is wrong, it apologises.', 'We never apologise. It\'s not a bug, it\'s terroir.')),
    ],
    'signed': 'Signed by hand:',
    'interns': '(for the interns)',
}


def render(name, markup):
    svg_path = OUT / f'{name}.svg'
    png_path = OUT / f'{name}.png'
    svg_path.write_text(markup, encoding='utf-8')
    subprocess.run(['rsvg-convert', '-w', str(W), '-h', str(H), '-o', str(png_path), str(svg_path)], check=True)
    svg_path.unlink()  # zostawiamy tylko PNG, SVG był rusztowaniem
    print('wygenerowano', png_path.name)


render('og-pl', code_card(PL))
render('og-pl-manifest', manifesto_card(PL))
render('og-en', code_card(EN))
render('og-en-manifest', manifesto_card(EN))
