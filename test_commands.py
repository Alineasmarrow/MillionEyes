"""
Test Command Parser with Example Run State

Demonstrates all available commands
"""

from command_parser import execute_command

# Use one of our test scenarios
from test_epilogues import run_state_redchurch, run_state_miracle

print("=" * 80)
print("COMMAND PARSER DEMO")
print("=" * 80)
print()

# Use the Redchurch scenario for testing
run_state = run_state_redchurch

print("Command: /help")
print("-" * 80)
result = execute_command("/help", run_state)
print(result)
print()
print()

print("Command: /show_run")
print("-" * 80)
result = execute_command("/show_run", run_state)
print(result)
print()
print()

print("Command: /show_cards_played")
print("-" * 80)
result = execute_command("/show_cards_played", run_state)
print(result)
print()
print()

print("Command: /compose")
print("-" * 80)
print("(Generating epilogue preview...)")
result = execute_command("/compose", run_state)
print(result[:500] + "...")  # Show first 500 chars
print()
print()

print("Command: /save_run")
print("-" * 80)
print("(This will save to logs/ directory)")
result = execute_command("/save_run", run_state)
print("Run saved successfully!")
print()
print()

print("=" * 80)
print("All commands tested successfully!")
print("Check the logs/ directory for the saved run file.")
print("=" * 80)
