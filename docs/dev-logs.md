# Developer Logs

## 10/28/2025 (Peter)

* Restructured the project:
  * Created the `src/` and `docs/` folders.
  * Move existing data to `src/data/`.
  * Scaffold `src/setup/` for future data fetching and processing.
* Documented table schema at [schema.md](./schema.md).

## 10/29 2025 (Peter)

* Updated documentation:
  * Uploaded the [ER Diagram](./er_diagram.pdf).
  * Updated the [README](./../README.md).
  * Other minor updates.

## 11/22 2025 (Connor)

* Processed Pokemon Showdown! Data
  * Wrote Typescript to process Typescript Classes to JSON

## 11/24 2025 (Connor)

* Architected page navigation and Menu page
  * Setup buttons and key bindings
  * Created stucture in src/app for widgets and screens and styles
* Setup scripts to run application
  * Created Makefile options to run the app
* Minor doc changes

## 11/27 2025 (Connor)

* Made script to download all gen 9 smogon chaos files
  * Downloads to src/data/smogon_data
  * Files are categorised using directories based on year and month
* Determined data to cut to fit under 300MB limit
