"""Prototype data layer for Owens & Minor Teammate Training & Development."""

from __future__ import annotations

import hashlib
from typing import Dict, List, Optional

BUSINESS_LINE_SUPERVISORS: Dict[str, List[str]] = {
    "SurgiTrack": ["Tim Norris"],
    "Medical Distribution": ["Tyler Bourgeois", "Gerald Radcliff"],
    "Global Products": [
        "Eleanor Bragg",
        "Michael McDowell",
        "Samuel Meyer",
        "Kevin Guthrie",
    ],
}

JOB_FUNCTIONS = [
    "Receiving",
    "Putaway",
    "Picking",
    "Packing",
    "Shipping",
    "Replenishment",
    "Inventory Control",
    "Cycle Counting",
    "Loading/Unloading",
    "Quality Inspection",
]

MHE_TYPES = [
    "Electric Pallet Jack",
    "Walkie Rider",
    "Reach Truck",
    "Order Picker",
    "Sit-Down Forklift",
    "Stand-Up Forklift",
    "Turret Truck",
    "Clamp Truck",
]

ETQ_GROUPS = [
    "Safety SOPs",
    "Receiving SOPs",
    "Picking SOPs",
    "Shipping SOPs",
    "Quality SOPs",
    "Inventory SOPs",
    "MHE Safety SOPs",
    "Hazmat SOPs",
    "Emergency Response SOPs",
    "PPE Requirements",
]

SUPERVISOR_TEAMMATES: Dict[str, List[str]] = {
    "Tim Norris": [
        "Avery Bennett",
        "Jordan Collins",
        "Cameron Foster",
        "Morgan Hayes",
        "Riley Lawson",
        "Taylor Mercer",
        "Casey Nolan",
        "Parker Rhodes",
        "Devin Sullivan",
        "Reese Thornton",
        "Quinn Wallace",
        "Hayden Brooks",
        "Logan Carter",
        "Drew Mitchell",
        "Blake Preston",
    ],
    "Tyler Bourgeois": [
        "Sydney Vaughn",
        "Colby Ramirez",
        "Jamie Franklin",
        "Peyton Duncan",
        "Robin Kramer",
        "Alexis Harper",
        "Emerson Boyd",
        "Kendall Price",
        "Marley Sutton",
        "Finley Bishop",
        "Skyler Briggs",
        "Ari Chandler",
        "Kieran Delaney",
        "Sage Matthews",
        "Rowan McBride",
    ],
    "Gerald Radcliff": [
        "Dakota Grimes",
        "Shawn Ellison",
        "Bailey Eaton",
        "Reagan Atkins",
        "Piper Donovan",
        "Tatum Vance",
        "Harper Neal",
        "Keegan Lane",
        "Presley Wolfe",
        "Payton Harmon",
        "Ellis Ritchie",
        "Jules Conrad",
        "Milan Faulkner",
        "Noel Carver",
        "Ashton Cline",
    ],
    "Eleanor Bragg": [
        "Lennon Walsh",
        "Campbell Russo",
        "Teagan Morrow",
        "Bellamy Dyer",
        "Arden Estes",
        "Greer Whitman",
        "Monroe Flynn",
        "Sterling Crane",
        "Hollis Bartlett",
        "Wren Castillo",
        "Blaire Rowe",
        "Remy Farley",
        "Galen Hines",
        "Shiloh Massey",
        "Brett Odom",
    ],
    "Michael McDowell": [
        "Carson Yates",
        "Devon Shepard",
        "Parker Irwin",
        "Kelsey Baird",
        "Spencer Mays",
        "Rory Beck",
        "Quincy Welch",
        "Linden Park",
        "Brooks Garner",
        "Merritt Kline",
        "Alden Kirby",
        "Nicolette Shaw",
        "Tobin Healy",
        "Brinley Hurst",
        "Callum Oakes",
    ],
    "Samuel Meyer": [
        "Taryn Pollard",
        "Mackenzie Sloan",
        "Nolan Everett",
        "Rory Gaines",
        "Sawyer Kent",
        "Paige Ingram",
        "Kendrix Monroe",
        "Leighton Quinn",
        "Micah Dalton",
        "Jocelyn Raines",
        "Eden Salazar",
        "Brady Finch",
        "Lane Holloway",
        "Marin Abbott",
        "Reid Sandoval",
    ],
    "Kevin Guthrie": [
        "Cade Whitaker",
        "Brynlee Hodge",
        "Emery Sykes",
        "Jensen Poole",
        "Marlowe Ray",
        "Ainsley Frazier",
        "Tyson Moffett",
        "Rylan Pace",
        "Everett Knapp",
        "Noa Calder",
        "Zane Mccall",
        "Tori Mullen",
        "Landry Moss",
        "Sutton Boyle",
        "Gentry Flores",
    ],
}


def _status_seed(*parts: str) -> int:
    raw = "|".join(parts).encode("utf-8")
    return int(hashlib.md5(raw).hexdigest(), 16)


def _binary_statuses(
    teammate_name: str,
    supervisor: str,
    items: List[str],
    positive_label: str,
    negative_label: str,
    base_completion: int,
) -> Dict[str, str]:
    statuses: Dict[str, str] = {}
    for idx, item in enumerate(items):
        seed = _status_seed(teammate_name, supervisor, item, str(idx))
        statuses[item] = positive_label if seed % 100 < base_completion else negative_label
    return statuses


def _get_business_line_for_supervisor(supervisor: str) -> Optional[str]:
    for business_line, supervisors in BUSINESS_LINE_SUPERVISORS.items():
        if supervisor in supervisors:
            return business_line
    return None


def load_training_data() -> List[Dict[str, object]]:
    """Return teammate-level prototype records.

    This abstraction allows future replacement with DB/API/warehouse sources.
    """

    records: List[Dict[str, object]] = []
    for supervisor, teammates in SUPERVISOR_TEAMMATES.items():
        business_line = _get_business_line_for_supervisor(supervisor)
        if not business_line:
            continue

        for teammate_idx, teammate_name in enumerate(teammates):
            base_completion = [92, 82, 72, 60, 48][teammate_idx % 5]

            job_function_training = _binary_statuses(
                teammate_name,
                supervisor,
                JOB_FUNCTIONS,
                "Yes",
                "No",
                base_completion,
            )
            mhe_certifications = _binary_statuses(
                teammate_name,
                supervisor,
                MHE_TYPES,
                "Yes",
                "No",
                max(35, base_completion - 12),
            )
            etq_training = _binary_statuses(
                teammate_name,
                supervisor,
                ETQ_GROUPS,
                "Complete",
                "Incomplete",
                min(97, base_completion + 5),
            )

            records.append(
                {
                    "teammate_name": teammate_name,
                    "business_line": business_line,
                    "supervisor": supervisor,
                    "job_function_training": job_function_training,
                    "mhe_certifications": mhe_certifications,
                    "etq_training": etq_training,
                }
            )

    return records


def get_business_lines() -> List[str]:
    return list(BUSINESS_LINE_SUPERVISORS.keys())


def get_supervisors_for_business_line(business_line: str) -> List[str]:
    return BUSINESS_LINE_SUPERVISORS.get(business_line, [])


def get_teammates_for_supervisor(
    records: List[Dict[str, object]],
    supervisor: str,
    business_line: Optional[str] = None,
) -> List[str]:
    return sorted(
        [
            str(record["teammate_name"])
            for record in records
            if record.get("supervisor") == supervisor
            and (business_line is None or record.get("business_line") == business_line)
        ]
    )


def get_teammate_record(
    records: List[Dict[str, object]],
    business_line: str,
    supervisor: str,
    teammate_name: str,
) -> Optional[Dict[str, object]]:
    for record in records:
        if (
            record.get("business_line") == business_line
            and record.get("supervisor") == supervisor
            and record.get("teammate_name") == teammate_name
        ):
            return record
    return None
