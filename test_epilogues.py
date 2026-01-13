"""
Test Epilogue System with 4 Canonical Scenarios

Tests:
1. Canon Redchurch (Yuul + Kit dead)
2. Disappearance (Yuul + Kit dissolved)
3. CoR Manifestation (Maeve last survivor)
4. Miracle Run (everyone lives)
"""

from epilogue_composer import compose_epilogue


# ============================================================================
# TEST 1: CANON REDCHURCH
# ============================================================================

run_state_redchurch = {
    "characters": {
        "maeve": {"dead": False, "dissolved": False, "coherence": 4.5},
        "yuul": {"dead": True, "dissolved": False, "coherence": 0.0},
        "kit": {"dead": True, "dissolved": False, "coherence": 0.0},
        "rielle": {"dead": False, "dissolved": False, "coherence": 5.0},
        "daniel": {"dead": False, "dissolved": False, "coherence": 4.0},
        "farris": {"dead": False, "dissolved": False, "coherence": 6.0}
    },
    "flags": {
        "sacred_with_yuul": True,
        "rielle_recursion": False,
        "farris_death_echo": False,
        "maeve_learned_list_hunger": True,
        "cor_manifestation": False,
        "dce_pressure_high": False,
        "h11_team_compromised": True,
        "miracle_ending_possible": False,
        "dominant_archetype": "witness"
    },
    "metrics": {
        "chaos_total": 19.5,
        "turbulence": 10.8,
        "pressure": 8.7,
        "maeve_coherence": 4.5
    },
    "end_state": {
        "total_party_kill": False,
        "everyone_survived": False,
        "kit_dead": True,
        "yuul_dead": True,
        "kit_dissolved": False,
        "yuul_dissolved": False
    }
}


# ============================================================================
# TEST 2: DISAPPEARANCE
# ============================================================================

run_state_disappearance = {
    "characters": {
        "maeve": {"dead": False, "dissolved": False, "coherence": 5.0},
        "yuul": {"dead": False, "dissolved": True, "coherence": 0.0},
        "kit": {"dead": False, "dissolved": True, "coherence": 0.0},
        "rielle": {"dead": False, "dissolved": False, "coherence": 5.5},
        "daniel": {"dead": False, "dissolved": False, "coherence": 4.5},
        "farris": {"dead": False, "dissolved": False, "coherence": 6.5}
    },
    "flags": {
        "sacred_with_yuul": True,
        "rielle_recursion": False,
        "farris_death_echo": False,
        "maeve_learned_list_hunger": False,
        "cor_manifestation": False,
        "dce_pressure_high": False,
        "h11_team_compromised": True,
        "miracle_ending_possible": False,
        "dominant_archetype": "witness"
    },
    "metrics": {
        "chaos_total": 18.0,
        "turbulence": 11.2,
        "pressure": 6.8,
        "maeve_coherence": 5.0
    },
    "end_state": {
        "total_party_kill": False,
        "everyone_survived": False,
        "kit_dead": False,
        "yuul_dead": False,
        "kit_dissolved": True,
        "yuul_dissolved": True
    }
}


# ============================================================================
# TEST 3: CoR MANIFESTATION
# ============================================================================

run_state_cor = {
    "characters": {
        "maeve": {"dead": False, "dissolved": False, "coherence": 3.0},
        "yuul": {"dead": False, "dissolved": True, "coherence": 0.0},
        "kit": {"dead": True, "dissolved": False, "coherence": 0.0},
        "rielle": {"dead": False, "dissolved": True, "coherence": 0.0},
        "daniel": {"dead": True, "dissolved": False, "coherence": 0.0},
        "farris": {"dead": True, "dissolved": False, "coherence": 0.0}
    },
    "flags": {
        "sacred_with_yuul": False,
        "rielle_recursion": True,
        "farris_death_echo": False,
        "maeve_learned_list_hunger": True,
        "cor_manifestation": True,
        "dce_pressure_high": False,
        "h11_team_compromised": True,
        "miracle_ending_possible": False,
        "dominant_archetype": "devourer"
    },
    "metrics": {
        "chaos_total": 22.5,
        "turbulence": 7.0,
        "pressure": 15.5,
        "maeve_coherence": 3.0
    },
    "end_state": {
        "total_party_kill": False,
        "everyone_survived": False,
        "kit_dead": True,
        "yuul_dead": False,
        "kit_dissolved": False,
        "yuul_dissolved": True
    }
}


# ============================================================================
# TEST 4: MIRACLE RUN
# ============================================================================

run_state_miracle = {
    "characters": {
        "maeve": {"dead": False, "dissolved": False, "coherence": 7.5},
        "yuul": {"dead": False, "dissolved": False, "coherence": 6.5},
        "kit": {"dead": False, "dissolved": False, "coherence": 7.0},
        "rielle": {"dead": False, "dissolved": False, "coherence": 6.5},
        "daniel": {"dead": False, "dissolved": False, "coherence": 5.5},
        "farris": {"dead": False, "dissolved": False, "coherence": 8.0}
    },
    "flags": {
        "sacred_with_yuul": True,
        "rielle_recursion": False,
        "farris_death_echo": False,
        "maeve_learned_list_hunger": False,
        "cor_manifestation": False,
        "dce_pressure_high": False,
        "h11_team_compromised": False,
        "miracle_ending_possible": True,
        "dominant_archetype": "witness"
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
    }
}


# ============================================================================
# RUN TESTS
# ============================================================================

if __name__ == '__main__':
    scenarios = [
        ("CANON REDCHURCH", run_state_redchurch),
        ("DISAPPEARANCE", run_state_disappearance),
        ("CoR MANIFESTATION", run_state_cor),
        ("MIRACLE RUN", run_state_miracle)
    ]

    for name, run_state in scenarios:
        print("=" * 80)
        print(f"TEST: {name}")
        print("=" * 80)
        print()

        epilogue = compose_epilogue(run_state)
        print(epilogue)
        print()
        print()
