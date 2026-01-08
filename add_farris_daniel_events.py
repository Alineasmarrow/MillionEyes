#!/usr/bin/env python3
"""
Add Farris and Daniel events to act_data.json

This script adds the missing Farris and Daniel events to their respective acts.
"""

import json

# Farris and Daniel events to add
NEW_EVENTS = {
    "1": [  # Act 1
        {
            "id": "farris_sees_shadow",
            "name": "Farris Sees the Shadow First",
            "category": "farris_presence",
            "act": 1,
            "unique": False,
            "burns": False,
            "cooldown": 3,
            "probability_decay": 0.85,
            "chaos": 0.5,
            "turbulence": 0.3,
            "pressure": 0.2,
            "description": "Farris stares at a corner no one else feels drawn to. 'It's already watching.'"
        },
        {
            "id": "farris_reaches_maeve",
            "name": "Farris Reaches for Maeve",
            "category": "farris_presence",
            "act": 1,
            "unique": False,
            "burns": False,
            "cooldown": 2,
            "probability_decay": 0.8,
            "chaos": -0.5,
            "turbulence": 0.0,
            "pressure": -0.3,
            "description": "Farris quietly sits beside Maeve. No words. Just presence."
        },
        {
            "id": "daniel_wrong_questions",
            "name": "Daniel Asks the Wrong Questions",
            "category": "daniel_institutional",
            "act": 1,
            "unique": False,
            "burns": False,
            "cooldown": 2,
            "probability_decay": 0.75,
            "chaos": 0.5,
            "turbulence": 0.5,
            "pressure": 0.5,
            "description": "Daniel tries to help with protocol and paperwork. Maeve feels more distant."
        },
        {
            "id": "daniel_notices_yuul",
            "name": "Daniel Notices Yuul",
            "category": "daniel_institutional",
            "act": 1,
            "unique": False,
            "burns": False,
            "cooldown": 3,
            "probability_decay": 0.8,
            "chaos": 0.3,
            "turbulence": 0.2,
            "pressure": 0.3,
            "description": "Daniel watches Yuul closely. Something in his expression shifts."
        }
    ],
    "2": [  # Act 2
        {
            "id": "farris_intercepts_stress",
            "name": "Farris Intercepts the Stress",
            "category": "farris_presence",
            "act": 2,
            "unique": False,
            "burns": False,
            "cooldown": 2,
            "probability_decay": 0.8,
            "chaos": -0.8,
            "turbulence": -0.3,
            "pressure": 0.0,
            "description": "Farris steps in when Maeve's about to snap. 'Not yet. Not here.'"
        },
        {
            "id": "farris_smells_wrongness",
            "name": "Farris Smells the Wrongness",
            "category": "farris_presence",
            "act": 2,
            "unique": False,
            "burns": False,
            "cooldown": 3,
            "probability_decay": 0.85,
            "chaos": 0.8,
            "turbulence": 0.8,
            "pressure": 0.0,
            "description": "Farris stops mid-sentence, nostrils flaring. 'It's here. Close.'"
        },
        {
            "id": "farris_breaks_tension",
            "name": "Farris Breaks the Tension",
            "category": "farris_presence",
            "act": 2,
            "unique": False,
            "burns": False,
            "cooldown": 2,
            "probability_decay": 0.75,
            "chaos": -0.5,
            "turbulence": -0.5,
            "pressure": 0.2,
            "description": "Farris does something absurd at exactly the right moment. Everyone exhales."
        },
        {
            "id": "daniel_covers_for_maeve",
            "name": "Daniel Covers for Maeve",
            "category": "daniel_institutional",
            "act": 2,
            "unique": False,
            "burns": False,
            "cooldown": 3,
            "probability_decay": 0.8,
            "chaos": -0.3,
            "turbulence": 0.0,
            "pressure": 0.5,
            "description": "Daniel lies to H11 to protect Maeve. It costs him."
        },
        {
            "id": "daniel_detects_pattern",
            "name": "Daniel Detects the Pattern",
            "category": "daniel_institutional",
            "act": 2,
            "unique": False,
            "burns": False,
            "cooldown": 2,
            "probability_decay": 0.85,
            "chaos": 0.8,
            "turbulence": 0.5,
            "pressure": 0.8,
            "description": "Daniel sees the data. The disappearances aren't random. His hands shake."
        }
    ],
    "3": [  # Act 3
        {
            "id": "farris_refuses_alone",
            "name": "Farris Refuses to Let Maeve Go Alone",
            "category": "farris_presence",
            "act": 3,
            "unique": False,
            "burns": False,
            "cooldown": 2,
            "probability_decay": 0.9,
            "chaos": -0.5,
            "turbulence": 0.0,
            "pressure": 0.0,
            "description": "Farris blocks the door. 'If you're walking into it, I'm coming too.'"
        },
        {
            "id": "farris_wolf_sense_door",
            "name": "Wolf-Sense: The Door Is Already Open",
            "category": "farris_presence",
            "act": 3,
            "unique": True,
            "burns": False,
            "cooldown": 0,
            "probability_decay": 1.0,
            "chaos": 2.0,
            "turbulence": 1.5,
            "pressure": 0.5,
            "description": "Farris can feel it: something at Redchurch opened itself. 'The door is already open.'"
        },
        {
            "id": "daniel_makes_call",
            "name": "Daniel Makes the Call",
            "category": "daniel_institutional",
            "act": 3,
            "unique": False,
            "burns": True,
            "cooldown": 0,
            "probability_decay": 1.0,
            "chaos": 3.0,
            "turbulence": 1.0,
            "pressure": 2.0,
            "description": "Daniel calls H11 again. They send a strategist, not a counselor.",
            "burn_effects": {
                "h11_max_pressure": True,
                "dce_ending_path": True
            }
        },
        {
            "id": "daniel_last_warning",
            "name": "Daniel's Last Warning",
            "category": "daniel_institutional",
            "act": 3,
            "unique": False,
            "burns": False,
            "cooldown": 2,
            "probability_decay": 0.9,
            "chaos": 0.5,
            "turbulence": 0.3,
            "pressure": 0.2,
            "description": "Daniel begs Maeve to stop. Fear in his voice she's never heard."
        }
    ]
}

def add_events_to_act_data():
    """Add Farris and Daniel events to act_data.json"""

    # Load existing act_data
    with open('/home/user/MillionEyes/act_data.json', 'r') as f:
        act_data = json.load(f)

    # Add new events to each act
    for act_num_str, new_events in NEW_EVENTS.items():
        if act_num_str in act_data['acts']:
            # Add to existing events
            act_data['acts'][act_num_str]['events'].extend(new_events)
            print(f"✓ Added {len(new_events)} events to Act {act_num_str}")
        else:
            print(f"⚠️  Act {act_num_str} not found in act_data")

    # Save modified act_data
    with open('/home/user/MillionEyes/act_data.json', 'w') as f:
        json.dump(act_data, f, indent=2)

    print("\n✓ Successfully updated act_data.json")

    # Display summary
    for act_num_str in ['1', '2', '3']:
        event_count = len(act_data['acts'][act_num_str]['events'])
        print(f"  Act {act_num_str}: {event_count} total events")

if __name__ == "__main__":
    try:
        add_events_to_act_data()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
