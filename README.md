# euler-bench — Project Euler problem prompts

Self-contained local snapshot of **all Project Euler problems 1–1005** (as of 2026-07-10),
one markdown prompt per problem, with every image and data file stored locally.

## Layout

```
prompts/
  problem-<N>/
    problem-<N>.md      # the problem statement
    assets/             # present only when the problem references files
      <image>.png|gif|jpg
      <data>.txt
```

- **1005** problems, one folder each.
- **214** problems have an `assets/` folder → **255 images** + **23 `.txt` data files**.
- Everything is local and relative: markdown references assets as `assets/<name>`.
  There are **no** remote resource URLs. Links to *other* problems (`problem=<N>`) remain absolute.

## How it was built

- **Bodies** come from Project Euler's clean HTML endpoint `https://projecteuler.net/minimal=<N>`,
  converted to GitHub-flavored Markdown with `pandoc`. All mathematics is preserved as LaTeX (`$...$`);
  Project Euler renders formulas as text, so images are never equations — they are diagrams,
  figures, and animations.
- **Titles** come from the archives pages (`/archives;page=<p>`) and `/recent`.
- **Assets** (images + linked `.txt` data files) were downloaded and copied into each problem's
  `assets/` folder, with the markdown rewritten to relative paths.

## Notes

- 20 of the images are animated GIFs (only the first frame renders in most markdown viewers).
- **Problem 991** ("Fruit Salad"): Project Euler's own text has a typo in the third denominator;
  the authoritative rendered equation is at `prompts/problem-991/assets/0991_fruits.png`.
  The markdown reproduces the source text faithfully (uncorrected).

Data © Project Euler contributors — see https://projecteuler.net (problems are published under
CC BY-NC-SA). This repository is an offline mirror for local use.
