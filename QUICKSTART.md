# Quick Start Guide

## Running Your First Scenario

### Option 1: Use Pre-made Scenarios

```bash
python example_scenario.py
```

Select from:
1. **The Descent** - Yuul in crisis, recommended for first run
2. **Custom** - Moderate conditions
3. **Edge of Collapse** - High stakes
4. **The Golden Age** - Ideal start

### Option 2: Create Your Own (Simple)

Create a file called `my_scenario.py`:

```python
from simulation import NarrativeSimulation

# Create simulation
sim = NarrativeSimulation("My First Story")

# Add characters (name, c_self from 0-10)
sim.add_character("Alice", c_self=7.0)
sim.add_character("Bob", c_self=6.0)
sim.add_character("Carol", c_self=8.0)

# Add relationships (char_a, char_b, c_dyad from 0-10)
sim.add_relationship("Alice", "Bob", c_dyad=7.5)
sim.add_relationship("Alice", "Carol", c_dyad=6.0)
sim.add_relationship("Bob", "Carol", c_dyad=5.0)

# Set starting chaos (0-20)
sim.chaos = 5.0

# Run the simulation (10 rounds)
sim.run_scenario(num_rounds=10)
```

Run it:
```bash
python my_scenario.py
```

## Understanding the Output

### Character States
- **Transcendent** (9+): Sacred territory
- **Stable** (7-9): Functioning well
- **Functional** (5-7): Managing but stressed
- **Strained** (4-5): Approaching crisis
- **Crisis** (3-4): Breaking point near
- **Dissolving** (1-3): Identity fragmenting
- **Gone** (<1): Ceased to exist

### Relationship States
- **MYTHIC/SACRED** (9-10): Unbreakable bonds
- **Strong** (7-9): Deep trust
- **Functional** (5-7): Working relationship
- **STRAINED** (3-5): Tension, risk of rupture
- **RUPTURE ZONE** (1-3): Barely holding
- **SEVERED** (0): Destroyed

### Chaos
- **0-10**: Stable
- **10-15**: Rising tension
- **16-19**: Warning zone
- **20+**: CoR manifests

### Symbols in Output
- ✓ Good/Stable
- ~ Neutral/Functional
- ⚠ Warning/Strained
- 🔥 Critical/Danger
- ✨ Transcendent/Sacred
- ↑/↓/→ Rising/Falling/Stable

## Tips for Good Scenarios

### Starting Values

**For balanced scenarios:**
- Characters: C_self around 6-7
- Relationships: C_dyad around 6-8
- Chaos: 5-10

**For crisis scenarios:**
- Characters: C_self around 3-5
- Relationships: C_dyad around 4-6
- Chaos: 12-16

**For ideal scenarios:**
- Characters: C_self around 7-9
- Relationships: C_dyad around 7-9
- Chaos: 2-5

### Number of Rounds

- **5-8 rounds**: Quick story arc
- **10-15 rounds**: Full narrative
- **20+ rounds**: Epic saga

### The Witch Trine

If you use characters named **Maeve**, **Yuul**, and **Rielle**, the system will automatically track their collective bond strength (Witch Trine). Make sure to add all three dyadic relationships between them.

## Viewing Event Cards

See all 20 event cards:
```bash
python list_events.py
```

See cards sorted by chaos impact:
```bash
python list_events.py --chaos
```

## Advanced: Running Specific Events

```python
from simulation import NarrativeSimulation
from events import create_event_deck

sim = NarrativeSimulation("Controlled Story")

# ... add characters and relationships ...

# Get the deck
deck = create_event_deck()

# Run specific events by ID (0-19)
sim.run_round(deck[0])   # Card 1: Yuul Has a Vision
sim.run_round(deck[13])  # Card 14: Bonfire Night
sim.run_round(deck[19])  # Card 20: Grace Moment

# Print final state
sim.print_final_state()
```

## Saving Your Results

The simulation automatically saves logs when using `run_scenario()`. You can also manually save:

```python
sim.save_log("my_story_log.txt")
```

## Next Steps

1. Run `python example_scenario.py` to see the system in action
2. Read `README.md` for full documentation
3. Check `list_events.py` to see all available events
4. Create your own scenarios!

## Troubleshooting

**"Character not found" error:**
- Make sure you've added the character before referencing them in relationships

**"Relationship not found" error:**
- Make sure you've added the relationship with `sim.add_relationship()`

**Events don't make sense for my characters:**
- The default events are designed for Yuul, Maeve, Kit, and Rielle
- You can still run them with other characters, but narratives may not fit
- For custom characters, consider creating custom events (see README.md)

## Example: Minimal Working Code

```python
from simulation import NarrativeSimulation

sim = NarrativeSimulation("Test")
sim.add_character("A", c_self=7.0)
sim.add_character("B", c_self=6.0)
sim.add_relationship("A", "B", c_dyad=7.0)
sim.chaos = 5.0
sim.run_scenario(num_rounds=5)
```

That's it! Have fun exploring narrative coherence dynamics!
