#!/usr/bin/env python3
"""
Test Final Words System
"""

from final_words import get_final_words, get_highest_dyad_partner, display_final_words


class MockDyad:
    """Mock dyad for testing"""
    def __init__(self, char_a, char_b, c_dyad):
        self.char_a = char_a
        self.char_b = char_b
        self.c_dyad = c_dyad


def test_highest_dyad_partner():
    """Test finding highest dyad partner"""
    print("Test 1: Finding highest dyad partner")
    print("="*60)

    # Create mock dyads for Kit
    dyads = [
        MockDyad("Kit", "Maeve", 6.5),
        MockDyad("Kit", "Yuul", 9.0),  # Highest - sacred bond
        MockDyad("Kit", "Rielle", 6.0),
    ]

    partner, value = get_highest_dyad_partner("Kit", dyads)
    print(f"Kit's highest bond: {partner} (C={value})")
    assert partner == "Yuul", f"Expected Yuul, got {partner}"
    assert value == 9.0, f"Expected 9.0, got {value}"
    print("✓ Correctly identified Yuul as highest bond\n")


def test_final_words_standard():
    """Test standard final words"""
    print("Test 2: Standard final words")
    print("="*60)

    # Kit to Yuul with normal bond
    words = get_final_words("Kit", "Yuul", 7.0)
    print(f"Kit to Yuul (C=7.0):")
    print(f"  {words}")
    assert "I see you" in words, "Should use standard Kit->Yuul words"
    print("✓ Standard final words working\n")


def test_final_words_sacred():
    """Test sacred bond final words"""
    print("Test 3: Sacred bond final words (C≥9)")
    print("="*60)

    # Kit to Yuul with sacred bond
    words = get_final_words("Kit", "Yuul", 9.5)
    print(f"Kit to Yuul (C=9.5 - Sacred):")
    print(f"  {words}")
    assert "find you" in words and "after" in words, "Should use sacred bond words"
    print("✓ Sacred bond final words working\n")


def test_final_words_alone():
    """Test dying alone"""
    print("Test 4: Dying alone")
    print("="*60)

    # Rielle dying alone
    words = get_final_words("Rielle", None, 0)
    print(f"Rielle dying alone:")
    print(f"  {words}")
    assert "burn alone" in words, "Should use Rielle's alone words"
    print("✓ Alone final words working\n")


def test_full_display():
    """Test full display sequence"""
    print("Test 5: Full display sequence")
    print("="*60)

    print("\nScenario: Kit dies, looking to Yuul (Sacred bond C=9.0)")
    display_final_words("Kit", "Yuul", 9.0)
    print("\n✓ Full display sequence working\n")


def test_all_characters():
    """Test final words for all characters"""
    print("Test 6: All character pairings")
    print("="*60)

    pairings = [
        ("Maeve", "Yuul", 7.0),
        ("Maeve", "Rielle", 8.0),
        ("Maeve", "Farris", 7.0),
        ("Kit", "Yuul", 7.0),
        ("Yuul", "Kit", 7.0),
        ("Rielle", "Maeve", 8.0),
        ("Daniel", "Maeve", 6.0),
        ("Farris", "Maeve", 7.0),
    ]

    for char, partner, value in pairings:
        words = get_final_words(char, partner, value)
        print(f"  {char} → {partner}: {words[:40]}...")

    print("\n✓ All character pairings working\n")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("FINAL WORDS SYSTEM - TEST SUITE")
    print("="*60 + "\n")

    try:
        test_highest_dyad_partner()
        test_final_words_standard()
        test_final_words_sacred()
        test_final_words_alone()
        test_full_display()
        test_all_characters()

        print("="*60)
        print("✅ ALL TESTS PASSED")
        print("="*60)

    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
