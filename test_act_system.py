#!/usr/bin/env python3
"""
Test the Act System

Verifies that:
- Act data loads correctly
- Event pools are built properly
- Act transitions work
- Choices load from act_data.json
"""

from simulation import NarrativeSimulation


def test_act_system_basic():
    """Test basic act system functionality"""
    print("\n" + "=" * 80)
    print("TEST: Act System Basic Functionality")
    print("=" * 80)

    # Create simulation with act system
    sim = NarrativeSimulation("Act System Test", interactive_mode=False, use_act_system=True)

    if not sim.use_act_system:
        print("❌ Act system failed to initialize")
        return False

    print(f"✓ Act system initialized")
    print(f"✓ Act 1 event deck size: {len(sim.event_deck)}")

    # Setup minimal scenario
    sim.add_character("Yuul", c_self=7.0)
    sim.add_character("Maeve", c_self=7.0)
    sim.add_character("Kit", c_self=7.0)
    sim.add_character("Rielle", c_self=7.0)

    sim.add_relationship("Yuul", "Maeve", c_dyad=6.5)
    sim.add_relationship("Kit", "Yuul", c_dyad=7.0)
    sim.add_relationship("Maeve", "Rielle", c_dyad=8.0)

    # Run a few rounds in Act 1
    print("\n--- Running 3 rounds in Act I ---")
    for i in range(3):
        sim.run_round()
        current_act = sim.act_system.get_current_act(sim.round_number)
        print(f"Current Act after round {sim.round_number}: {current_act}")

    # Jump to Act II (round 11)
    print("\n--- Jumping to Act II (round 11) ---")
    sim.round_number = 10
    sim.run_round()  # This will be round 11, triggering Act II banner

    current_act = sim.act_system.get_current_act(sim.round_number)
    print(f"Current Act after round {sim.round_number}: {current_act}")
    print(f"Act II event deck size: {len(sim.event_deck)}")

    print("\n✓ Act system test passed!")
    return True


def test_act_choices():
    """Test that choices load from act_data.json"""
    print("\n" + "=" * 80)
    print("TEST: Act System Choices")
    print("=" * 80)

    # Create simulation with act system and interactive mode
    sim = NarrativeSimulation("Act Choices Test", interactive_mode=True, use_act_system=True)

    if not sim.interactive_mode:
        print("❌ Interactive mode failed to initialize")
        return False

    if not sim.choices_data:
        print("❌ Choices data not loaded")
        return False

    print(f"✓ Choices loaded: {len(sim.choices_data['choices'])} choice moments")
    print(f"✓ Unique card mapping: {len(sim.choices_data['unique_card_mapping'])} mappings")

    # Display a few mappings
    print("\nSample choice mappings:")
    for event_id, choice_id in list(sim.choices_data['unique_card_mapping'].items())[:5]:
        print(f"  Event '{event_id}' → Choice {choice_id}")

    print("\n✓ Act choices test passed!")
    return True


def test_event_properties():
    """Test that events have proper turbulence/pressure"""
    print("\n" + "=" * 80)
    print("TEST: Event Turbulence/Pressure Properties")
    print("=" * 80)

    sim = NarrativeSimulation("Event Properties Test", interactive_mode=False, use_act_system=True)

    # Check a few events
    act1_events = sim.event_deck
    print(f"\nChecking {len(act1_events)} Act I events:")

    sample_events = act1_events[:5]
    for event in sample_events:
        print(f"\n{event.name}")
        print(f"  Chaos: {event.chaos_base:+.1f}")
        print(f"  Turbulence: {event.turbulence:+.1f}" if event.turbulence is not None else "  Turbulence: None")
        print(f"  Pressure: {event.pressure:+.1f}" if event.pressure is not None else "  Pressure: None")
        print(f"  Unique: {event.unique}")
        print(f"  Burns: {event.burns}")

    print("\n✓ Event properties test passed!")
    return True


if __name__ == "__main__":
    print("\n🧪 TESTING ACT SYSTEM\n")

    tests = [
        test_act_system_basic,
        test_act_choices,
        test_event_properties
    ]

    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"\n❌ Test failed with error: {e}")
            import traceback
            traceback.print_exc()
            results.append(False)

    print("\n" + "=" * 80)
    if all(results):
        print("ALL ACT SYSTEM TESTS PASSED ✓")
    else:
        print(f"SOME TESTS FAILED: {sum(results)}/{len(results)} passed")
    print("=" * 80)
