"""
Run Logger for Narrative Coherence Engine

Saves complete run logs with:
- Ending type
- Character fates
- Flags
- Metrics
- Cards played (if tracked)
- Generated epilogue
"""

import json
import os
import datetime


LOG_DIR = "logs"


def ensure_log_dir():
    """Create logs directory if it doesn't exist"""
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)


def derive_ending_key(run_state):
    """
    Determine which ending was selected based on run_state

    Matches the logic in epilogue_composer.py
    """
    end_state = run_state.get('end_state', {})
    flags = run_state.get('flags', {})

    if end_state.get('total_party_kill', False):
        return 'tpk_redchurch'
    if flags.get('cor_manifestation', False):
        return 'cor_manifestation'
    if flags.get('dce_pressure_high', False) and flags.get('h11_team_compromised', False):
        return 'dce_win'
    if end_state.get('kit_dead', False) and end_state.get('yuul_dead', False):
        return 'redchurch_canon'
    if end_state.get('kit_dissolved', False) or end_state.get('yuul_dissolved', False):
        return 'disappearance'
    if end_state.get('everyone_survived', False):
        return 'miracle_run'

    return 'redchurch_canon'


def format_cards(cards):
    """Format cards_played list into readable lines"""
    lines = []
    for card in cards:
        act = card.get('act', '?')
        card_id = card.get('id', 'unknown')
        choice = card.get('choice', 'none')
        burned = card.get('burned', False)
        timestamp = card.get('timestamp', '')

        line = f"[{act}] {card_id} | choice={choice} | burned={burned} | time={timestamp}"
        lines.append(line)
    return '\n'.join(lines)


def log_run(run_state, epilogue_text):
    """
    Save complete run log to timestamped file

    Args:
        run_state: Dictionary with characters, flags, metrics, end_state, cards_played
        epilogue_text: Full generated epilogue text

    Returns:
        String of the full log text
    """
    ensure_log_dir()
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    ending_key = derive_ending_key(run_state)

    lines = []
    lines.append("===== HORIZON-11 RUN LOG =====")
    lines.append(f"Timestamp: {timestamp}")
    lines.append("")

    # ENDING
    lines.append("=== Ending Selection ===")
    lines.append(f"Ending: {ending_key}")
    lines.append("")

    # CHARACTER FATES
    lines.append("=== Character Fates ===")
    for name, char_data in run_state.get('characters', {}).items():
        if char_data.get('dead', False):
            fate = "DEAD"
        elif char_data.get('dissolved', False):
            fate = "DISSOLVED"
        else:
            fate = "SURVIVED"

        coherence = char_data.get('coherence', 0.0)
        lines.append(f"- {name.title()}: {fate} (C={coherence:.1f})")
    lines.append("")

    # FLAGS
    lines.append("=== Flags ===")
    for flag, value in run_state.get('flags', {}).items():
        lines.append(f"- {flag}: {value}")
    lines.append("")

    # METRICS
    lines.append("=== Metrics ===")
    for metric, value in run_state.get('metrics', {}).items():
        lines.append(f"{metric}: {value}")
    lines.append("")

    # CARDS PLAYED
    lines.append("=== Cards Played ===")
    cards = run_state.get('cards_played', [])
    if cards:
        lines.append(format_cards(cards))
    else:
        lines.append("(none tracked)")
    lines.append("")

    # EPILOGUE
    lines.append("=== Generated Epilogue ===")
    lines.append(epilogue_text)

    final_text = '\n'.join(lines)

    # Save to file
    filename = f"run_{timestamp}.txt"
    filepath = os.path.join(LOG_DIR, filename)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(final_text)

    print(f"✓ Run saved to {filepath}")

    return final_text
