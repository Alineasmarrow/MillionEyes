#!/usr/bin/env python3
"""
Test the Sacred Dyad Conservation Law

This test demonstrates:
1. Sacred dyad formation (C_dyad >= 9.0)
2. Sacred conservation (changes echo between partners)
3. Chaos amplification (sacred bonds shake reality)
4. Catastrophic collapse (sacred break when partner falls)
"""

from simulation import NarrativeSimulation
from events import create_event_deck


def test_sacred_dyad_formation():
    """Test that a dyad becomes sacred when C_dyad >= 9.0"""
    print("=" * 80)
    print("TEST 1: Sacred Dyad Formation")
    print("=" * 80)

    sim = NarrativeSimulation("Sacred Formation Test")

    # Add characters
    sim.add_character("Alice", c_self=8.0)
    sim.add_character("Bob", c_self=8.0)

    # Add relationship starting at 8.5 (close to sacred)
    sim.add_relationship("Alice", "Bob", c_dyad=8.5)

    dyad = sim.get_dyad("Alice", "Bob")
    print(f"Initial dyad: {dyad}")
    print(f"Is sacred: {dyad.is_sacred}")

    # Push it over the threshold
    print("\nIncreasing dyad to 9.5...")
    result = sim.modify_dyad("Alice", "Bob", 1.0, "test increase")

    print(f"New dyad: {dyad}")
    print(f"Is sacred: {dyad.is_sacred}")
    print(f"Became sacred: {result.get('became_sacred', False)}")

    assert dyad.is_sacred, "Dyad should be sacred at C_dyad >= 9.0"
    print("\n✓ TEST PASSED: Sacred dyad forms at C_dyad >= 9.0\n")


def test_sacred_conservation():
    """Test that changes to one character echo in their sacred partner"""
    print("=" * 80)
    print("TEST 2: Sacred Conservation Law")
    print("=" * 80)

    sim = NarrativeSimulation("Sacred Conservation Test")

    # Add characters
    sim.add_character("Kit", c_self=8.0)
    sim.add_character("Yuul", c_self=7.0)

    # Add sacred relationship (start at 9.0)
    sim.add_relationship("Kit", "Yuul", c_dyad=9.5)

    dyad = sim.get_dyad("Kit", "Yuul")
    print(f"Sacred dyad: {dyad}")
    print(f"Coupling strength: {dyad.coupling_strength}")

    print("\nInitial states:")
    print(f"  Kit: C_self = {sim.get_character('Kit').c_self:.1f}")
    print(f"  Yuul: C_self = {sim.get_character('Yuul').c_self:.1f}")

    # Modify Kit
    print("\nKit loses -2.0 C_self...")
    result = sim.modify_character_c_self("Kit", -2.0, "test decrease")

    print(f"\nAfter change:")
    print(f"  Kit: C_self = {sim.get_character('Kit').c_self:.1f}")
    print(f"  Yuul: C_self = {sim.get_character('Yuul').c_self:.1f}")

    # Check echo
    sacred_echoes = result.get('sacred_echoes', [])
    if sacred_echoes:
        print(f"\n⚡ Sacred echo detected:")
        for echo in sacred_echoes:
            print(f"  {echo['partner']}: {echo['delta']:+.1f} → {echo['new_value']:.1f}")

    # Yuul should have echoed the change
    expected_yuul = 7.0 + (-2.0 * dyad.coupling_strength)
    actual_yuul = sim.get_character('Yuul').c_self

    assert abs(actual_yuul - expected_yuul) < 0.01, f"Yuul should be {expected_yuul:.1f} but is {actual_yuul:.1f}"
    print(f"\n✓ TEST PASSED: Sacred conservation applies (coupling: {dyad.coupling_strength:.1%})\n")


def test_chaos_amplification():
    """Test that sacred dyads amplify chaos"""
    print("=" * 80)
    print("TEST 3: Chaos Amplification from Sacred Bonds")
    print("=" * 80)

    sim = NarrativeSimulation("Chaos Amplification Test")

    # Add characters
    sim.add_character("Maeve", c_self=8.0)
    sim.add_character("Rielle", c_self=8.0)

    # Add sacred relationship
    sim.add_relationship("Maeve", "Rielle", c_dyad=9.5)

    print(f"Initial chaos: {sim.chaos:.1f}")

    # Modify Maeve
    print("\nMaeve drops -3.0 C_self...")
    result = sim.modify_character_c_self("Maeve", -3.0, "test drop")

    sacred_chaos = result.get('sacred_chaos', 0)
    print(f"Sacred chaos impact: +{sacred_chaos:.1f}")
    print(f"Final chaos: {sim.chaos:.1f}")

    assert sacred_chaos > 0, "Sacred dyads should amplify chaos"
    print(f"\n✓ TEST PASSED: Sacred bonds shake reality (+{sacred_chaos:.1f} chaos)\n")


def test_catastrophic_collapse():
    """Test sacred break when a partner collapses"""
    print("=" * 80)
    print("TEST 4: Catastrophic Collapse (Sacred Break)")
    print("=" * 80)

    sim = NarrativeSimulation("Sacred Break Test")

    # Add characters
    sim.add_character("Alice", c_self=1.0)  # Near collapse
    sim.add_character("Bob", c_self=8.0)   # Stable

    # Add sacred relationship
    sim.add_relationship("Alice", "Bob", c_dyad=9.5)

    print("Initial states:")
    print(f"  Alice: C_self = {sim.get_character('Alice').c_self:.1f}")
    print(f"  Bob: C_self = {sim.get_character('Bob').c_self:.1f}")
    print(f"  Chaos: {sim.chaos:.1f}")

    # Push Alice to collapse
    print("\nAlice drops -1.5 C_self (collapse)...")
    old_chaos = sim.chaos
    result = sim.modify_character_c_self("Alice", -1.5, "test collapse")

    print(f"\nAfter collapse:")
    print(f"  Alice: C_self = {sim.get_character('Alice').c_self:.1f}")
    print(f"  Bob: C_self = {sim.get_character('Bob').c_self:.1f}")
    print(f"  Chaos: {sim.chaos:.1f} (+{sim.chaos - old_chaos:.1f})")

    # Bob should suffer grief rupture
    bob_c_self = sim.get_character('Bob').c_self

    # Bob should be: 8.0 (initial) + (-1.5 * 0.3 coupling) + (-2.0 grief rupture)
    # = 8.0 - 0.45 - 2.0 = 5.55
    expected_range = (5.0, 6.0)
    assert expected_range[0] <= bob_c_self <= expected_range[1], \
        f"Bob should be in range {expected_range} but is {bob_c_self:.1f}"

    print(f"\n✓ TEST PASSED: Sacred break causes grief rupture\n")


def run_sacred_scenario():
    """Run a full scenario demonstrating sacred dyad mechanics"""
    print("\n" + "=" * 80)
    print("FULL SCENARIO: The Sacred Bond")
    print("=" * 80)

    sim = NarrativeSimulation("The Sacred Bond")

    # Create Kit and Yuul with high relationship
    sim.add_character("Kit", c_self=7.0)
    sim.add_character("Yuul", c_self=5.0)
    sim.add_character("Maeve", c_self=7.0)

    # Kit-Yuul start at 8.5 (almost sacred)
    sim.add_relationship("Kit", "Yuul", c_dyad=8.5)
    sim.add_relationship("Kit", "Maeve", c_dyad=6.5)
    sim.add_relationship("Yuul", "Maeve", c_dyad=6.0)

    sim.chaos = 10.0

    # Manually trigger specific events
    deck = create_event_deck()

    # Round 1: Kit Makes a Promise (should push Kit-Yuul to sacred)
    print("\n🎯 Forcing Card 18: Kit Makes a Promise")
    sim.run_round(deck[17])  # Card 18

    # Round 2: Kit Overextends
    print("\n🎯 Forcing Card 7: Kit Overextends")
    sim.run_round(deck[6])   # Card 7

    # Round 3: Random event
    sim.run_round()

    sim.print_final_state()


if __name__ == "__main__":
    print("\n🔬 TESTING SACRED DYAD CONSERVATION LAW\n")

    # Run tests
    test_sacred_dyad_formation()
    test_sacred_conservation()
    test_chaos_amplification()
    test_catastrophic_collapse()

    print("=" * 80)
    print("ALL TESTS PASSED ✓")
    print("=" * 80)

    # Run full scenario
    run_sacred_scenario()

    print("\n✓ Sacred Dyad Conservation Law fully functional!\n")
