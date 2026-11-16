# The check-up

## What to collect first

- The pages you can see and how: crawled (status codes known), pasted text, pasted HTML, screenshots,
  a site folder. Different sources prove different things.
- The profile's facts: phone, WhatsApp, address, hours, prices, services, review count and rating.
- Last month's findings from memory.

## The five lenses

### 1. Broken (costs customers today)

| Check | Evidence that proves it |
|---|---|
| Links and buttons that go nowhere (404, 500, wrong domain, `href="#"` on a real CTA) | Crawl status, or the href in the HTML |
| Contact paths: phone link (`tel:`), WhatsApp link, email, booking link, form destination | The HTML attribute; a form with no `action` and no handler is suspect, not proven broken |
| Missing images, broken embeds (maps, videos) | Crawl status or screenshot |
| Placeholder or test content ("lorem ipsum", "your text here", "test") | Text |
| Mixed content (http resources on an https page), certificate warnings | HTML / crawl |

### 2. Outdated (makes the business look closed or careless)

- Years in the past next to "now" words ("2024 schedule", "© 2023"), expired promotions ("Black Friday
  2025"), events that already happened.
- Facts that differ between pages or from the profile: phone, hours, address, prices, services. Show
  each version with its page; the owner says which is right.
- Staff, products or services the owner says no longer exist.

### 3. Weak copy

See `copy.md`. The 5-second test: from the top of the page, can a stranger say what this business
does, for whom, where, and what to do next?

### 4. Conversion

See `conversion.md`: tap-to-call/WhatsApp on mobile, form length, trust near CTAs, one primary action
per page, navigation.

### 5. Basics

See `technical.md`: title and description, one H1, heading order, alt text, labels, contrast, mobile,
language attribute, privacy notice and cookie consent where needed.

## Ranking

1. Wrong or broken contact path (wrong phone, dead booking link, form going nowhere).
2. Wrong facts that cause a bad visit (hours, address, prices).
3. Expired offers and old dates.
4. Copy that hides what the business does.
5. Conversion friction.
6. Basics and polish.

Group repeats ("alt text missing on 14 images across 5 pages" is one finding).

## Writing a finding

```
3. Contact page: phone number differs from the rest of the site
   Where: contato.html, footer and "Call us" button
   Evidence: footer shows (41) 3333-0000, button links to tel:+554133330001 (seen in the HTML);
             home and services show (41) 3333-0000; profile says (41) 3333-0000
   Impact: callers from the contact page reach a wrong or old number
   Fix: change the button link to tel:+554133330000   ·   Effort: 2 minutes
```

## What was not checked

Always end with it: pages not seen, links not tested (no browsing), speed not measured, mobile not
rendered, forms not submitted (never submit a real form without the owner's yes: it sends a real
message to someone).
