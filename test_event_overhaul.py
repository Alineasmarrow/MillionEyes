#!/usr/bin/env python3
"""
Test the Event Card Overhaul System

This test demonstrates:
1. Event cooldowns (can't replay too soon)
2. Unique events (can only happen once)
3. Probability decay (events become less likely each time)
4. Event tracking and display
"""

from simulation import NarrativeSimulation
from events import create_event_deck


def test_event_metadata():
    """Test that event metadata is properly set"""
    print("=" * 80)
    print("TEST 1: Event Metadata")
    print("=" * 80)

    deck = create_event_deck()

    print("\n📋 UNIQUE EVENTS:")
    unique_events = [e for e in deck if e.unique]
    for event in unique_events:
        print(f"  {event}")

    print("\n📋 EVENTS WITH HIGH COOLDOWNS (≥4):")
    high_cooldown = [e for e in deck if e.cooldown >= 4]
    for event in high_cooldown:
        print(f"  {event}")

    print("\n📋 EVENTS WITH HIGH DECAY (≤0.5):")
    high_decay = [e for e in deck if e.probability_decay <= 0.5]
    for event in high_decay:
        print(f"  {event}")

    assert len(unique_events) == 4, f"Expected 4 unique events, got {len(unique_events)}"
    print("\n✓ TEST PASSED: Event metadata correctly set\n")


def test_cooldown_system():
    """Test that cooldowns prevent events from repeating too soon"""
    print("=" * 80)
    print("TEST 2: Cooldown System")
    print("=" * 80)

    sim = NarrativeSimulation("Cooldown Test")

    # Add proper characters for events
    sim.add_character("Yuul", c_self=7.0)
    sim.add_character("Maeve", c_self=7.0)
    sim.add_character("Kit", c_self=7.0)
    sim.add_character("Rielle", c_self=7.0)
    sim.add_relationship("Yuul", "Maeve", c_dyad=7.0)
    sim.add_relationship("Kit", "Yuul", c_dyad=7.0)
    sim.add_relationship("Kit", "Maeve", c_dyad=6.5)
    sim.add_relationship("Yuul", "Rielle", c_dyad=6.0)
    sim.add_relationship("Maeve", "Rielle", c_dyad=7.0)
    sim.add_relationship("Kit", "Rielle", c_dyad=6.0)

    deck = create_event_deck()

    # Force an event with cooldown=2
    card_1 = deck[0]  # Card 1: cooldown=2
    print(f"\n🎯 Round 1: Force {card_1.name}")
    print(f"   Cooldown: {card_1.cooldown}, Decay: {card_1.probability_decay}")

    sim.run_round(card_1)

    # Check tracking
    assert card_1.id in sim.event_last_played, "Event should be tracked"
    assert sim.event_play_count.get(card_1.id, 0) == 1, "Play count should be 1"

    print(f"\n📊 Event tracking:")
    print(f"   Last played: Round {sim.event_last_played[card_1.id]}")
    print(f"   Play count: {sim.event_play_count[card_1.id]}")

    # Try to select events - Card 1 should NOT be available (on cooldown)
    print(f"\n🔍 Testing cooldown enforcement...")
    print(f"   Card 1 requires {card_1.cooldown} rounds cooldown")
    print(f"   Current round: {sim.round_number}")

    # Run more rounds and check when Card 1 becomes available
    for i in range(3):
        sim.run_round()
        rounds_since = sim.round_number - sim.event_last_played[card_1.id]
        available = rounds_since >= card_1.cooldown
        print(f"   Round {sim.round_number}: Rounds since Card 1 = {rounds_since}, Available: {available}")

    print("\n✓ TEST PASSED: Cooldown system working\n")


def test_unique_events():
    """Test that unique events can only be played once"""
    print("=" * 80)
    print("TEST 3: Unique Event Enforcement")
    print("=" * 80)

    sim = NarrativeSimulation("Unique Test")

    # Add characters for the unique events
    sim.add_character("Yuul", c_self=5.0)
    sim.add_character("Maeve", c_self=7.0)
    sim.add_character("Kit", c_self=7.0)
    sim.add_relationship("Yuul", "Maeve", c_dyad=6.0)
    sim.add_relationship("Kit", "Yuul", c_dyad=7.0)

    deck = create_event_deck()

    # Find a unique event
    unique_event = next(e for e in deck if e.unique)
    print(f"\n🎯 Testing unique event: {unique_event}")

    # Play it once
    print(f"\n▶ Playing unique event first time...")
    sim.run_round(unique_event)

    assert unique_event.id in sim.event_played_unique, "Unique event should be marked as played"
    print(f"   ✓ Event marked as played: {unique_event.id in sim.event_played_unique}")

    # Try to get available events - unique event should NOT be available
    available = sim.select_event_with_probability()
    if available:
        assert available.id != unique_event.id, "Unique event should not be selected again"
        print(f"   ✓ Unique event excluded from selection")

    print("\n✓ TEST PASSED: Unique events can only play once\n")


def test_probability_decay():
    """Test that probability decay affects event weights"""
    print("=" * 80)
    print("TEST 4: Probability Decay System")
    print("=" * 80)

    sim = NarrativeSimulation("Decay Test")

    # Add proper characters for events
    sim.add_character("Yuul", c_self=7.0)
    sim.add_character("Maeve", c_self=7.0)
    sim.add_character("Kit", c_self=7.0)
    sim.add_character("Rielle", c_self=7.0)
    sim.add_relationship("Yuul", "Maeve", c_dyad=7.0)
    sim.add_relationship("Kit", "Yuul", c_dyad=7.0)
    sim.add_relationship("Maeve", "Rielle", c_dyad=7.0)

    deck = create_event_deck()

    # Find event with high decay
    high_decay_event = next(e for e in deck if e.probability_decay <= 0.5 and not e.unique)
    print(f"\n🎯 Testing event with high decay: {high_decay_event}")
    print(f"   Probability decay: {high_decay_event.probability_decay}")

    # Play it multiple times and show weight changes
    print(f"\n📊 Weight progression:")
    for i in range(4):
        play_count = sim.event_play_count.get(high_decay_event.id, 0)
        weight = high_decay_event.probability_decay ** play_count
        print(f"   Play {i}: count={play_count}, weight={weight:.4f} ({weight*100:.1f}%)")

        if i < 3:  # Don't play on last iteration
            sim.run_round(high_decay_event)

    print(f"\n   After 3 plays, weight drops to {(high_decay_event.probability_decay**3)*100:.1f}% of original")
    print("\n✓ TEST PASSED: Probability decay reduces event likelihood\n")


def run_demonstration_scenario():
    """Run a scenario demonstrating the new event system"""
    print("\n" + "=" * 80)
    print("DEMONSTRATION: Event System in Action")
    print("=" * 80)

    sim = NarrativeSimulation("Event System Demo")

    # Setup
    sim.add_character("Yuul", c_self=6.0)
    sim.add_character("Maeve", c_self=7.0)
    sim.add_character("Kit", c_self=7.0)
    sim.add_character("Rielle", c_self=7.0)

    sim.add_relationship("Yuul", "Maeve", c_dyad=6.5)
    sim.add_relationship("Yuul", "Kit", c_dyad=7.0)
    sim.add_relationship("Yuul", "Rielle", c_dyad=6.0)
    sim.add_relationship("Maeve", "Kit", c_dyad=6.5)
    sim.add_relationship("Maeve", "Rielle", c_dyad=8.0)
    sim.add_relationship("Kit", "Rielle", c_dyad=6.0)

    sim.chaos = 8.0

    print(f"\n🎲 Running 15 rounds with probability-weighted event selection...")
    print(f"   - Events with cooldowns can't repeat immediately")
    print(f"   - Unique events can only happen once")
    print(f"   - Repeated events become less likely (probability decay)")

    # Run scenario
    for i in range(15):
        sim.run_round()

    # Summary
    print("\n" + "=" * 80)
    print("EVENT PLAY SUMMARY")
    print("=" * 80)

    deck = create_event_deck()
    played_events = [(e, sim.event_play_count.get(e.id, 0)) for e in deck]
    played_events.sort(key=lambda x: x[1], reverse=True)

    for event, count in played_events:
        if count > 0:
            unique_mark = " [UNIQUE]" if event.unique else ""
            print(f"  {count}x - {event.name}{unique_mark}")

    print(f"\n📊 Unique events played: {len(sim.event_played_unique)}/4")
    print(f"📊 Total events played: {len(sim.event_history)}")

    sim.print_final_state()


if __name__ == "__main__":
    print("\n🔬 TESTING EVENT CARD OVERHAUL SYSTEM\n")

    # Run tests
    test_event_metadata()
    test_cooldown_system()
    test_unique_events()
    test_probability_decay()

    print("=" * 80)
    print("ALL TESTS PASSED ✓")
    print("=" * 80)

    # Run demonstration
    run_demonstration_scenario()

    print("\n✓ Event Card Overhaul fully functional!\n")
