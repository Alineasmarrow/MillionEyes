"""
Command Parser for Narrative Coherence Engine

Provides dev commands:
- /show_run - Display current run state
- /compose - Generate epilogue preview
- /save_run - Save run to log file
- /show_cards_played - Display cards played this run
- /summon_set <act> - Show cards for an act (if card_sets.json exists)
- /edit_cards - Show all cards for editing (if card_sets.json exists)
"""

import json
import os
from epilogue_composer import compose_epilogue
from run_logger import log_run, derive_ending_key


# ---------------------------------------------------------
#  COMMAND HANDLERS
# ---------------------------------------------------------

def handle_show_run(args, engine_state):
    """Display current run state summary"""
    run_state = engine_state.get('run_state', {})

    ending = derive_ending_key(run_state)

    summary = {
        "ending": ending,
        "characters": {
            name: {
                "fate": "DEAD" if c.get('dead') else "DISSOLVED" if c.get('dissolved') else "SURVIVED",
                "coherence": c.get('coherence', 0.0)
            }
            for name, c in run_state.get('characters', {}).items()
        },
        "flags": run_state.get('flags', {}),
        "metrics": run_state.get('metrics', {}),
        "cards_played_count": len(run_state.get('cards_played', []))
    }

    return json.dumps(summary, indent=2)


def handle_compose(args, engine_state):
    """Generate epilogue preview without saving"""
    run_state = engine_state.get('run_state', {})
    epilogue = compose_epilogue(run_state)
    return epilogue


def handle_save_run(args, engine_state):
    """Save complete run to log file"""
    run_state = engine_state.get('run_state', {})
    epilogue = compose_epilogue(run_state)
    result = log_run(run_state, epilogue)
    return "Run saved to logs/\n\n" + result


def handle_show_cards_played(args, engine_state):
    """Display chronological list of cards played"""
    run_state = engine_state.get('run_state', {})
    cards = run_state.get('cards_played', [])

    if not cards:
        return "No cards tracked this run."

    lines = ["=== Cards Played ==="]
    for card in cards:
        act = card.get('act', '?')
        card_id = card.get('id', 'unknown')
        choice = card.get('choice', 'none')
        burned = card.get('burned', False)

        lines.append(f"[{act}] {card_id} | {choice} | burned={burned}")

    return '\n'.join(lines)


def handle_summon_set(args, engine_state):
    """Show cards for a specific act (requires card_sets.json)"""
    if not args:
        return "Usage: /summon_set <act_number>"

    act = args[0]
    card_sets = engine_state.get('card_sets', {})

    if not card_sets:
        return "No card_sets.json found. Card tracking not enabled."

    if act not in card_sets:
        return f"No cards found for Act {act}"

    return json.dumps({"act": act, "cards": card_sets[act]}, indent=2)


def handle_edit_cards(args, engine_state):
    """Display all card sets for editing (requires card_sets.json)"""
    card_sets = engine_state.get('card_sets', {})

    if not card_sets:
        return "No card_sets.json found. Card tracking not enabled."

    return json.dumps(card_sets, indent=2)


def handle_help(args, engine_state):
    """Display available commands"""
    help_text = """
Available Commands:

/show_run
  Display current run state (ending, fates, flags, metrics)

/compose
  Generate epilogue preview without saving

/save_run
  Save complete run log to logs/ directory

/show_cards_played
  Display chronological list of cards played this run

/summon_set <act>
  Show cards for specific act (requires card_sets.json)

/edit_cards
  Show all cards for editing (requires card_sets.json)

/help
  Show this help message
"""
    return help_text.strip()


# ---------------------------------------------------------
#  COMMAND TABLE
# ---------------------------------------------------------

COMMANDS = {
    "show_run": handle_show_run,
    "compose": handle_compose,
    "save_run": handle_save_run,
    "show_cards_played": handle_show_cards_played,
    "summon_set": handle_summon_set,
    "edit_cards": handle_edit_cards,
    "help": handle_help,
}


# ---------------------------------------------------------
#  MAIN PARSER
# ---------------------------------------------------------

def parse_command(input_str, engine_state):
    """
    Parse and execute a command

    Args:
        input_str: Command string starting with /
        engine_state: Dictionary with run_state, card_sets (optional)

    Returns:
        Command output as string or JSON
    """
    if not input_str.strip():
        return "Empty command. Type /help for available commands."

    if not input_str.startswith("/"):
        return "Invalid command: commands must start with '/'\nType /help for available commands."

    parts = input_str.strip().split()
    cmd = parts[0][1:]  # Remove "/"
    args = parts[1:]

    if cmd not in COMMANDS:
        return f"Unknown command: {cmd}\nType /help for available commands."

    try:
        return COMMANDS[cmd](args, engine_state)
    except Exception as e:
        return f"Error executing command: {str(e)}"


# ---------------------------------------------------------
#  CONVENIENCE FUNCTION
# ---------------------------------------------------------

def execute_command(command, run_state, card_sets=None):
    """
    Execute a command with minimal setup

    Args:
        command: Command string (e.g., "/show_run")
        run_state: Current run state dictionary
        card_sets: Optional card sets dictionary

    Returns:
        Command output
    """
    engine_state = {
        'run_state': run_state,
        'card_sets': card_sets or {}
    }

    return parse_command(command, engine_state)
