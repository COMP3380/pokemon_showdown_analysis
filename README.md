# COMP 3380 Pokemon Showdown Group Project

## Quickstart

Navigate to the main directory with all files and run:

```bash
make
```

Immediately the code will download all relevant raw Smogon data, as keeping all
of this in the repository would make it too large. The Pokemon Showdown raw
data, however, is already inlcuded in the repository, as we had to manually
process it. Additionally it is relatively small.

The database comes pre-populated and you can navigate around using bindings
listed at the bottom of each page, using arrow or Vim keys on tables (such as
j, k, h, l, g, G, ctrl+d, and ctrl+u), using 'Tab' and 'Shift+Tab' to navigate
between elements on pages, or using your mouse to click on things or drag
scrollbars.

Upon choose to "Repopulate", you will be met with a confirmation dialog box.
Choosing "Yes" will cause deletion and repopulation to begin. You will
purposefully not being able to interact with the program while this is
happening. This will take about 5-6 minutes and you will know it is done when
the dialog box disappears and functionality returns.

## For Developers

Before running `make`, if you wish to have debug information, first run the
following in one terminal emulator:

```bash
make setup
textual console
```

Then in different terminal emulator run:

```bash
make
```

### Documentation

- [Smogon Stats](https://www.smogon.com/stats/)
- [Understanding `Cutoff`](https://www.smogon.com/forums/threads/weighted-stats-faq.3478570/)
- [Understanding `ViabilityCeiling`](https://www.smogon.com/forums/threads/viability-ceiling-a-measure-of-how-far-a-pokemon-can-take-you.3546373/)

Examples on similar projects can be found here:

- [Porydex](https://www.porydex.com/)
- [Smogon stats as SQLite database](https://git.pyrope.net/mbk/smogon-stats) 
