# The weekly watch

## Snapshot format

```
competitor;item;kind;value;source;date
Bella Forneria;Pizza margherita (large);price;79.90;site/menu;2026-06-02
Bella Forneria;Free delivery over 120;offer;active;instagram post;2026-06-02
Bella Forneria;Google rating;rating;4.6 (812);Google;2026-06-02
Bella Forneria;Ad "2 pizzas 99,90";ad;running since 2026-05-20;Meta Ad Library;2026-06-02
```

`kind`: price, offer, product, ad, rating, content, news, hiring.

## Compare (by hand or `scripts/watch.py old.csv new.csv`)

| Change | How to report |
|---|---|
| Price change | old → new, % and the dates of both observations |
| New / removed item | what, since when (date first/last seen) |
| New offer | terms and deadline exactly as published |
| Offer ended | last date seen active |
| Ads | new ads and angles; ads running for 4+ weeks (likely profitable) |
| Rating | rating and count change; new complaint themes |

No earlier observation → "first seen", not "new" or "changed". A source that could not be read this
week → "not checked", not "no change".

## Reading the signal (label as inference)

- Lower price on one item only: test, clearance or traffic driver.
- Many new ads with one angle: they found something that converts; watch how long it runs.
- Rising complaints about delivery or waiting: an opening on speed and reliability.
- Hiring for delivery/sales: expansion coming.
