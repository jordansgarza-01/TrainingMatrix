"""
Centralized prototype data model for the Owens & Minor
Teammate Training & Development application.

This module is the single source of truth for:
    - Business Line -> Supervisor relationships
    - Supervisor -> Teammate relationships
    - Job Function / MHE / ETQ training catalogs
    - Randomized (but deterministic) dummy training records

`load_training_data()` is the intended integration point for swapping this
in-memory dummy data for a real enterprise data source later (Snowflake,
SQL Server, SharePoint, Excel/CSV, REST API, etc.) without requiring
changes to ui.py or app.py.
"""

import random

# ---------------------------------------------------------------------------
# Business Line -> Supervisor relationships (order matters for the UI)
# ---------------------------------------------------------------------------
BUSINESS_LINE_SUPERVISORS = {
    "SurgiTrack": ["Tim Norris"],
    "Medical Distribution": ["Tyler Bourgeois", "Gerald Radcliff"],
    "Global Products": [
        "Eleanor Bragg",
        "Michael McDowell",
        "Samuel Meyer",
        "Kevin Guthrie",
    ],
}

BUSINESS_LINES = list(BUSINESS_LINE_SUPERVISORS.keys())

# Reverse lookup: Supervisor -> Business Line
SUPERVISOR_BUSINESS_LINE = {
    supervisor: business_line
    for business_line, supervisors in BUSINESS_LINE_SUPERVISORS.items()
    for supervisor in supervisors
}

# ---------------------------------------------------------------------------
# Supervisor -> Teammate roster (~15 dummy teammates each, ~105 total)
# ---------------------------------------------------------------------------
SUPERVISOR_TEAMMATES = {
    "Tim Norris": [
        "Avery Bennett", "Jordan Collins", "Cameron Foster", "Morgan Hayes",
        "Riley Lawson", "Taylor Mercer", "Casey Nolan", "Parker Rhodes",
        "Devin Sullivan", "Reese Thornton", "Quinn Wallace", "Hayden Brooks",
        "Logan Carter", "Drew Mitchell", "Blake Preston",
    ],
    "Tyler Bourgeois": [
        "Peyton Alvarez", "Marcus Bellamy", "Sydney Chandler", "Trevor Donovan",
        "Alexis Fenwick", "Grant Holloway", "Nadia Ibarra", "Corey Jansen",
        "Brielle Kensington", "Dominic Larkspur", "Vanessa Merrick", "Elliot Prescott",
        "Simone Quintero", "Nathaniel Rourke", "Isabela Whitfield",
    ],
    "Gerald Radcliff": [
        "Beatrice Ashworth", "Julian Castellano", "Fiona Delacroix", "Marcus Ellington",
        "Priya Fitzgerald", "Desmond Garrity", "Lila Hutchinson", "Omar Kavanagh",
        "Renata Lindqvist", "Silas Monaghan", "Adelaide Northrup", "Theo Pemberton",
        "Wren Sinclair", "Maribel Torrance", "Gideon Wexler",
    ],
    "Eleanor Bragg": [
        "Amara Chisholm", "Bennett Crawley", "Delphine Osei", "Emmett Fairweather",
        "Giselle Harrow", "Holden Iverson", "Ingrid Kowalczyk", "Jasper Lindgren",
        "Kendra Marchetti", "Leandro Novak", "Miriam Ocampo", "Nash Patterson",
        "Odalys Rhinehart", "Percival Stanhope", "Rosalind Tremaine",
    ],
    "Michael McDowell": [
        "Anders Blackwood", "Camille Duquette", "Dashiell Everhart", "Esme Falconer",
        "Frederick Gantry", "Harriet Ibsen", "Ignatius Jorgensen", "Josephine Kestrel",
        "Killian Lachance", "Lucinda Maddox", "Montgomery Nash", "Ophelia Prewitt",
        "Quentin Radcliffe", "Seraphina Thorne", "Tobias Winslow",
    ],
    "Samuel Meyer": [
        "Abigail Sorensen", "Baxter Colfax", "Clementine Drayton", "Desmond Farraday",
        "Estelle Granger", "Foster Hollingsworth", "Genevieve Ibbotson", "Hamish Jennings",
        "Ivy Larchmont", "Jethro Mancini", "Katarina Nesbitt", "Lorcan Osgood",
        "Magnolia Pruett", "Nolan Quimby", "Octavia Ridgeway",
    ],
    "Kevin Guthrie": [
        "Alistair Banfield", "Cordelia Eastwood", "Dexter Fallowfield", "Evangeline Grosvenor",
        "Fitzgerald Holbrook", "Griselda Inkster", "Hollis Jarrett", "Imogen Kirkland",
        "Jasper Lonsdale", "Katrina Merriweather", "Lachlan Norwood", "Marisol Pemberly",
        "Nikolai Quintrell", "Petra Rathbone", "Roscoe Standish",
    ],
}

# ---------------------------------------------------------------------------
# Training catalogs
# ---------------------------------------------------------------------------
JOB_FUNCTIONS = [
    "Receiving", "Putaway", "Picking", "Packing", "Shipping",
    "Replenishment", "Inventory Control", "Cycle Counting",
    "Loading/Unloading", "Quality Inspection", "Returns Processing",
]

MHE_TYPES = [
    "Electric Pallet Jack", "Walkie Rider", "Reach Truck", "Order Picker",
    "Sit-Down Forklift", "Stand-Up Forklift", "Turret Truck", "Clamp Truck",
    "Tugger", "Scissor Lift",
]

ETQ_TRAINING_GROUPS = [
    "Safety SOPs", "Receiving SOPs", "Picking SOPs", "Shipping SOPs",
    "Quality SOPs", "Inventory SOPs", "MHE Safety SOPs", "Hazmat SOPs",
    "Emergency Response SOPs", "GMP/Quality Awareness", "PPE Requirements",
    "Warehouse Security",
]


def _build_status_map(rng, items, positive_value, negative_value, completion_rate):
    """Return {item: positive/negative value}, weighted by a completion rate."""
    return {
        item: positive_value if rng.random() < completion_rate else negative_value
        for item in items
    }


def _generate_teammate_record(teammate_name, supervisor):
    """Build one deterministic-but-varied dummy training record."""
    # Seed on the name so results are stable across reruns/sessions but
    # still differ from one teammate to the next.
    rng = random.Random(f"seed::{teammate_name}")

    # Each teammate gets their own overall proficiency level so some are
    # fully trained, some partially trained, and some have real gaps.
    completion_rate = rng.uniform(0.35, 0.95)

    return {
        "teammate_name": teammate_name,
        "business_line": SUPERVISOR_BUSINESS_LINE[supervisor],
        "supervisor": supervisor,
        "job_function_training": _build_status_map(
            rng, JOB_FUNCTIONS, "Yes", "No", completion_rate
        ),
        "mhe_certifications": _build_status_map(
            rng, MHE_TYPES, "Yes", "No", completion_rate
        ),
        "etq_training": _build_status_map(
            rng, ETQ_TRAINING_GROUPS, "Complete", "Incomplete", completion_rate
        ),
    }


def load_training_data():
    """
    Load all teammate training records.

    This is the intended integration point for swapping the dummy,
    in-memory data below for a real enterprise data source later
    (Snowflake, SQL Server, SharePoint, Excel/CSV, REST API, etc.). The
    rest of the application only depends on the dict-of-records shape
    returned here, so a future implementation can change the data source
    without touching ui.py or app.py.

    Returns:
        dict: {teammate_name: teammate_record}
    """
    records = {}
    for supervisor, teammates in SUPERVISOR_TEAMMATES.items():
        for teammate_name in teammates:
            records[teammate_name] = _generate_teammate_record(teammate_name, supervisor)
    return records


# Loaded once at import time; acts as the prototype's "database".
TEAMMATE_RECORDS = load_training_data()


def get_supervisors_for_business_line(business_line):
    """Return the list of valid supervisors for a given Business Line."""
    return BUSINESS_LINE_SUPERVISORS.get(business_line, [])


def get_teammates_for_supervisor(supervisor):
    """Return the list of teammate names reporting to a given Supervisor."""
    return SUPERVISOR_TEAMMATES.get(supervisor, [])


def get_teammate_record(teammate_name):
    """Return the full training record for a teammate, or None if missing."""
    return TEAMMATE_RECORDS.get(teammate_name)
