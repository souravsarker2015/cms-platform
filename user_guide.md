# Editor's guide

A guide to running the Endeavours website from the Wagtail admin. No technical
knowledge needed — if you can use a word processor, you can use this.

**Contents**

1. [Signing in](#1-signing-in)
2. [Finding your way around](#2-finding-your-way-around)
3. [Editing a page](#3-editing-a-page)
4. [Building a page with blocks](#4-building-a-page-with-blocks)
5. [The block library](#5-the-block-library)
6. [Adding a new page](#6-adding-a-new-page)
7. [Navigation menus](#7-navigation-menus)
8. [The footer](#8-the-footer)
9. [Company details and social links](#9-company-details-and-social-links)
10. [Images](#10-images)
11. [Search engines and social sharing](#11-search-engines-and-social-sharing)
12. [Publishing, drafts and undo](#12-publishing-drafts-and-undo)
13. [Good habits](#13-good-habits)
14. [Troubleshooting](#14-troubleshooting)

---

## 1. Signing in

Go to **<http://localhost:8000/admin/>** and sign in.

On a new local setup the starting account is:

| Username | Password |
|----------|----------|
| `admin`  | `admin123456` |

> ⚠️ **Change this password.** It is a development default and is written down
> in the project files. Click your name in the bottom-left corner →
> **Account settings** → **Change password**. Do this before anyone else can
> reach the site.

---

## 2. Finding your way around

The menu runs down the left-hand side.

| Menu item | What it holds |
|-----------|---------------|
| **Pages** | Every page on the website |
| **Images** | All uploaded pictures |
| **Documents** | PDFs and other files |
| **Snippets** | Navigation menus and the footer |
| **Settings** | Company name, logo, contact details, social links |
| **Reports** | Recent edits, broken links, workflow history |

Click **Pages** to see the site as a tree. Everything sits under **Home**.

---

## 3. Editing a page

1. Click **Pages** in the sidebar.
2. Click the page you want (or hover and press **Edit**).
3. Make your changes.
4. Click **Publish** at the bottom.

Your changes go live immediately.

Each page has tabs at the top:

- **Content** — the text and sections visitors see. This is where you'll spend
  your time.
- **Promote** — the page address, plus how the page looks in Google and on
  social media. See [section 11](#11-search-engines-and-social-sharing).
- **Settings** — publishing dates and privacy.

> **Tip:** Use **Preview** (next to Publish) to see your changes before making
> them live. The preview updates as you type.

---

## 4. Building a page with blocks

Page content is built from **blocks** — self-contained sections you stack in
any order. Think of them like LEGO bricks.

**To add a block:** click the **+** button in the body area and pick a block
from the list.

**To reorder:** grab the handle (⠿) on the left of a block and drag it, or use
the up/down arrows.

**To delete:** click the bin icon on the block.

**To collapse:** click the block's title bar. Useful on long pages.

Blocks can be rearranged freely, so it's safe to experiment — nothing is
permanent until you click **Publish**.

---

## 5. The block library

### Hero
A large banner for the top of a page.

- **Eyebrow** — small line above the headline (e.g. "Our services")
- **Heading** — the main headline
- **Subheading** — a sentence or two of supporting text
- **Background image** — optional; text stays readable automatically
- **Alignment** — left or centred
- **Buttons** — up to two

### Rich text
Ordinary prose: headings, **bold**, *italic*, links, bullet and numbered
lists, and quotes. Use this for paragraphs of writing.

### Image
A picture with an optional caption and credit. Choose a width:
**Standard** (text width), **Wide**, or **Full bleed** (edge to edge).

### Feature grid
A row of cards, each with an icon, title and short description. Good for
listing services or benefits.

- Pick **2**, **3** or **4** columns — 3 is usually best
- Choose an icon for each card from the fixed set (keeps the site consistent)
- Cards can link somewhere; the whole card becomes clickable

### Call to action
A bold panel prompting visitors to do something — get in touch, book a call.
A heading, optional text, and one or two buttons. Choose an **Accent**
(dark, high-impact) or **Muted** (subtle) background.

### Testimonial
A customer quote with their name, role, photo and company logo. Only the quote
and name are required.

### Stats
Up to four headline figures, e.g. "120+ projects delivered". Each has a
**Value** (the number) and a **Label** (what it means). Keep values short.

### FAQ
Questions and answers in an accordion — visitors click a question to expand
the answer. Add as many as you need.

### Button
A link styled as a button, used inside other blocks.

- **Text** — leave blank to use the linked page's name
- **Page** — pick a page on this site
- **External URL** — for links to other websites
- **Style** — Primary (solid), Secondary (outlined), Ghost (plain)

> **Important:** To link somewhere on *this* website, always use the **Page**
> picker rather than typing the address. If that page is later renamed or
> moved, the link follows it automatically. A typed address would break.

---

## 6. Adding a new page

1. Go to **Pages** and hover over the page it should sit *under*
   (usually **Home**).
2. Click **+ Add child page**.
3. Choose **Standard page**.
4. Give it a **Title** — this becomes the page's heading and web address.
5. Add an **Intro** (a short summary under the title) and build the body from
   blocks.
6. Click **Publish**.

New pages appear in the navigation automatically. To keep one out of the menu,
go to the **Promote** tab and untick **Show in menus**.

> There can only ever be one **Home** page — that's deliberate.

---

## 7. Navigation menus

The menu across the top of the site is edited under
**Snippets → Navigation menus → Main menu**.

Each **menu item** is one link in the top bar:

- **Title** — leave blank to use the page's own name
- **Page** — the page to link to
- **External URL** — for another website instead
- **Highlight** — tick to show this item as a button. Use for one item only,
  usually "Contact".

**To add a dropdown**, add **Sub-items** underneath a menu item. Each sub-item
can have a short description shown under its name.

**To reorder**, drag items by the handle on the left.

> The menu with the slug `main` is the one that appears in the header. Don't
> change that slug.

---

## 8. The footer

Edit under **Snippets → Footer → Main footer**.

- **Intro** — a short paragraph about the company
- **Columns** — groups of links. Each column has a heading and a list of
  links. Two or three columns works well.
- **Copyright text** — appears after the year, which updates on its own
- **Legal links** — small links along the bottom (Privacy, Terms)

If you have more than one footer, the site uses the most recently created one
marked **Active**. Untick **Active** on the others.

---

## 9. Company details and social links

**Settings → Site settings** holds details reused across the whole site.
Change them once here and they update everywhere.

- **Brand** — company name, tagline, logo, favicon. The **dark logo** is used
  on the dark footer; if you don't set one, the main logo is used.
- **Contact** — email, phone and address. These appear in the footer. Put each
  line of the address on its own line.
- **Social links** — paste the full address (e.g.
  `https://linkedin.com/company/yourcompany`). Only the ones you fill in are
  shown, each with the right icon.
- **Defaults** — a fallback image for social sharing.

---

## 10. Images

Upload under **Images**, or directly from any block that takes a picture.

**Sizes.** Upload large and let the site resize: at least **2000px wide** for
banners, **1200×630** for social sharing images. The site generates every
smaller size it needs.

**Alt text.** Wagtail asks for a description of each image. This is read aloud
to visually impaired visitors and shown if the image fails to load. Describe
what's in the picture — "Team members reviewing plans in the office", not
"image1". If a picture is purely decorative, leave it blank.

**Focal point.** Click **Edit** on an image and drag a box over the most
important part — a face, say. When the image is cropped, that part is kept.

---

## 11. Search engines and social sharing

On any page, open the **Promote** tab.

**Page metadata**

- **Slug** — the last part of the web address (`/about-us/`). Keep it short
  and in lowercase with hyphens. Changing it on a live page breaks existing
  links, so avoid it once published.
- **Title tag** — the heading shown in Google results. Leave blank to use the
  page title. Aim for under 60 characters.
- **Meta description** — the grey summary under the Google result. Aim for
  around 150 characters. Write it for a person, not a search engine.

**Social sharing** — the title, description and image shown when the page is
posted on LinkedIn, Facebook or X. Leave blank and the page falls back to the
metadata above. A good share image is **1200×630**.

**Search engine visibility** — ticking **Hide from search engines** asks
Google not to list the page. Use it for thank-you pages. It doesn't make a
page private.

---

## 12. Publishing, drafts and undo

- **Save draft** — stores your work without changing the live site.
- **Publish** — makes it live immediately.
- **Preview** — shows how it will look, without publishing.

**Scheduling.** Under the **Settings** tab, set a **Go live date** and publish;
the page appears automatically at that time.

**Undo.** Every save is kept. Open the page and click **History** to see every
change and who made it. To go back, open an earlier version and click
**Revert to this version**. Nothing is ever truly lost.

**Deleting.** Deleted pages go to the bin and can be restored. Deleting a page
also deletes everything underneath it, so check its children first.

---

## 13. Good habits

**Writing**

- One idea per section; break up long text with headings
- Write "you" and "we" — it reads more naturally than "the company"
- Put the most important point first
- Keep button text short and specific: "Book a call", not "Click here"

**Structure**

- Start with a Hero, end with a Call to action
- Alternate text-heavy and visual blocks so pages don't feel dense
- Three or four sections is usually plenty for one page

**Accessibility**

- Always write alt text for meaningful images
- Don't skip heading levels
- Make link text describe its destination — "read our approach", not
  "click here"

**Before publishing**

- Preview on your phone as well as your computer
- Click every link
- Read it once more out loud

---

## 14. Troubleshooting

**My change isn't showing on the site.**
Check you clicked **Publish** rather than **Save draft**. If the page shows a
**Draft** label, your changes aren't live yet. Otherwise refresh with
`Ctrl+Shift+R` (`Cmd+Shift+R` on a Mac).

**A page is missing from the menu.**
Menu items come from **Snippets → Navigation menus**, not automatically from
the page tree. Add the page there. Also check **Show in menus** on the page's
**Promote** tab.

**My image looks stretched or badly cropped.**
Set a focal point (see [section 10](#10-images)). If it's still wrong, the
original is probably too small — re-upload a larger version.

**I can't find the block I want.**
Some blocks are only available in certain places, and the Hero block is
limited to one per page. Scroll the full list in the **+** menu.

**I deleted something by accident.**
Pages go to the bin and can be restored. For content inside a page, open
**History** and revert to an earlier version.

**I'm locked out.**
Another administrator can reset your password under **Settings → Users**.

---

*Questions this guide doesn't answer? Ask the development team — and tell them
which part was unclear, so it can be fixed here.*
