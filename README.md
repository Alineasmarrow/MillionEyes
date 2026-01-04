# Narrative Coherence Engine

A Python-based simulation engine for running story scenarios based on coherence theory. This system models character coherence (C_self), relationship coherence (C_dyad), chaos accumulation, and narrative events.

## Overview

The Narrative Coherence Engine simulates the dynamics of characters in a story world where:

- **Characters** have coherence with themselves (C_self, 0-10 scale)
- **Relationships** between characters have coherence values (C_dyad, 0-10 scale)
- **Chaos** accumulates through events and threatens the narrative fabric
- **Events** create dynamic changes based on conditional logic

## Quick Start

### Run a pre-made scenario:

```bash
python example_scenario.py
```

This will prompt you to choose from several scenarios:
1. **The Descent** - Yuul in crisis, group strained
2. **Custom** - Moderate starting conditions
3. **Edge of Collapse** - High chaos, everyone struggling
4. **The Golden Age** - Ideal starting conditions

### Create your own scenario:

```python
from simulation import NarrativeSimulation

# Create simulation
sim = NarrativeSimulation("My Story")

# Add characters with C_self values (0-10)
sim.add_character("Alice", c_self=7.0)
sim.add_character("Bob", c_self=6.5)

# Add relationships with C_dyad values (0-10)
sim.add_relationship("Alice", "Bob", c_dyad=7.5)

# Set initial chaos
sim.chaos = 5.0

# Run the scenario
sim.run_scenario(num_rounds=10)

# Save the log
sim.save_log("my_scenario.txt")
```

## Core Concepts

### Character States (C_self thresholds)

| C_self Range | State | Meaning |
|-------------|-------|---------|
| >= 9.0 | Transcendent | Approaching sacred/mythic territory |
| >= 7.0 | Stable | Functional, grounded |
| >= 5.0 | Functional | Managing but stressed |
| >= 4.0 | Strained | Close to crisis |
| >= 3.0 | Crisis | Breaking point approaching |
| >= 1.0 | Dissolving | Identity fragmenting |
| < 1.0 | Gone | Ceased to exist as individual |

### Relationship States (C_dyad thresholds)

| C_dyad Range | State | Meaning |
|-------------|-------|---------|
| >= 10.0 | MYTHIC | Beyond mortal bonds (rare) |
| >= 9.0 | SACRED | Unbreakable, cosmic significance |
| >= 7.0 | Strong | Deep trust, stable |
| >= 5.0 | Functional | Working relationship |
| >= 3.0 | STRAINED | Tension, risk of rupture |
| >= 1.0 | RUPTURE ZONE | Barely holding |
| == 0.0 | SEVERED | Relationship destroyed |

### Chaos System

- **Chaos Threshold**: 20.0 (CoR manifestation point)
- **Warning Threshold**: 16.0 (80% of max)
- Events add or subtract chaos based on their effects
- High chaos indicates narrative instability

### ⚡ Sacred Dyad Conservation Law

When a relationship reaches **SACRED status (C_dyad >= 9.0)**, the characters become metaphysically coupled:

**The Law:**
- Changes to one character **echo** in their sacred partner (default: 30% coupling strength)
- If Character A loses 2.0 C_self, Character B loses 0.6 C_self (30% coupling)
- This applies to both positive and negative changes

**Chaos Amplification:**
- Sacred bonds **shake reality** when they waver
- Each sacred dyad change adds: `|delta| × 0.5` chaos
- Multiple sacred bonds multiply the effect

**Catastrophic Collapse:**
- If a sacred partner falls to C_self ≤ 0, their partner suffers:
  - **Grief Rupture**: -2.0 C_self (immediate)
  - **Reality Buckles**: +4.0 chaos
  - This can trigger cascading failures

**Why This Matters:**
- Sacred bonds are **liabilities under pressure**, not just strengths
- They magnify transformations (both rise and fall)
- High chaos makes sacred dyads **volatile**
- Creates prophecy-like emergent narratives: lovers destroy each other, sisters break reality, promises become tragic

**Visual Indicators:**
- Sacred dyads marked with ⚡ symbol
- Sacred echoes displayed in event logs
- Dedicated section in final state output

**Example:**
```
Kit-Yuul: 9.5 [SACRED] → ⚡ SACRED
  ↓ Kit: C_self -2.0 → 6.0 [Functional]
     → overextends
     ⚡ Sacred echo: Yuul ↓ -0.6 → 5.4
     ⚡ Sacred bond shakes reality: +1.0 chaos
```

## Event Cards

The engine includes 20 narrative event cards organized into categories:

### Yuul Vulnerability (Cards 1-4)
- Card 1: Yuul Has a Vision - Horror
- Card 2: Prophetic Isolation
- Card 3: Yuul Speaks in Reversals
- Card 4: The Mirror Incident

### Kit's Hidden Feelings (Cards 5-7)
- Card 5: Kit Tries to Ground Yuul
- Card 6: Someone Notices
- Card 7: Kit Overextends

### Trine Fracture (Cards 8-10)
- Card 8: Trine Ritual Required
- Card 9: Rielle Questions Maeve's Choice
- Card 10: Yuul's Last Prophecy

### External Pressure (Cards 11-13)
- Card 11: Mission Goes Wrong
- Card 12: DCE Investigation
- Card 13: The Thing They've Been Avoiding

### Potential Salvation (Cards 14-16)
- Card 14: Bonfire Night
- Card 15: Kit Confesses (Not to Yuul)
- Card 16: Maeve Reaches Out to Yuul

### Wild Cards (Cards 17-20)
- Card 17: Yuul Warns About Redchurch
- Card 18: Kit Makes a Promise
- Card 19: Rielle's Impulse
- Card 20: Grace Moment

Each event has:
- **Base chaos effect**: How much chaos it adds or removes
- **Character effects**: Changes to C_self values
- **Relationship effects**: Changes to C_dyad values
- **Conditional logic**: Effects that depend on current state

## File Structure

```
MillionEyes/
├── constants.py           # System constants and thresholds
├── models.py             # Character and Relationship classes
├── events.py             # Event card definitions and logic
├── simulation.py         # Main simulation engine
├── example_scenario.py   # Pre-made scenarios
└── README.md            # This file
```

## Advanced Usage

### Manual Event Selection

```python
from events import create_event_deck

sim = NarrativeSimulation("Controlled Story")
# ... add characters and relationships ...

# Get the event deck
deck = create_event_deck()

# Run specific events by ID
sim.run_round(deck[0])  # Card 1: Yuul Has a Vision
sim.run_round(deck[4])  # Card 5: Kit Tries to Ground Yuul
```

### Track Character Changes

```python
# After running simulation, check character history
yuul = sim.get_character("Yuul")
for change in yuul.history:
    print(f"{change['reason']}: {change['old_value']:.1f} → {change['new_value']:.1f}")
```

### Witch Trine Health

```python
# Check the health of the Witch Trine (Maeve, Yuul, Rielle)
trine_health = sim.calculate_witch_trine_health()
print(f"Trine Health: {trine_health:.1f}")

# >= 8.0 = Strong
# >= 6.0 = Functional
# < 6.0 = Failing
```

### Customizing Sacred Dyad Coupling

```python
# Create a relationship with custom coupling strength
# Default: 0.3 (30%)
# Higher values = more brutal fate coupling

sim.add_relationship("Alice", "Bob", c_dyad=9.5)
dyad = sim.get_dyad("Alice", "Bob")

# Set custom coupling strength
dyad.coupling_strength = 0.5  # 50% coupling (more intense)
# or
dyad.coupling_strength = 0.8  # 80% coupling (tragic)

# Now when Alice changes by -2.0:
# - With 30% coupling: Bob changes by -0.6
# - With 50% coupling: Bob changes by -1.0
# - With 80% coupling: Bob changes by -1.6
```

### Custom Events

You can create custom events by defining a function:

```python
def my_custom_event(sim):
    log = []
    chaos_change = 1

    # Apply effects
    change = sim.modify_character_c_self("Alice", -1, "my event effect")
    log.append(change)

    return {"chaos": chaos_change, "log": log}

from events import Event
custom = Event(99, "My Event", "custom", "Description", 1, my_custom_event)

# Run it
sim.run_round(custom)
```

## Output Interpretation

When running a scenario, you'll see:

- **Initial State**: Starting C_self and C_dyad values for all characters/relationships
- **Round-by-round events**: What happened, who was affected, how values changed
- **Final State**: End state with warnings for critical situations
- **Saved logs**: Detailed text file of the entire simulation

### Symbols

- ✓ Stable/Positive state
- ~ Functional/Neutral state
- ⚠ Warning/Strained state
- 🔥 Critical/Danger state
- ✨ Transcendent/Sacred state
- ↑ Increasing
- ↓ Decreasing
- → Stable

## Tips for Running Scenarios

1. **Start with moderate values**: C_self around 6-7, C_dyad around 6-8
2. **Set appropriate chaos**: 5-10 for normal scenarios, higher for crisis scenarios
3. **Run enough rounds**: 10-15 rounds to see interesting dynamics
4. **Save your logs**: Use `sim.save_log()` to keep records
5. **Watch for cascades**: When characters drop below 3.0 C_self, things can spiral quickly

## The Witch Trine

The Witch Trine is a special mechanic involving three characters:
- Maeve
- Yuul
- Rielle

Their collective bond strength affects certain events (especially Card 8: Trine Ritual Required). The Trine health is calculated as the average of their three dyadic relationships.

## License

This is a narrative simulation tool for creative and analytical purposes.

## Credits

Based on coherence theory applied to narrative dynamics.
