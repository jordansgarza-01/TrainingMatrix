# Owens & Minor — Teammate Training & Development

A Streamlit prototype that helps Operations/EHS leaders review teammate training readiness by Business Line, Supervisor, and Teammate.

## Purpose

This MVP provides a multi-screen workflow for:

1. Logging in
2. Selecting Business Line and Supervisor
3. Selecting a Teammate
4. Viewing a consolidated training matrix and training gaps

It uses dummy prototype data and is structured so the data source can later be replaced with enterprise systems.

## Project Structure

```text
owens_minor_training/
├── app.py
├── data.py
├── ui.py
├── styles.py
├── requirements.txt
└── README.md
```

## Architecture

- **`app.py`**: App entrypoint and screen routing
- **`data.py`**: Centralized data model + `load_training_data()` abstraction and helper access functions
- **`ui.py`**: Screen rendering, tables, metrics, validation, and training-gap logic
- **`styles.py`**: Owens & Minor-inspired visual theme styling

Data follows this hierarchy:

```text
Business Line
  └── Supervisor
        └── Teammate
              ├── Job Function Training
              ├── MHE Certification
              └── ETQ Training
```

## Installation

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Run the Application

```bash
streamlit run app.py
```

## Prototype Login

- Default password: `Platinum2025`
- Optional override: set `prototype_password` in `.streamlit/secrets.toml` or set environment variable `OM_TRAINING_APP_PASSWORD`

## Dummy Data Notes

- 3 business lines
- 7 supervisors
- ~15 teammates per supervisor (~105 teammate records total)
- Teammate-specific Job Function, MHE, and ETQ status values (not identical across all teammates)

## Replacing Dummy Data Later

The app uses `load_training_data()` as a data-layer abstraction. Replace that function to source records from systems such as:

- Snowflake
- SQL Server
- SharePoint
- Excel / CSV
- REST APIs
- Power BI-related data services

As long as the returned teammate record structure remains consistent, the UI module can remain unchanged.
