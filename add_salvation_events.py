#!/usr/bin/env python3
"""
Add Salvation and Miracle Events to act_data.json

Adds Act 2 salvation events (positive momentum cards) and Act 3 miracle events.
"""

import json

# Act 2 Salvation Events
ACT2_SALVATION = [
    {
        "id": "brief_reprieve",
        "name": "Brief Reprieve",
        "act": 2,
        "category": "salvation",
        "unique": False,
        "burns": False,
        "cooldown": 3,
        "probability_decay": 0.9,
        "chaos": -1.0,
        "turbulence": 0.0,
        "pressure": -0.5,
        "description": "A hunt ends cleanly. A call ends early. No one screams, dissolves, or bleeds. A breath of quiet in the storm."
    },
    {
        "id": "unexpected_kindness",
        "name": "Unexpected Kindness",
        "act": 2,
        "category": "external_salvation",
        "unique": False,
        "burns": False,
        "cooldown": 3,
        "probability_decay": 0.85,
        "chaos": -0.5,
        "turbulence": 0.0,
        "pressure": -1.0,
        "description": "A stranger they once helped returns the kindness. A reminder that not everything hunts them."
    },
    {
        "id": "house_remembers",
        "name": "The House Remembers Them",
        "act": 2,
        "category": "environment",
        "unique": False,
        "burns": False,
        "cooldown": 4,
        "probability_decay": 0.9,
        "chaos": -1.0,
        "turbulence": -1.0,
        "pressure": 0.0,
        "description": "The wards glow steady for the first time in months. The Sanctuary feels like home again."
    },
    {
        "id": "maeve_field_bows",
        "name": "The Field Bows to Her",
        "act": 2,
        "category": "maeve_resonance",
        "unique": True,
        "burns": False,
        "cooldown": 0,
        "probability_decay": 1.0,
        "chaos": -1.5,
        "turbulence": 0.0,
        "pressure": -1.0,
        "description": "Maeve makes a call only she can see. The world reacts. For a moment her brilliance stabilizes everyone."
    },
    {
        "id": "kit_refuses_to_give_up",
        "name": "He Refuses to Give Up",
        "act": 2,
        "category": "kit_heroics",
        "unique": False,
        "burns": False,
        "cooldown": 2,
        "probability_decay": 0.8,
        "chaos": -1.0,
        "turbulence": 0.0,
        "pressure": 0.0,
        "description": "Kit anchors Yuul with desperate tenderness. He becomes the spine of the household."
    },
    {
        "id": "rielle_truth",
        "name": "She Tells the Truth No One Wants to Hear",
        "act": 2,
        "category": "rielle_insight",
        "unique": False,
        "burns": False,
        "cooldown": 2,
        "probability_decay": 0.85,
        "chaos": -0.5,
        "turbulence": 0.0,
        "pressure": -0.5,
        "description": "Rielle corners someone and speaks a truth that breaks the spiral. Someone finally listens."
    },
    {
        "id": "daniel_fixes",
        "name": "He Fixes Something, Quietly",
        "act": 2,
        "category": "h11_daniel",
        "unique": False,
        "burns": False,
        "cooldown": 3,
        "probability_decay": 0.8,
        "chaos": -1.0,
        "turbulence": 0.0,
        "pressure": -1.0,
        "description": "Daniel pulls strings behind the scenes—reroutes a case, deletes a file. Buys them time."
    },
    {
        "id": "farris_stands_guard",
        "name": "He Stands Between Them and the Dark",
        "act": 2,
        "category": "farris_protection",
        "unique": True,
        "burns": False,
        "cooldown": 0,
        "probability_decay": 1.0,
        "chaos": -2.0,
        "turbulence": -1.0,
        "pressure": 0.0,
        "description": "A presence moves toward the Sanctuary. Farris moves faster. He destroys what approaches, at cost to himself."
    }
]

# Act 3 Miracle Events
ACT3_MIRACLES = [
    {
        "id": "maeve_field_bows_act3",
        "name": "The Field Bows to Her",
        "act": 3,
        "category": "maeve_resonance",
        "unique": True,
        "burns": False,
        "cooldown": 0,
        "probability_decay": 1.0,
        "chaos": -2.0,
        "turbulence": 0.0,
        "pressure": -1.0,
        "description": "Maeve steps into the wound in the field and stitches it shut with sheer force of will. A psychic lighthouse flickers into being."
    },
    {
        "id": "kit_refuses_act3",
        "name": "He Refuses to Give Up",
        "act": 3,
        "category": "kit_heroics",
        "unique": True,
        "burns": False,
        "cooldown": 0,
        "probability_decay": 1.0,
        "chaos": -1.0,
        "turbulence": 0.0,
        "pressure": 0.0,
        "description": "Someone is seconds from dissolving. Kit anchors them with desperate tenderness, dragging them back from the brink."
    },
    {
        "id": "rielle_breaks_pattern_act3",
        "name": "She Breaks the Pattern",
        "act": 3,
        "category": "rielle_insight",
        "unique": True,
        "burns": False,
        "cooldown": 0,
        "probability_decay": 1.0,
        "chaos": -1.0,
        "turbulence": -2.0,
        "pressure": -1.0,
        "description": "Rielle sees the resonance knot trapping them and cuts it with furious, impossible clarity."
    },
    {
        "id": "daniel_protocol_null_act3",
        "name": "Protocol Null: He Chooses Them",
        "act": 3,
        "category": "h11_daniel",
        "unique": True,
        "burns": False,
        "cooldown": 0,
        "probability_decay": 1.0,
        "chaos": -1.0,
        "turbulence": 0.0,
        "pressure": -3.0,
        "description": "Daniel breaks protocol and sabotages a Directorate operation. For one moment, he is theirs."
    },
    {
        "id": "farris_holds_line_act3",
        "name": "He Holds the Line Alone",
        "act": 3,
        "category": "farris_resonance",
        "unique": True,
        "burns": False,
        "cooldown": 0,
        "probability_decay": 1.0,
        "chaos": -3.0,
        "turbulence": -1.0,
        "pressure": 0.0,
        "description": "A monstrous presence tears through the field. Farris stands alone, and reality bends around his defiance."
    },
    {
        "id": "yuul_remembers_act3",
        "name": "She Remembers Herself Completely",
        "act": 3,
        "category": "yuul_prophecy",
        "unique": True,
        "burns": False,
        "cooldown": 0,
        "probability_decay": 1.0,
        "chaos": -3.0,
        "turbulence": 0.0,
        "pressure": 0.0,
        "description": "For one impossible moment, Yuul is whole—prophet and human, bound and free. She hands them a vision of the perfect path."
    }
]


def add_salvation_events():
    """Add salvation and miracle events to act_data.json"""

    # Load existing act_data
    with open('/home/user/MillionEyes/act_data.json', 'r') as f:
        act_data = json.load(f)

    # Add Act 2 salvation events
    if '2' in act_data['acts']:
        act_data['acts']['2']['events'].extend(ACT2_SALVATION)
        print(f"✓ Added {len(ACT2_SALVATION)} salvation events to Act 2")
    else:
        print("⚠️  Act 2 not found in act_data")

    # Add Act 3 miracle events
    if '3' in act_data['acts']:
        act_data['acts']['3']['events'].extend(ACT3_MIRACLES)
        print(f"✓ Added {len(ACT3_MIRACLES)} miracle events to Act 3")
    else:
        print("⚠️  Act 3 not found in act_data")

    # Save modified act_data
    with open('/home/user/MillionEyes/act_data.json', 'w') as f:
        json.dump(act_data, f, indent=2)

    print("\n✓ Successfully updated act_data.json")

    # Display summary
    for act_num_str in ['1', '2', '3']:
        if act_num_str in act_data['acts']:
            event_count = len(act_data['acts'][act_num_str]['events'])
            print(f"  Act {act_num_str}: {event_count} total events")


if __name__ == "__main__":
    try:
        add_salvation_events()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
