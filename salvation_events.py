"""
Salvation Events - Act 2 and Act 3 Miracle Cards

These events provide positive momentum and hope during dark times.
Act 2 events help the crew survive to Act 3.
Act 3 events are conditional miracles that can save a doomed run.
"""

import random


# ============================================================================
# ACT II SALVATION EVENTS
# ============================================================================

def event_brief_reprieve(sim):
    """Brief Reprieve"""
    log = []

    # A quiet moment - everyone gains a little coherence
    log.append({"note": "✨ Brief reprieve - a moment of quiet"})

    for char_name, char in sim.characters.items():
        if not char.is_dead:
            change = sim.modify_character_c_self(char_name, +0.5, "brief reprieve")
            log.append(change)

    log.append({"note": "→ No one screams, dissolves, or bleeds"})
    log.append({"note": "→ A breath of quiet in the storm"})

    return {"log": log}


def event_unexpected_kindness(sim):
    """Unexpected Kindness"""
    log = []

    # A stranger helps - random dyad boost
    log.append({"note": "✨ A stranger returns a kindness"})

    # Get all dyads and pick one randomly
    if sim.relationships:
        dyad = random.choice(sim.relationships)
        dyad_change = sim.modify_dyad(dyad.char_a, dyad.char_b, +1.0, "unexpected kindness")
        log.append(dyad_change)
        log.append({"note": f"→ {dyad.char_a}-{dyad.char_b} bond strengthened"})
        log.append({"note": "→ Not everything hunts them"})

    return {"log": log}


def event_house_remembers(sim):
    """The House Remembers Them"""
    log = []

    log.append({"note": "🏠 The wards glow steady"})
    log.append({"note": "→ The Sanctuary feels like home again"})
    log.append({"note": "→ For the first time in months"})

    return {"log": log}


def event_maeve_field_bows(sim):
    """The Field Bows to Her (UNIQUE)"""
    log = []

    maeve = sim.get_character("Maeve")
    if not maeve:
        return {"log": log}

    log.append({"note": "⭐ Maeve makes a call only she can see"})

    # Maeve gains coherence
    maeve_change = sim.modify_character_c_self("Maeve", +2.0, "field bows to her brilliance")
    log.append(maeve_change)

    # All of Maeve's dyads strengthen
    for dyad in sim.relationships:
        if dyad.involves("Maeve"):
            other = dyad.get_other("Maeve")
            dyad_change = sim.modify_dyad("Maeve", other, +1.0, "stabilized by Maeve's resonance")
            log.append(dyad_change)

    log.append({"note": "→ The world reacts to her call"})
    log.append({"note": "→ For a moment her brilliance stabilizes everyone"})

    return {"log": log}


def event_kit_refuses_to_give_up(sim):
    """He Refuses to Give Up"""
    log = []

    kit = sim.get_character("Kit")
    yuul = sim.get_character("Yuul")

    if not (kit and yuul):
        return {"log": log}

    log.append({"note": "💙 Kit refuses to give up"})

    # Kit gains coherence
    kit_change = sim.modify_character_c_self("Kit", +2.0, "becomes the spine of the household")
    log.append(kit_change)

    # Yuul stabilizes
    yuul_change = sim.modify_character_c_self("Yuul", +1.0, "anchored by Kit's tenderness")
    log.append(yuul_change)

    # Their bond strengthens
    dyad_change = sim.modify_dyad("Kit", "Yuul", +1.0, "desperate tenderness")
    log.append(dyad_change)

    log.append({"note": "→ He anchors Yuul with desperate tenderness"})

    return {"log": log}


def event_rielle_truth(sim):
    """She Tells the Truth No One Wants to Hear"""
    log = []

    rielle = sim.get_character("Rielle")
    if not rielle:
        return {"log": log}

    log.append({"note": "🔥 Rielle speaks a truth that breaks the spiral"})

    # Rielle gains coherence
    rielle_change = sim.modify_character_c_self("Rielle", +1.0, "truth spoken")
    log.append(rielle_change)

    # Boost dyad with Maeve or Yuul (random)
    targets = []
    if sim.get_character("Maeve"):
        targets.append("Maeve")
    if sim.get_character("Yuul"):
        targets.append("Yuul")

    if targets:
        target = random.choice(targets)
        dyad_change = sim.modify_dyad("Rielle", target, +1.0, "someone finally listens")
        log.append(dyad_change)
        log.append({"note": f"→ {target} finally listens"})

    return {"log": log}


def event_daniel_fixes(sim):
    """He Fixes Something, Quietly"""
    log = []

    daniel = sim.get_character("Daniel")
    maeve = sim.get_character("Maeve")

    if not (daniel and maeve):
        return {"log": log}

    log.append({"note": "📋 Daniel pulls strings behind the scenes"})

    # Maeve-Daniel bond improves
    dyad_change = sim.modify_dyad("Maeve", "Daniel", +1.0, "Daniel buys them time")
    log.append(dyad_change)

    log.append({"note": "→ Reroutes a case, deletes a file"})
    log.append({"note": "→ Buys them time"})

    return {"log": log}


def event_farris_stands_guard(sim):
    """He Stands Between Them and the Dark (UNIQUE)"""
    log = []

    farris = sim.get_character("Farris")
    maeve = sim.get_character("Maeve")

    if not (farris and maeve):
        return {"log": log}

    log.append({"note": "🐺 A presence moves toward the Sanctuary"})
    log.append({"note": "→ Farris moves faster"})

    # Farris takes damage
    farris_change = sim.modify_character_c_self("Farris", -1.0, "destroys what approaches")
    log.append(farris_change)

    # But Maeve-Farris bond strengthens significantly
    dyad_change = sim.modify_dyad("Maeve", "Farris", +2.0, "he stands between her and the dark")
    log.append(dyad_change)

    log.append({"note": "→ He destroys what approaches, at cost to himself"})

    return {"log": log}


# ============================================================================
# ACT III MIRACLE EVENTS
# ============================================================================

def event_maeve_field_bows_act3(sim):
    """The Field Bows to Her (Act 3 Miracle)"""
    log = []

    maeve = sim.get_character("Maeve")
    if not maeve:
        return {"log": log}

    log.append({"note": "⭐ Maeve steps into the wound in the field"})

    # Check if Maeve is strong enough
    if maeve.c_self >= 4.0:
        # Success
        log.append({"note": "→ She stitches it shut with sheer force of will"})

        maeve_change = sim.modify_character_c_self("Maeve", +2.0, "psychic lighthouse flickers into being")
        log.append(maeve_change)

        # Strengthen all Maeve dyads
        for dyad in sim.relationships:
            if dyad.involves("Maeve"):
                other = dyad.get_other("Maeve")
                dyad_change = sim.modify_dyad("Maeve", other, +1.0, "Maeve's miracle stabilizes")
                log.append(dyad_change)

        log.append({"note": "✨ SUCCESS: A psychic lighthouse flickers into being"})

    else:
        # Penalty - overextended
        log.append({"note": "→ She reaches too far"})

        # Random dyad degrades
        maeve_dyads = [d for d in sim.relationships if d.involves("Maeve")]
        if maeve_dyads:
            dyad = random.choice(maeve_dyads)
            other = dyad.get_other("Maeve")
            dyad_change = sim.modify_dyad("Maeve", other, -1.0, "Maeve overextended")
            log.append(dyad_change)

        # Add scar
        maeve.add_scar("overextended")
        log.append({"note": "⚠️  Maeve gains scar: overextended"})

    return {"log": log}


def event_kit_refuses_act3(sim):
    """He Refuses to Give Up (Act 3 Miracle)"""
    log = []

    kit = sim.get_character("Kit")
    if not kit:
        return {"log": log}

    # Find character with lowest coherence
    lowest_char = None
    lowest_value = 999
    for char_name, char in sim.characters.items():
        if not char.is_dead and char_name != "Kit" and char.c_self < lowest_value:
            lowest_value = char.c_self
            lowest_char = char_name

    if not lowest_char:
        return {"log": log}

    log.append({"note": f"💙 {lowest_char} is seconds from dissolving"})
    log.append({"note": "→ Kit anchors them with desperate tenderness"})

    # Check if Kit is strong enough
    if kit.c_self >= 4.0:
        # Success
        target_change = sim.modify_character_c_self(lowest_char, +3.0, "dragged back from the brink")
        kit_change = sim.modify_character_c_self("Kit", +1.0, "refuses to give up")
        dyad_change = sim.modify_dyad("Kit", lowest_char, +2.0, "desperate rescue")

        log.extend([target_change, kit_change, dyad_change])
        log.append({"note": f"✨ SUCCESS: {lowest_char} dragged back from the brink"})

    else:
        # Failure - Kit isn't strong enough
        log.append({"note": "→ Kit reaches but cannot hold"})

        target_change = sim.modify_character_c_self(lowest_char, -1.0, "Kit's failure")
        dyad_change = sim.modify_dyad("Kit", lowest_char, -1.0, "helplessness")

        log.extend([target_change, dyad_change])

        kit.add_scar("helplessness")
        log.append({"note": "⚠️  Kit gains scar: helplessness"})

    return {"log": log}


def event_rielle_breaks_pattern_act3(sim):
    """She Breaks the Pattern (Act 3 Miracle)"""
    log = []

    rielle = sim.get_character("Rielle")
    if not rielle:
        return {"log": log}

    log.append({"note": "🔥 Rielle sees the resonance knot trapping them"})

    # Check if Rielle is strong enough
    if rielle.c_self >= 3.0:
        # Success
        log.append({"note": "→ She cuts it with furious, impossible clarity"})

        rielle_change = sim.modify_character_c_self("Rielle", +2.0, "breaks the pattern")
        log.append(rielle_change)

        log.append({"note": "✨ SUCCESS: The pattern breaks"})

    else:
        # Failure - devoured by the pattern
        log.append({"note": "→ The pattern devours her instead"})

        rielle.add_scar("devoured_by_pattern")
        log.append({"note": "⚠️  Rielle gains scar: devoured_by_pattern"})

    return {"log": log}


def event_daniel_protocol_null_act3(sim):
    """Protocol Null: He Chooses Them (Act 3 Miracle)"""
    log = []

    daniel = sim.get_character("Daniel")
    maeve = sim.get_character("Maeve")

    if not (daniel and maeve):
        return {"log": log}

    # Check if DCE path is fully locked
    dce_locked = False
    if hasattr(sim, 'act3_system'):
        dce_locked = sim.act3_system.special_flags.get("h11_max_pressure", False)

    if dce_locked:
        log.append({"note": "⚠️  Daniel is too deep in the Directorate"})
        log.append({"note": "→ This card cannot be played"})
        return {"log": log}

    log.append({"note": "📋 Daniel breaks protocol"})
    log.append({"note": "→ He sabotages a Directorate operation"})

    # Success - always succeeds if not locked
    dyad_change = sim.modify_dyad("Maeve", "Daniel", +2.0, "Daniel chooses them")
    log.append(dyad_change)

    log.append({"note": "✨ For one moment, he is theirs"})

    return {"log": log}


def event_farris_holds_line_act3(sim):
    """He Holds the Line Alone (Act 3 Miracle)"""
    log = []

    farris = sim.get_character("Farris")
    maeve = sim.get_character("Maeve")

    if not (farris and maeve):
        return {"log": log}

    log.append({"note": "🐺 A monstrous presence tears through the field"})
    log.append({"note": "→ Farris stands alone"})

    # Farris takes damage
    farris_change = sim.modify_character_c_self("Farris", -2.0, "holds the line alone")
    log.append(farris_change)

    # But bond with Maeve strengthens massively
    dyad_change = sim.modify_dyad("Maeve", "Farris", +3.0, "reality bends around his defiance")
    log.append(dyad_change)

    # Group stability boost (small boost to all)
    for char_name, char in sim.characters.items():
        if not char.is_dead and char_name != "Farris":
            change = sim.modify_character_c_self(char_name, +1.0, "Farris holds the line")
            log.append(change)

    log.append({"note": "✨ Reality bends around his defiance"})

    # Penalty if Farris was already weak
    if farris.c_self < 4.0:
        farris_penalty = sim.modify_character_c_self("Farris", -1.0, "frayed boundary")
        log.append(farris_penalty)
        farris.add_scar("frayed_boundary")
        log.append({"note": "⚠️  Farris gains scar: frayed_boundary"})

    return {"log": log}


def event_yuul_remembers_act3(sim):
    """She Remembers Herself Completely (Act 3 Miracle)"""
    log = []

    yuul = sim.get_character("Yuul")
    if not yuul:
        return {"log": log}

    log.append({"note": "✨ For one impossible moment..."})

    # Check if Yuul is strong enough
    if yuul.c_self >= 6.0:
        # Success - Yuul becomes whole
        log.append({"note": "→ Yuul is whole—prophet and human, bound and free"})

        yuul_change = sim.modify_character_c_self("Yuul", +3.0, "remembers herself completely")
        log.append(yuul_change)

        # Strengthen bonds with Kit and Maeve
        kit = sim.get_character("Kit")
        maeve = sim.get_character("Maeve")

        if kit:
            ky_change = sim.modify_dyad("Kit", "Yuul", +2.0, "Yuul hands them the perfect path")
            log.append(ky_change)

        if maeve:
            my_change = sim.modify_dyad("Maeve", "Yuul", +2.0, "vision of the perfect path")
            log.append(my_change)

        log.append({"note": "🌟 She hands them a vision of the perfect path"})
        log.append({"note": "✨ SUCCESS: Perfect timeline hint unlocked"})

        # Set special flag for perfect ending
        if hasattr(sim, 'act3_system'):
            sim.act3_system.special_flags["perfect_timeline_hint"] = True

    else:
        # Failure - Seeress surge
        log.append({"note": "→ The Seeress surges instead"})

        yuul_change = sim.modify_character_c_self("Yuul", -1.0, "Seeress consumes the moment")
        log.append(yuul_change)

        log.append({"note": "⚠️  FAILURE: Seeress takes control"})

    return {"log": log}


# ============================================================================
# ADDITIONAL FARRIS & DANIEL EVENTS (Act 2 & 3)
# ============================================================================

def event_farris_sees_before_it_moves(sim):
    """He Sees the Thing Before It Moves (Act 2)"""
    log = []

    farris = sim.get_character("Farris")
    maeve = sim.get_character("Maeve")

    if not (farris and maeve):
        return {"log": log}

    log.append({"note": "🐺 Farris senses a threat before it breaches"})
    log.append({"note": "→ He orders them to move"})

    # Maeve-Farris bond strengthens (she trusts his instincts)
    dyad_change = sim.modify_dyad("Maeve", "Farris", +1.0, "saved by seconds")
    log.append(dyad_change)

    log.append({"note": "→ They move by seconds. It's enough."})

    return {"log": log}


def event_farris_asks_maeve(sim):
    """He Asks Maeve What's Wrong (Act 2)"""
    log = []

    farris = sim.get_character("Farris")
    maeve = sim.get_character("Maeve")

    if not (farris and maeve):
        return {"log": log}

    log.append({"note": "🐺 Farris corners Maeve with a quiet, steady: 'Tell me.'"})

    # Maeve stabilizes
    maeve_change = sim.modify_character_c_self("Maeve", +1.0, "Farris' presence stabilizes")
    log.append(maeve_change)

    # Bond strengthens significantly
    dyad_change = sim.modify_dyad("Maeve", "Farris", +2.0, "his presence stabilizes her")
    log.append(dyad_change)

    log.append({"note": "→ His presence stabilizes her far more than she admits"})

    return {"log": log}


def event_farris_breaks_threshold(sim):
    """He Breaks the Threshold (Act 3 Miracle)"""
    log = []

    farris = sim.get_character("Farris")
    if not farris:
        return {"log": log}

    log.append({"note": "🐺 The field collapses inward"})
    log.append({"note": "→ Farris tears through the boundary itself"})

    # Farris takes damage
    farris_change = sim.modify_character_c_self("Farris", -1.0, "tears through reality")
    log.append(farris_change)

    # Group stability boost
    for char_name, char in sim.characters.items():
        if not char.is_dead and char_name != "Farris":
            change = sim.modify_character_c_self(char_name, +1.0, "field stabilizes")
            log.append(change)

    log.append({"note": "✨ Reality forced open with sheer will"})

    # Penalty if Farris was already weak
    if farris.c_self < 4.0:
        farris_penalty = sim.modify_character_c_self("Farris", -1.0, "frayed boundary")
        log.append(farris_penalty)
        farris.add_scar("frayed_boundary")
        log.append({"note": "⚠️  Farris gains scar: frayed_boundary"})

    return {"log": log}


def event_daniel_real_intel(sim):
    """He Shows Up With Real Intel (Act 2)"""
    log = []

    daniel = sim.get_character("Daniel")
    maeve = sim.get_character("Maeve")

    if not (daniel and maeve):
        return {"log": log}

    log.append({"note": "📋 Daniel brings a full, actionable report"})
    log.append({"note": "→ Maps, timestamps, movement data"})

    # Maeve-Daniel bond improves
    dyad_change = sim.modify_dyad("Maeve", "Daniel", +1.0, "broke rules to get intel")
    log.append(dyad_change)

    log.append({"note": "→ He broke rules to get it"})

    return {"log": log}


def event_daniel_snaps(sim):
    """Daniel Snaps at a Directorate Agent (Act 2)"""
    log = []

    daniel = sim.get_character("Daniel")
    maeve = sim.get_character("Maeve")

    if not (daniel and maeve):
        return {"log": log}

    log.append({"note": "📋 A Directorate agent speaks about Yuul like she's a specimen"})
    log.append({"note": "→ Daniel loses his composure—for them"})

    # Daniel gains coherence from choosing his side
    daniel_change = sim.modify_character_c_self("Daniel", +1.0, "chooses them over protocol")
    log.append(daniel_change)

    # Bond with Maeve improves
    dyad_change = sim.modify_dyad("Maeve", "Daniel", +1.0, "Daniel defends Yuul")
    log.append(dyad_change)

    log.append({"note": "→ He chose them"})

    return {"log": log}


def event_daniel_structural_override(sim):
    """Structural Override: Daniel's Rewrite (Act 3 Miracle)"""
    log = []

    daniel = sim.get_character("Daniel")
    maeve = sim.get_character("Maeve")

    if not (daniel and maeve):
        return {"log": log}

    # Check if DCE path is fully locked
    dce_locked = False
    if hasattr(sim, 'act3_system'):
        dce_locked = sim.act3_system.special_flags.get("h11_max_pressure", False)

    if dce_locked:
        log.append({"note": "⚠️  Daniel is too deep in the Directorate"})
        log.append({"note": "→ This card cannot be played"})
        return {"log": log}

    log.append({"note": "📋 Daniel overrides a Directorate protocol"})
    log.append({"note": "→ He wasn't meant to access this"})

    # Daniel takes damage for the override
    daniel_change = sim.modify_character_c_self("Daniel", -1.0, "structural override")
    log.append(daniel_change)

    # Bonds improve
    md_change = sim.modify_dyad("Maeve", "Daniel", +1.0, "Daniel rewrites reality for them")
    log.append(md_change)

    kit = sim.get_character("Kit")
    if kit and not kit.is_dead:
        kd_change = sim.modify_dyad("Kit", "Daniel", +1.0, "Daniel chooses them")
        log.append(kd_change)

    log.append({"note": "✨ The world buckles and rights itself"})

    return {"log": log}


# ============================================================================
# ACT III MIRACLE CHOICE EVENTS - High Stakes
# ============================================================================

def event_act3_door_breathes(sim):
    """The Door That Breathes (CHOICE)

    The Sanctuary door exhales. Wood ripples like skin.
    Yuul flickers—half here, half echo. A crossing point forms.

    Choice determines if they navigate it safely.
    """
    log = []

    yuul = sim.get_character("Yuul")
    if not yuul or yuul.is_dead:
        return {"log": log}

    log.append({"note": "🚪 The Sanctuary door exhales"})
    log.append({"note": "→ Wood ripples like skin"})
    log.append({"note": "→ Yuul flickers—half here, half echo"})

    # Base effects before choice
    sim.chaos_state.add_hybrid(0.5, 0.5)  # +1 chaos total
    log.append({"note": "   Chaos rises"})

    log.append({"note": "⚡ A crossing point forms..."})

    # Choice will be presented by game system
    # Effects depend on archetype chosen

    return {"log": log}


def event_act3_choir_not_choir(sim):
    """The Choir That Isn't (CHOICE)

    There is singing in the walls—overtones of something thinking.
    Yuul hums along without realizing it.

    Choice determines if they can navigate the auditory trap.
    """
    log = []

    yuul = sim.get_character("Yuul")
    if not yuul or yuul.is_dead:
        return {"log": log}

    log.append({"note": "🎵 Singing echoes through the walls"})
    log.append({"note": "→ Overtones of something thinking"})
    log.append({"note": "→ Yuul hums along without realizing"})

    # Base effects before choice
    # Pressure spike
    if hasattr(sim, 'chaos_state'):
        old_pressure = sim.chaos_state.pressure
        sim.chaos_state.pressure = min(10.0, old_pressure + 2.0)
        log.append({"note": f"   Pressure {old_pressure:.1f} → {sim.chaos_state.pressure:.1f}"})

    log.append({"note": "⚡ The chorus waits for response..."})

    # Choice will be presented by game system

    return {"log": log}


def event_act3_field_blinks(sim):
    """When the Field Blinks (CHOICE)

    Maps fold. Reality un-renders for a heartbeat.
    Names slide. Futures shake loose.

    Choice determines if they can stay grounded.
    """
    log = []

    log.append({"note": "🌀 Maps fold—reality un-renders"})
    log.append({"note": "→ Names slide sideways"})
    log.append({"note": "→ Futures shake loose"})

    # Base effects before choice
    sim.chaos_state.add_hybrid(1.5, 1.5)  # +3 chaos total
    log.append({"note": "   Chaos spikes violently"})

    # Random dyad strain
    if sim.relationships:
        dyad = random.choice(sim.relationships)
        dyad_change = sim.modify_dyad(dyad.char_a, dyad.char_b, -1.0, "field blinks—bonds strain")
        log.append(dyad_change)

    log.append({"note": "⚡ The world holds its breath..."})

    # Choice will be presented by game system

    return {"log": log}


def event_act3_name_wants_to_live(sim):
    """The Name That Wants to Live (CHOICE)

    Maeve hears the hidden name—the one beneath the Pattern,
    the one she never dared to claim.

    CRITICAL: Correct choice unlocks the Miracle ending path.
    """
    log = []

    maeve = sim.get_character("Maeve")
    if not maeve or maeve.is_dead:
        return {"log": log}

    # Only trigger if Maeve's coherence is high enough
    if maeve.c_self < 7:
        return {"log": log}

    log.append({"note": "✨ Maeve hears the hidden name"})
    log.append({"note": "→ Not the List's hunger"})
    log.append({"note": "→ The name beneath the Pattern"})
    log.append({"note": "→ Her own"})

    # Base positive effect
    maeve_change = sim.modify_character_c_self("Maeve", +3.0, "hears her true name")
    log.append(maeve_change)

    # Pressure relief
    if hasattr(sim, 'chaos_state'):
        old_pressure = sim.chaos_state.pressure
        sim.chaos_state.pressure = max(0.0, old_pressure - 2.0)
        log.append({"note": f"   Pressure {old_pressure:.1f} → {sim.chaos_state.pressure:.1f}"})

    log.append({"note": "⚡ THE CRITICAL MOMENT..."})
    log.append({"note": "→ If she claims it, the miracle becomes possible"})

    # The choice system will handle player selection
    # After this event, we need to check what they chose and unlock miracle if correct

    # NOTE: The miracle unlock will happen via the choice handler
    # For now, mark that this event occurred
    if hasattr(sim, 'act3_system'):
        sim.act3_system.special_flags["name_event_occurred"] = True

    return {"log": log}

