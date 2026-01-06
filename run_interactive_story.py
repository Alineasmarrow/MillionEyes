#!/usr/bin/env python3
"""
Interactive Story Mode

Run a full narrative simulation with choice moments on unique cards.
When a unique card triggers, you'll be presented with 3 archetype choices:
- WITNESS: Clarity and truth-telling
- TRICKSTER: Chaos and disruption
- DEVOURER: Sacrifice and burden-bearing

Your choices shape the story and are tracked in the final archetype summary.
"""

from simulation import NarrativeSimulation


def run_interactive_story():
    """Run an interactive story with choice moments"""
    print("\n" + "=" * 80)
    print("🎭 NARRATIVE COHERENCE ENGINE - INTERACTIVE MODE")
    print("=" * 80)
    print()
    print("You are witnessing the story of House 11.")
    print("When unique moments arise, you will choose how to respond.")
    print()
    print("Your choices shape the narrative through three archetypes:")
    print("  • WITNESS: Speak truth, bring clarity")
    print("  • TRICKSTER: Disrupt, create space through chaos")
    print("  • DEVOURER: Sacrifice, bear burdens for others")
    print()
    print("=" * 80)
    input("\nPress ENTER to begin...")

    # Create interactive simulation with act system
    sim = NarrativeSimulation("The Descent - Interactive", interactive_mode=True, use_act_system=True)

    # Setup: The Descent scenario
    print("\n📖 Scenario: The Descent")
    print("Yuul's prophetic coherence is failing. Can H11 survive the spiral?")
    print("\nThe story unfolds in two acts:")
    print("  ACT I: Misleading Calm (rounds 1-10)")
    print("  ACT II: Escalation (rounds 11-25)")
    print()

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

    print(f"Starting Chaos: {sim.chaos:.1f}/20.0")
    print()
    input("Press ENTER to continue...")

    # Run simulation (25 rounds covers both Act I and Act II)
    num_rounds = 25

    print(f"\n🎲 Running up to {num_rounds} rounds...")
    print("You will be prompted to make choices when unique events occur.\n")

    for i in range(num_rounds):
        sim.run_round()

        # Check for end conditions
        if sim.chaos >= 20:
            print("\n🔥 CHAOS THRESHOLD REACHED - CoR manifests!")
            print("The story spirals beyond control...\n")
            break

        # Pause between rounds for readability
        if i < num_rounds - 1:
            input("\nPress ENTER for next round...")

    # Display final state
    sim.print_final_state()


if __name__ == "__main__":
    try:
        run_interactive_story()
    except KeyboardInterrupt:
        print("\n\n⚠️  Story interrupted by user")
        print("The narrative remains unfinished...")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
