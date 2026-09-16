# Owens & Minor — Teammate Training & Development

## Purpose

This is a Streamlit prototype/MVP that gives Operations and EHS leadership a
simple way to select a **Business Line → Supervisor → Teammate** and
immediately view that Teammate's consolidated training matrix, covering:

- Job Function Training
- MHE (Material Handling Equipment) Certification
- ETQ / SOP Training

All Teammate and training data in this prototype is **dummy data**,
generated deterministically from a centralized data model so it can later
be swapped for a real enterprise data source without redesigning the app.

## Application Architecture

```
app.py         Application entry point, session-state routing, login gate
data.py        Centralized prototype data model (Business Line -> Supervisor
               -> Teammate -> training records) and load_training_data()
ui.py          Screen rendering functions (login, selection screens,
               training profile dashboard, reusable table/metric helpers)
styles.py      Owens & Minor color palette and CSS/header components
requirements.txt   Python dependencies
```

`app.py` never contains dummy data or table-rendering logic directly — it
only orchestrates which screen to show based on `st.session_state`. This
keeps the UI (`ui.py`), design system (`styles.py`), and data
(`data.py`) cleanly separated.

### User Flow

1. **Login** — password-gated entry screen.
2. **Business Line / Supervisor** — two dependent dropdowns; Supervisor
   options are filtered by the selected Business Line.
3. **Teammate Selection** — dropdown populated from the selected
   Supervisor's roster (~15 Teammates each).
4. **Training Profile** — dashboard with summary metrics, three training
   tables, and a dynamically generated Training Gaps section.

Session state (`st.session_state`) persists the current Business Line,
Supervisor, and Teammate selections as the user moves between screens, and
a sidebar allows changing any selection or logging out at any time.

## Installation

```bash
pip install -r requirements.txt
```

## Running the Application

```bash
streamlit run app.py
```

## Prototype Login Password

```
Platinum2025
```

The password is read from the `OM_APP_PASSWORD` environment variable if
set, otherwise it falls back to the hard-coded prototype value above. This
makes it straightforward to later move the password into `st.secrets` or an
enterprise SSO/identity provider without changing the login flow.

## Dummy Data

`data.py` defines:

- **`BUSINESS_LINE_SUPERVISORS`** — the 3 Business Lines and their 7
  Supervisors (SurgiTrack → Tim Norris; Medical Distribution → Tyler
  Bourgeois, Gerald Radcliff; Global Products → Eleanor Bragg, Michael
  McDowell, Samuel Meyer, Kevin Guthrie).
- **`SUPERVISOR_TEAMMATES`** — ~15 realistic dummy Teammate names per
  Supervisor (~105 Teammates total), each belonging to exactly one
  Supervisor / Business Line.
- **`JOB_FUNCTIONS`**, **`MHE_TYPES`**, **`ETQ_TRAINING_GROUPS`** — the
  training catalogs used across all Teammates.
- **`load_training_data()`** — generates a training record for every
  Teammate. Each Teammate is assigned a random-but-deterministic overall
  "proficiency rate" (seeded on their name) that drives individualized
  Yes/No and Complete/Incomplete results, so some Teammates are fully
  trained, some partially trained, and some have real gaps. Because the
  random seed is derived from the Teammate's name, the same Teammate
  always shows the same data across reruns.

## Replacing the Dummy Data Source

`data.load_training_data()` is the single integration point for a future
enterprise data source. To connect a real backend:

1. Replace the body of `load_training_data()` with a call to your data
   source (Snowflake query, SQL Server query, SharePoint list read, Excel/
   CSV import, REST API call, etc.).
2. Return the same shape: a dict keyed by `teammate_name`, where each value
   is a record with `teammate_name`, `business_line`, `supervisor`,
   `job_function_training`, `mhe_certifications`, and `etq_training`.
3. Optionally replace `BUSINESS_LINE_SUPERVISORS` and
   `SUPERVISOR_TEAMMATES` with data pulled from the same source so the
   Business Line/Supervisor/Teammate hierarchy stays in sync.

No changes to `ui.py`, `styles.py`, or `app.py` are required as long as the
returned record shape is preserved.
