# Command System & Run Logger

The Narrative Coherence Engine now includes a command parser and run logger for debugging and tracking gameplay.

## Quick Start

```python
from command_parser import execute_command

# Execute commands on a run_state
result = execute_command("/show_run", run_state)
print(result)
```

## Available Commands

### `/help`
Display all available commands and their usage.

### `/show_run`
Display current run state summary in JSON format:
- Ending type
- Character fates (SURVIVED/DEAD/DISSOLVED)
- Character coherence values
- All flags
- All metrics

```python
execute_command("/show_run", run_state)
```

### `/compose`
Generate epilogue preview without saving to file. Shows the full Maeve-narrated epilogue based on current run state.

```python
epilogue = execute_command("/compose", run_state)
print(epilogue)
```

### `/save_run`
Save complete run log to `logs/` directory with timestamp. Includes:
- Ending selection
- Character fates
- Flags
- Metrics
- Cards played (if tracked)
- Full generated epilogue

```python
execute_command("/save_run", run_state)
# Creates: logs/run_2026-01-21_10-09-48.txt
```

### `/show_cards_played`
Display chronological list of cards played during run (requires `cards_played` in run_state).

```python
execute_command("/show_cards_played", run_state)
```

### `/summon_set <act>`
Show all cards for a specific act (requires `card_sets.json`).

```python
execute_command("/summon_set 2", run_state, card_sets)
```

### `/edit_cards`
Display all card sets for editing (requires `card_sets.json`).

```python
execute_command("/edit_cards", run_state, card_sets)
```

## Run State Schema

The command system expects a `run_state` dictionary with this structure:

```python
run_state = {
    "characters": {
        "maeve": {"dead": False, "dissolved": False, "coherence": 7.5},
        "yuul": {"dead": False, "dissolved": False, "coherence": 6.5},
        # ... other characters
    },
    "flags": {
        "sacred_with_yuul": True,
        "rielle_recursion": False,
        "maeve_learned_list_hunger": False,
        # ... other flags
    },
    "metrics": {
        "chaos_total": 17.0,
        "turbulence": 10.5,
        "pressure": 6.5,
        "maeve_coherence": 7.5
    },
    "end_state": {
        "total_party_kill": False,
        "everyone_survived": True,
        "kit_dead": False,
        "yuul_dead": False,
        "kit_dissolved": False,
        "yuul_dissolved": False
    },
    "cards_played": [  # Optional
        {
            "id": "act1_case_opening",
            "act": 1,
            "choice": "witness",
            "burned": False,
            "timestamp": "2026-01-21T10:00:00"
        }
    ]
}
```

## Card Tracking (Optional)

To enable card tracking commands (`/summon_set`, `/edit_cards`), create a `card_sets.json`:

```json
{
  "1": [
    {
      "id": "act1_case_opening",
      "type": "case",
      "text": "...",
      "burnable": false
    }
  ],
  "2": [...],
  "3": [...]
}
```

Then pass it to the command system:

```python
from command_parser import execute_command

result = execute_command("/summon_set 2", run_state, card_sets)
```

## Log Files

Saved runs are stored in `logs/` directory with format:
```
logs/run_2026-01-21_10-09-48.txt
```

Each log contains:
- Timestamp
- Ending type
- Character fates and coherence
- All flags
- All metrics
- Cards played
- Full generated epilogue in Maeve's voice

## Integration Example

```python
from command_parser import parse_command
from epilogue_composer import compose_epilogue

# Setup engine state
engine_state = {
    'run_state': my_run_state,
    'card_sets': {}  # Optional
}

# Execute commands
result = parse_command("/show_run", engine_state)
print(result)

epilogue = parse_command("/compose", engine_state)
print(epilogue)

# Save run
parse_command("/save_run", engine_state)
```

## Testing

Run the test suite:
```bash
python3 test_commands.py
```

This will demonstrate all commands and save a test run to `logs/`.
