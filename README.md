## github-readme-seasons-animation

Generate animated SVGs that represent the seasons for your GitHub profile README.
The color scheme changes based on the season (spring/summer/autumn/winter), with gentle swaying leaf animations.

### Local Generation

```bash
python main.py --output assets/seasons.svg
```

Output: `assets/seasons.svg`

### Embedding in README

For reliable display on GitHub, use the raw URL:

```md
![seasons](https://raw.githubusercontent.com/<YOUR_GITHUB>/<YOUR_REPO>/main/assets/seasons.svg)
```

(Replace the repository name and branch name as needed)

### Season/Date Behavior

- By default, uses today's date (UTC) for generation
- Can be fixed with `--date 2026-01-06`
- Can force a specific season with `--season winter`
- All options can also be set via environment variables: `SEASONS_DATE` / `SEASONS_SEASON` / `SEASONS_SEED`

### Automatic Updates with GitHub Actions

This repository includes a workflow that periodically regenerates and commits `assets/seasons.svg`.
If you fork this repository, make sure to enable Actions.

