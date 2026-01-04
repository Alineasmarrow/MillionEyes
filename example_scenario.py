#!/usr/bin/env python3
"""
Example scenario: The Descent
A simulation showing Yuul's deterioration and the group's response
"""

from simulation import NarrativeSimulation


def run_descent_scenario():
    """
    The Descent: Yuul is already struggling, the Trine is functional but strained,
    and Kit is silently bearing too much weight.
    """

    # Create the simulation
    sim = NarrativeSimulation("The Descent")

    # Add characters with starting states
    print("Setting up characters...")

    # Yuul starts in Crisis
    sim.add_character("Yuul", c_self=3.5)

    # Maeve is functional but stressed
    sim.add_character("Maeve", c_self=6.0)

    # Kit is grounded but masking exhaustion
    sim.add_character("Kit", c_self=6.5)

    # Rielle is stable, maybe the most stable
    sim.add_character("Rielle", c_self=7.5)

    # Add relationships
    print("Setting up relationships...")

    # The Witch Trine dyads
    sim.add_relationship("Maeve", "Yuul", c_dyad=5.5)  # Strained
    sim.add_relationship("Maeve", "Rielle", c_dyad=7.0)  # Strong
    sim.add_relationship("Yuul", "Rielle", c_dyad=6.0)  # Functional

    # Kit's relationships
    sim.add_relationship("Kit", "Yuul", c_dyad=7.5)  # Strong (he cares deeply)
    sim.add_relationship("Kit", "Maeve", c_dyad=6.5)  # Functional
    sim.add_relationship("Kit", "Rielle", c_dyad=6.0)  # Functional

    # Set initial chaos
    sim.chaos = 8.0  # Already elevated

    # Run the scenario for 12 rounds
    sim.run_scenario(num_rounds=12)

    # Save the log
    sim.save_log("descent_log.txt")


def run_custom_scenario():
    """
    Custom scenario where you can define your own starting conditions
    and run specific events.
    """

    # Create the simulation
    sim = NarrativeSimulation("Custom Scenario")

    # Add your characters
    sim.add_character("Yuul", c_self=5.0)
    sim.add_character("Maeve", c_self=7.0)
    sim.add_character("Kit", c_self=7.0)
    sim.add_character("Rielle", c_self=8.0)

    # Add relationships
    sim.add_relationship("Maeve", "Yuul", c_dyad=7.0)
    sim.add_relationship("Maeve", "Rielle", c_dyad=8.0)
    sim.add_relationship("Yuul", "Rielle", c_dyad=7.0)
    sim.add_relationship("Kit", "Yuul", c_dyad=8.0)
    sim.add_relationship("Kit", "Maeve", c_dyad=7.0)
    sim.add_relationship("Kit", "Rielle", c_dyad=7.0)

    # Set starting chaos
    sim.chaos = 5.0

    # Run with random events
    sim.run_scenario(num_rounds=10)

    # Save the log
    sim.save_log("custom_log.txt")


def run_high_chaos_scenario():
    """
    High Chaos scenario: Everything is already falling apart.
    Can they pull back from the brink?
    """

    sim = NarrativeSimulation("Edge of Collapse")

    # Everyone is struggling
    sim.add_character("Yuul", c_self=2.0)  # Dissolving
    sim.add_character("Maeve", c_self=4.5)  # Strained
    sim.add_character("Kit", c_self=4.0)  # Strained
    sim.add_character("Rielle", c_self=5.5)  # Functional (barely)

    # Relationships are damaged
    sim.add_relationship("Maeve", "Yuul", c_dyad=4.0)
    sim.add_relationship("Maeve", "Rielle", c_dyad=5.5)
    sim.add_relationship("Yuul", "Rielle", c_dyad=4.5)
    sim.add_relationship("Kit", "Yuul", c_dyad=6.0)  # Kit still holding on
    sim.add_relationship("Kit", "Maeve", c_dyad=4.5)
    sim.add_relationship("Kit", "Rielle", c_dyad=5.0)

    # Chaos is very high
    sim.chaos = 15.0  # Near threshold

    print("\n⚠️  WARNING: Starting at high chaos! CoR manifestation imminent!")

    # Run scenario
    sim.run_scenario(num_rounds=8)

    # Save the log
    sim.save_log("high_chaos_log.txt")


def run_ideal_scenario():
    """
    Ideal scenario: Everyone starts stable and connected.
    How long can they maintain it?
    """

    sim = NarrativeSimulation("The Golden Age")

    # Everyone is stable
    sim.add_character("Yuul", c_self=7.0)
    sim.add_character("Maeve", c_self=8.0)
    sim.add_character("Kit", c_self=7.5)
    sim.add_character("Rielle", c_self=8.0)

    # Strong relationships
    sim.add_relationship("Maeve", "Yuul", c_dyad=8.0)
    sim.add_relationship("Maeve", "Rielle", c_dyad=8.5)
    sim.add_relationship("Yuul", "Rielle", c_dyad=7.5)
    sim.add_relationship("Kit", "Yuul", c_dyad=8.0)
    sim.add_relationship("Kit", "Maeve", c_dyad=7.5)
    sim.add_relationship("Kit", "Rielle", c_dyad=7.5)

    # Low chaos
    sim.chaos = 2.0

    print("\n✨ Starting from ideal conditions...")

    # Run scenario
    sim.run_scenario(num_rounds=15)

    # Save the log
    sim.save_log("golden_age_log.txt")


if __name__ == "__main__":
    import sys

    print("🎭 NARRATIVE COHERENCE ENGINE")
    print("=" * 80)
    print("\nAvailable scenarios:")
    print("  1. The Descent (default) - Yuul in crisis, group strained")
    print("  2. Custom - Moderate starting conditions")
    print("  3. Edge of Collapse - High chaos, everyone struggling")
    print("  4. The Golden Age - Ideal starting conditions")
    print()

    choice = input("Select scenario (1-4) or press Enter for default: ").strip()

    if choice == "2":
        run_custom_scenario()
    elif choice == "3":
        run_high_chaos_scenario()
    elif choice == "4":
        run_ideal_scenario()
    else:
        run_descent_scenario()

    print("\n✓ Simulation complete!")
