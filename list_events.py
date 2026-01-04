#!/usr/bin/env python3
"""
List all available event cards in the Narrative Coherence Engine
"""

from events import create_event_deck


def list_all_events():
    """Display all event cards with their details"""

    deck = create_event_deck()

    print("=" * 80)
    print("NARRATIVE COHERENCE ENGINE - EVENT DECK")
    print("=" * 80)
    print(f"\nTotal Cards: {len(deck)}\n")

    # Group by category
    categories = {}
    for event in deck:
        if event.category not in categories:
            categories[event.category] = []
        categories[event.category].append(event)

    # Category display names
    category_names = {
        "yuul_vulnerability": "YUUL VULNERABILITY",
        "kit_hidden_feelings": "KIT'S HIDDEN FEELINGS",
        "trine": "TRINE FRACTURE",
        "external_pressure": "EXTERNAL PRESSURE",
        "salvation": "POTENTIAL SALVATION",
        "wild_card": "WILD CARDS"
    }

    # Display by category
    for category_key in [
        "yuul_vulnerability",
        "kit_hidden_feelings",
        "trine",
        "external_pressure",
        "salvation",
        "wild_card"
    ]:
        if category_key in categories:
            print(f"\n{category_names[category_key]}")
            print("-" * 80)

            for event in categories[category_key]:
                chaos_value = event.chaos
                chaos_label = chaos_value if not isinstance(chaos_value, dict) else " / ".join(
                    f"{key}:{value}" for key, value in chaos_value.items()
                )
                chaos_symbol = "+" if isinstance(event.chaos_base, (int, float)) and event.chaos_base >= 0 else ""
                print(f"\n[{event.id:2d}] {event.name}")
                if isinstance(chaos_value, (int, float)):
                    print(f"     Chaos: {chaos_symbol}{event.chaos_base:.0f}")
                else:
                    print(f"     Chaos: {chaos_label}")
                print(
                    "     Unique: {unique} | Cooldown: {cooldown} | Decay: {decay} | Choice: {choice}".format(
                        unique=event.unique,
                        cooldown=event.cooldown,
                        decay=event.probability_decay,
                        choice=event.choice_hook
                    )
                )
                print(f"     {event.description}")


def list_by_chaos_impact():
    """List events sorted by chaos impact"""

    deck = create_event_deck()

    print("\n" + "=" * 80)
    print("EVENTS BY CHAOS IMPACT")
    print("=" * 80)

    # Sort by chaos (most stabilizing first)
    sorted_deck = sorted(deck, key=lambda e: e.chaos_base)

    print("\nSTABILIZING (Negative Chaos):")
    print("-" * 80)
    for event in sorted_deck:
        if event.chaos_base < 0:
            print(f"  [{event.id:2d}] {event.name:40s} Chaos: {event.chaos_base:+.0f}")

    print("\nNEUTRAL (Zero Chaos):")
    print("-" * 80)
    for event in sorted_deck:
        if event.chaos_base == 0:
            print(f"  [{event.id:2d}] {event.name:40s} Chaos: {event.chaos_base:+.0f}")

    print("\nDESTABILIZING (Positive Chaos):")
    print("-" * 80)
    for event in sorted_deck:
        if event.chaos_base > 0:
            print(f"  [{event.id:2d}] {event.name:40s} Chaos: {event.chaos_base:+.0f}")


if __name__ == "__main__":
    import sys

    print("🎭 NARRATIVE COHERENCE ENGINE - EVENT CARD REFERENCE\n")

    if len(sys.argv) > 1 and sys.argv[1] == "--chaos":
        list_by_chaos_impact()
    else:
        list_all_events()

    print("\n" + "=" * 80)
    print("Use: python list_events.py --chaos   to see cards sorted by chaos impact")
    print("=" * 80)
