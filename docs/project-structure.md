# Project Structure

```bash
pokemon_showdown_analysis/
  docs/
    README.md
    dev-logs.md                 # Developer's personal logs
    project-structure.md
    schema.md                   # Database schema
    er_diagram.pdf
  src/
    data/
      showdown_data_processed/  # Pokémon Showdown! data parsed into JSON
      showdown_data_raw/        # Pokémon Showdown! data in TypeScript as in the repository
      smogon_data/              # Smogon Stats JSON files
      data.sql                  # Queries to build the database
    setup/
      download/                 # Script to download raw data (create data/showdown_data_raw/, data/smogon_data/)
      setup_json/               # Script to process Pokémon Showdown! data into JSON form (create data/showdown_data_processed/)
      setup_sql/                # Script to generate data.sql from JSON data
    app/
      app.py                    # Main TUI app entry point
      widgets/                  # Holds reusable widgets created by us
      screens/                  # Holds different TUI pages/screens 
    # More modules to be added
  .gitignore
  README.md
  Makefile                      # Runs the program
  requirements.txt
```
