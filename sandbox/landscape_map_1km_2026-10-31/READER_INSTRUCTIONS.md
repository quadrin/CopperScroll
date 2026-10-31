# Reader instructions (benchmark C, run 27)

You will look at map images. Each is a piece of a British Survey of Palestine 1:20,000 sheet from the 1940s, at about 2 m per pixel.

## Task

List every place on the image where the map marks one of these things:

| class | What to look for (English labels, abbreviations and Arabic name elements printed on these maps) |
|---|---|
| `cave` | "Cave", "Caves", "Mgh.", "Mughr", "Mughara", "Magharet", or a cave symbol |
| `tomb` | "Tomb", "Tombs", "Qabr", "Qubur", "Rock-cut tombs" |
| `cistern` | "Cistern", "Cisterns", "Cist.", "Bir", "Biyar", "Bayar", or a cistern symbol |
| `well` | "Well", "W.", or a well symbol. If you cannot tell well from cistern, use `well` |
| `pool` | "Pool", "Birket", "Birkat", "Res.", "Reservoir" |
| `aqueduct` | "Aqueduct", "Aq.", "Qanat", "Channel", or a line labelled as one of these |

Do not list anything else: ruins, springs, villages, roads, shrines, trees or contour labels. A spring ("ʿAin", "Spring") is **not** a pool or cistern.

## How to record

For each item, give:
- `class`: one of the six above;
- `text`: the printed words, exactly as you read them, or "" for a symbol without words;
- `x`, `y`: the pixel position of the feature itself (the symbol, or the point the label belongs to), from the top-left corner of the image;
- `confidence`: "high", "medium" or "low".

If a label names a place that has several of these things (for example "Caves"), give one item at the label's feature.

Return JSON only, in this form:

```
{"window": "<window id>", "items": [{"class": "cave", "text": "Mgh. el ...", "x": 312, "y": 140, "confidence": "high"}]}
```

If the image shows none of these, return an empty `items` list. Do not guess beyond what is printed. You have no other information about these places, and you should not look for any.
