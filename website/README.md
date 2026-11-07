# Project website

Static site that presents the V2 comparison results. No build tools needed.

- `index.html`: the page
- `data.js` / `data.json`: numbers summarized from a comparison batch
- `figures/`: MATLAB figures from the same batch
- `build_data.py`: regenerates the data files (Python 3 standard library only)

## Update after a new MATLAB run

```bash
python3 website/build_data.py comparison_YYYYMMDD_HHMMSS_SSS
cp revisions/v2/results/comparison_YYYYMMDD_HHMMSS_SSS/figures/*.png website/figures/
```

## Preview locally

```bash
python3 -m http.server 8765 --directory website
```

## Deploy on Render

`render.yaml` at the repository root defines a static site that publishes `./website`.
Push the repository to GitHub, then in Render choose **New → Blueprint** and select the repository.
