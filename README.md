# Kraftowy Kod

A satirical website for a made-up software house that refuses to use AI and writes all its code by hand. The site talks about code the way craft breweries talk about beer: "kod długo dojrzewający w naszych głowach" (code slowly ageing in our heads).

The company doesn't exist. Neither do its three employees, Tadeusz, Zacheusz and Mateusz. The well-known companies in the client strip aren't clients, and the page says so.

## Files

| File | What it is |
|---|---|
| `index.html` | Polish site (main version) |
| `en/index.html` | English translation |
| `README.md` | This file, written by hand, obviously |

Each language is a single HTML file containing three or four pages. A short script at the bottom switches between them using the part of the address after `#`.

| Page | Polish | English |
|---|---|---|
| Home | `#start` | `#start` |
| Tech stack | `#technologie` | `#stack` |
| About us | `#o-nas` | `#about` |
| Contact | `#kontakt` | `#contact` |

## Viewing it

There's no build step. Open `index.html` in a browser, or serve the folder so the links between languages work:

```bash
python3 -m http.server 8000
```

Then go to http://localhost:8000.

There's also a private published copy at https://claude.ai/artifact/3jVeMTRGktKtqMYC4tm9Ea. Only people it's shared with can open it.

## How it's built

- **Tailwind CSS** from its CDN (`cdn.tailwindcss.com/3.4.17`), with the site's colours and fonts set in a small `tailwind.config` block at the top of each file.
- **Classes are written out in full in the HTML.** No `@apply`, no class-merging helpers, no shortened or obfuscated class names. That's part of the joke and part of the brief.
- **Fonts** come from Google Fonts: Rye for headings, Bitter for body text, Caveat for the handwriting.
- **Plain JavaScript** for the page switcher and the contact form.
- **The contact form really sends orders.** They're delivered by email through a form-handling service. The page only holds that service's public access key, which can do nothing except send messages to the brewery's inbox, so the email address itself never appears in the source. A hidden checkbox catches spam bots. The form needs a live internet connection and doesn't work inside the private claude.ai copy, which blocks requests to other sites.
- **Animations**: the scrolling ribbon and client strip, the "BEZ AI" stamp, and the code sample writing itself line by line. All of them switch off when the visitor's system is set to reduce motion.
- **The page is a light-only design** on purpose. It doesn't switch to dark mode.

## Search engines

Both pages ask search engines and AI crawlers not to index, cache, preview or train on them (`noindex, nofollow, noarchive, nosnippet, noimageindex, noai, noimageai`). These tags are requests, so badly behaved bots can ignore them. If you host the site yourself, also add a `robots.txt` with `Disallow: /` and send an `X-Robots-Tag: noindex, noarchive` header from the server.

## Hosting it yourself

The site is deployed on Vercel as a static site, with no build settings needed. Keep the main page named `index.html`: Vercel serves it at the site root, and the "Po polsku" link on the English page points to `../`, which relies on it.

## Editing

Each file is plain HTML. Edit it in any text editor. In keeping with company policy, Notepad is preferred.

Changes to text usually need making twice, once in each language.
