# Data pipeline

Two stages: **scrapers** pull vendor catalogues into JSON, **loaders** push that JSON
into the database. Loaders are idempotent — they `update_or_create` on `import_url`,
so re-running updates rows instead of duplicating them.

Run everything from the Django project root (`bikebuilder/`), with the venv active.

## Restoring a populated database

    # 1. Dosnoventa + Engine11 (40 rows)
    python scripts/load_dos_engine11_frames.py
    python scripts/load_dosnoventa_components.py

    # 2. Retro-Gression (480 rows)
    for f in scripts/retrogression/load_*.py; do python "$f"; done
    python scripts/retrogression/load_cranks.py arms   # see note below

Expected total: **520 components**.

### Note on crank arms

`load_cranks.py` has two entry points. Bare invocation loads cranksets; crank arms
need the explicit `arms` argument. The `for` loop above only covers the first, so the
second line is required — without it you get 17 cranksets and 0 crank arms.

## Layout

    scripts/
      load_dos_engine11_frames.py     frames from both dosnoventa + engine11
      load_dosnoventa_components.py   bars/stems/seatposts/wheels
      clear_components.py             deletes every component row
      scrape_*.py                     vendor scrapers (write the JSON here)
      retrogression/
        load_*.py                     15 loaders, one per category
        extracted/*.json              loader inputs
        *.json                        raw scrape output
      velodrome/
        scrape_velodrome.py           scraper only — no loader exists yet, so
                                      velodrome/*.json is not in the database

Each script locates the project root by walking up for `manage.py`, so they work from
any working directory and survive being moved.

## Images

Loaders store the vendor's own image URL. Normalizing images onto a uniform canvas and
rehosting them on S3 is a separate, opt-in step:

    python manage.py normalize_images --dry-run
    python manage.py normalize_images --type saddle
    python manage.py normalize_images

**Before running it**, extend the S3 bucket policy to cover the `component-image/*`
prefix. It currently grants public read to `user-upload/*` only, so normalized images
upload fine but return 403 to browsers.
