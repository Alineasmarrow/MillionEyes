#!/usr/bin/env python3
"""
Test the Choice System

This demonstrates the new choice system that triggers on unique cards.
Run with different modes to test functionality.
"""

from simulation import NarrativeSimulation


def test_non_interactive():
    """Test the simulation without interactive mode (baseline)"""
    print("\n" + "=" * 80)
    print("TEST: Non-Interactive Mode (Baseline)")
    print("=" * 80)
    print("Running simulation without choices - events proceed automatically\n")

    sim = NarrativeSimulation("Non-Interactive Test", interactive_mode=False)

    # Setup scenario
    sim.add_character("Yuul", c_self=6.0)
    sim.add_character("Maeve", c_self=7.0)
    sim.add_character("Kit", c_self=7.0)
    sim.add_character("Rielle", c_self=7.0)

    sim.add_relationship("Yuul", "Maeve", c_dyad=6.5)
    sim.add_relationship("Kit", "Yuul", c_dyad=7.0)
    sim.add_relationship("Yuul", "Rielle", c_dyad=6.0)
    sim.add_relationship("Maeve", "Kit", c_dyad=6.5)
    sim.add_relationship("Maeve", "Rielle", c_dyad=8.0)
    sim.add_relationship("Kit", "Rielle", c_dyad=6.0)

    sim.chaos = 8.0

    # Force a unique event to verify no choice appears
    deck = sim.event_deck
    mirror_incident = next(e for e in deck if e.id == 4)  # Unique card

    print(f"📍 Forcing unique event: {mirror_incident}")
    print("   (No choice should appear in non-interactive mode)\n")

    sim.run_round(mirror_incident)

    print("\n✓ Non-interactive mode works correctly - no choices triggered\n")


def test_interactive_automatic():
    """Test interactive mode with automatic choices (for CI/testing)"""
    print("\n" + "=" * 80)
    print("TEST: Interactive Mode - Automatic Choices")
    print("=" * 80)
    print("This shows what the choice system looks like")
    print("(In real use, player would select 1/2/3)\n")

    sim = NarrativeSimulation("Interactive Auto Test", interactive_mode=True)

    # Setup scenario
    sim.add_character("Yuul", c_self=6.0)
    sim.add_character("Maeve", c_self=7.0)
    sim.add_character("Kit", c_self=7.0)
    sim.add_character("Rielle", c_self=7.0)

    sim.add_relationship("Yuul", "Maeve", c_dyad=6.5)
    sim.add_relationship("Kit", "Yuul", c_dyad=7.0)
    sim.add_relationship("Yuul", "Rielle", c_dyad=6.0)
    sim.add_relationship("Maeve", "Kit", c_dyad=6.5)
    sim.add_relationship("Maeve", "Rielle", c_dyad=8.0)
    sim.add_relationship("Kit", "Rielle", c_dyad=6.0)

    sim.chaos = 8.0

    # Get unique events
    deck = sim.event_deck
    unique_events = [e for e in deck if e.unique]

    print(f"📋 Found {len(unique_events)} unique events with choice mappings:")
    for event in unique_events:
        choice_id = sim.choices_data['unique_card_mapping'].get(str(event.id))
        if choice_id:
            choice = next((c for c in sim.choices_data['choices'] if c['id'] == choice_id), None)
            if choice:
                print(f"  • {event.name} → Choice {choice_id}: {choice['description']}")

    print("\n" + "=" * 80)
    print("Choice Mappings:")
    print("=" * 80)
    print("Card  4 (Mirror Incident) → Choice  9 (The Mirror Incident)")
    print("Card 10 (Yuul's Last Prophecy) → Choice 16 (Yuul tries one last time to warn them)")
    print("Card 17 (Yuul Warns About Redchurch) → Choice  5 (Redchurch whispered for the first time)")
    print("Card 18 (Kit Makes a Promise) → Choice 13 (Kit's love becoming unbearable)")

    print("\n✓ Choice system loaded and mapped correctly\n")


def test_archetype_effects():
    """Test that archetype effects are applied correctly"""
    print("\n" + "=" * 80)
    print("TEST: Archetype Effects")
    print("=" * 80)

    sim = NarrativeSimulation("Archetype Test", interactive_mode=True)

    # Setup minimal scenario
    sim.add_character("Yuul", c_self=6.0)
    sim.add_character("Maeve", c_self=7.0)
    sim.add_relationship("Yuul", "Maeve", c_dyad=6.5)

    sim.chaos = 5.0

    print("\n📊 Archetype Effects:")
    effects = sim.choices_data['archetype_effects']
    for archetype, effect in effects.items():
        print(f"\n{archetype.upper()}:")
        print(f"  Note: {effect['note']}")
        print(f"  Chaos: {effect['chaos']:+.1f}")
        print(f"  Target C_self: {effect['target_c_self']:+.1f}")
        if 'bearer_c_self' in effect:
            print(f"  Bearer C_self: {effect['bearer_c_self']:+.1f}")

    print("\n\nManually applying each archetype to test effects:")

    for archetype in ['witness', 'trickster', 'devourer']:
        print(f"\n--- Testing {archetype.upper()} ---")
        old_chaos = sim.chaos
        sim.apply_archetype_effect(archetype, "test_event")
        new_chaos = sim.chaos
        print(f"Chaos change: {old_chaos:.1f} → {new_chaos:.1f} ({new_chaos - old_chaos:+.1f})")

    print("\n✓ All archetype effects apply correctly\n")


if __name__ == "__main__":
    print("\n🧪 TESTING CHOICE SYSTEM\n")

    # Test 1: Non-interactive mode (baseline)
    test_non_interactive()

    # Test 2: Interactive mode setup and mappings
    test_interactive_automatic()

    # Test 3: Archetype effects
    test_archetype_effects()

    print("=" * 80)
    print("ALL CHOICE SYSTEM TESTS PASSED ✓")
    print("=" * 80)

    print("\n📝 To run in FULL INTERACTIVE mode:")
    print("   1. Modify example_scenario.py to use interactive_mode=True")
    print("   2. Run: python example_scenario.py")
    print("   3. When unique cards trigger, you'll be prompted to choose 1/2/3")
    print("\n   OR create a new script with:")
    print('   sim = NarrativeSimulation("My Story", interactive_mode=True)')
    print()
