"""
Act-Based Event Functions

Event handlers for Act I and Act II of the Narrative Coherence Engine.
These events are organized by act and have textured chaos (turbulence/pressure).
"""

import random


# ============================================================================
# ACT I EVENTS - Misleading Calm
# ============================================================================

def event_kit_grounds_yuul_soft(sim):
    """Kit Tries to Ground Yuul"""
    log = []

    kit_change = sim.modify_character_c_self("Kit", +0.5, "grounds Yuul with care")
    yuul_change = sim.modify_character_c_self("Yuul", +0.3, "responds with slight delay")
    dyad_change = sim.modify_dyad("Kit", "Yuul", +0.5, "quiet stabilization")

    log.extend([kit_change, yuul_change, dyad_change])
    log.append({"note": "→ A moment of grounding, slightly off-rhythm"})

    return {"log": log}


def event_someone_notices(sim):
    """Someone Notices (CHOICE)"""
    log = []

    # External pressure - someone sees too much
    target = random.choice(["Yuul", "Maeve"])
    target_change = sim.modify_character_c_self(target, -0.5, "studied by stranger")

    log.append(target_change)
    log.append({"note": f"→ A stranger's gaze lingers on {target}: 'You look hollow.'"})

    return {"log": log}


def event_rielle_impulse_soft(sim):
    """Rielle's Impulse"""
    log = []

    # Rielle acts on instinct - it half-works
    rielle_change = sim.modify_character_c_self("Rielle", -0.3, "impulse half-works")

    # Random effect on one other person
    other = random.choice(["Yuul", "Maeve", "Kit"])
    other_change = sim.modify_character_c_self(other, +0.5, "helped by Rielle's impulse")

    log.extend([rielle_change, other_change])
    log.append({"note": "→ Instinct carries them forward, barely"})

    return {"log": log}


def event_grace_moment(sim):
    """Grace Moment"""
    log = []

    # Beautiful moment - shared experience
    yuul_change = sim.modify_character_c_self("Yuul", +0.5, "beautiful moment")
    maeve_change = sim.modify_character_c_self("Maeve", +0.5, "shared silence")
    kit_change = sim.modify_character_c_self("Kit", +0.5, "sunrise together")
    rielle_change = sim.modify_character_c_self("Rielle", +0.5, "genuine laughter")

    # Strengthen a random dyad
    pairs = [("Maeve", "Yuul"), ("Kit", "Yuul"), ("Maeve", "Kit"), ("Maeve", "Rielle")]
    pair = random.choice(pairs)
    dyad_change = sim.modify_dyad(pair[0], pair[1], +1.0, "grace moment")

    log.extend([yuul_change, maeve_change, kit_change, rielle_change, dyad_change])
    log.append({"note": "✨ A moment of genuine beauty"})

    return {"log": log}


def event_bonfire_night(sim):
    """Bonfire Night (CHOICE)"""
    log = []

    # Their last truly safe moment
    yuul_change = sim.modify_character_c_self("Yuul", +1.0, "safe moment around fire")
    maeve_change = sim.modify_character_c_self("Maeve", +1.0, "warmth and safety")
    kit_change = sim.modify_character_c_self("Kit", +1.0, "belonging")
    rielle_change = sim.modify_character_c_self("Rielle", +1.0, "connection")

    # Strengthen all dyads slightly
    my_change = sim.modify_dyad("Maeve", "Yuul", +0.5, "bonfire togetherness")
    ky_change = sim.modify_dyad("Kit", "Yuul", +0.5, "bonfire togetherness")
    mr_change = sim.modify_dyad("Maeve", "Rielle", +0.5, "bonfire togetherness")

    log.extend([yuul_change, maeve_change, kit_change, rielle_change, my_change, ky_change, mr_change])
    log.append({"note": "🔥 Their last truly safe moment"})

    return {"log": log}


def event_thing_avoided_soft(sim):
    """The Thing They've Been Avoiding"""
    log = []

    # A topic resurfaces, met with silence
    target = random.choice(["Maeve", "Kit", "Rielle"])
    target_change = sim.modify_character_c_self(target, -0.3, "avoidance resurfaces")

    log.append(target_change)
    log.append({"note": "→ A topic left unspoken grows heavier"})

    return {"log": log}


def event_mission_wrong_low(sim):
    """Mission Goes Wrong (Low-Stakes)"""
    log = []

    # Hunt gets sloppy, coordination falters
    kit_change = sim.modify_character_c_self("Kit", -0.5, "mission coordination fails")
    rielle_change = sim.modify_character_c_self("Rielle", -0.3, "hunt gets sloppy")

    # Dyad strain between Kit and Rielle
    kr_change = sim.modify_dyad("Kit", "Rielle", -0.5, "mission misalignment")

    log.extend([kit_change, rielle_change, kr_change])
    log.append({"note": "→ No one hurt, but trust frays"})

    return {"log": log}


def event_rielle_questions_early(sim):
    """Rielle Questions Maeve's Choice (Early)"""
    log = []

    # Soft rebuke, teasing but edged
    rielle_change = sim.modify_character_c_self("Rielle", -0.2, "questions choice")
    maeve_change = sim.modify_character_c_self("Maeve", -0.3, "defensive")

    mr_change = sim.modify_dyad("Maeve", "Rielle", -0.5, "soft questioning")

    log.extend([rielle_change, maeve_change, mr_change])
    log.append({"note": "→ Teasing, but there's an edge"})

    return {"log": log}


def event_maeve_reaches_early(sim):
    """Maeve Reaches Out to Yuul (Early)"""
    log = []

    # Maeve tries connecting; Yuul deflects
    maeve_change = sim.modify_character_c_self("Maeve", +0.3, "reaches out")
    yuul_change = sim.modify_character_c_self("Yuul", -0.2, "deflects connection")

    my_change = sim.modify_dyad("Maeve", "Yuul", -0.3, "deflection hurts")

    log.extend([maeve_change, yuul_change, my_change])
    log.append({"note": "→ Connection attempted, gently refused"})

    return {"log": log}


def event_yuul_reversals_soft(sim):
    """Yuul Speaks in Reversals (Soft)"""
    log = []

    # Yuul says something backward-feeling
    yuul_change = sim.modify_character_c_self("Yuul", -0.5, "speaks in reversals")

    # Others notice but shrug it off
    other = random.choice(["Maeve", "Kit"])
    other_change = sim.modify_character_c_self(other, -0.2, "unsettled by reversals")

    log.extend([yuul_change, other_change])
    log.append({"note": "→ Words feel backward, but harmless... right?"})

    return {"log": log}


def event_yuul_vision_soft(sim):
    """Yuul Vision (Soft) (CHOICE)"""
    log = []

    # An eerie micro-vision she shrugs off
    yuul_change = sim.modify_character_c_self("Yuul", -0.5, "micro-vision")
    maeve_change = sim.modify_character_c_self("Maeve", -0.3, "senses Yuul's unease")

    my_change = sim.modify_dyad("Maeve", "Yuul", -0.5, "vision not shared")

    log.extend([yuul_change, maeve_change, my_change])
    log.append({"note": "→ A flicker of something worse"})

    return {"log": log}


def event_trine_ritual_stable(sim):
    """Trine Ritual (Stable)"""
    log = []

    # Small ritual stabilizes Yuul
    yuul_change = sim.modify_character_c_self("Yuul", +0.5, "ritual stabilizes")
    maeve_change = sim.modify_character_c_self("Maeve", +0.3, "ritual grounds")
    rielle_change = sim.modify_character_c_self("Rielle", +0.3, "ritual succeeds")

    log.extend([yuul_change, maeve_change, rielle_change])
    log.append({"note": "→ The ritual holds, for now"})

    return {"log": log}


def event_soft_surveillance(sim):
    """Soft Surveillance"""
    log = []

    # A car, a shadow-maybe following
    target = random.choice(["Kit", "Maeve"])
    target_change = sim.modify_character_c_self(target, -0.3, "senses being watched")

    log.append(target_change)
    log.append({"note": "→ Was that car there before?"})

    return {"log": log}


def event_misaligned_questions(sim):
    """Misaligned Questions"""
    log = []

    # DCE asks something slightly off
    target = random.choice(["Kit", "Maeve", "Rielle"])
    target_change = sim.modify_character_c_self(target, -0.3, "odd questions from DCE")

    log.append(target_change)
    log.append({"note": "→ The questions don't quite line up"})

    return {"log": log}


def event_quiet_heroics(sim):
    """Quiet Heroics"""
    log = []

    # A mundane save, barely noticed
    hero = random.choice(["Kit", "Rielle"])
    hero_change = sim.modify_character_c_self(hero, +0.5, "quiet save")

    log.append(hero_change)
    log.append({"note": f"→ {hero} does something good. No one notices."})

    return {"log": log}


def event_internal_suspicion(sim):
    """Internal Suspicion"""
    log = []

    # A superior asks comforting questions that feel rehearsed
    target = random.choice(["Kit", "Maeve"])
    target_change = sim.modify_character_c_self(target, -0.5, "rehearsed comfort")

    log.append(target_change)
    log.append({"note": "→ The comfort feels scripted"})

    return {"log": log}


def event_case_solves_itself(sim):
    """Case Solves Itself"""
    log = []

    # A missing person returns with no explanation
    kit_change = sim.modify_character_c_self("Kit", -0.3, "unease at easy resolution")
    maeve_change = sim.modify_character_c_self("Maeve", -0.3, "knows this is wrong")

    log.extend([kit_change, maeve_change])
    log.append({"note": "→ Too easy. Something's off."})

    return {"log": log}


def event_quiet_town_watches(sim):
    """Quiet Town Watches"""
    log = []

    # Locals smile too warmly; eyes linger
    yuul_change = sim.modify_character_c_self("Yuul", -0.5, "too-warm smiles")
    rielle_change = sim.modify_character_c_self("Rielle", -0.3, "lingering eyes")

    log.extend([yuul_change, rielle_change])
    log.append({"note": "→ The warmth feels like a warning"})

    return {"log": log}


def event_yuul_forgets_date(sim):
    """Yuul Forgets Date"""
    log = []

    # A harmless lapse, shrugged off
    yuul_change = sim.modify_character_c_self("Yuul", -0.3, "forgets the date")

    log.append(yuul_change)
    log.append({"note": "→ Just a small slip. Nothing to worry about."})

    return {"log": log}


def event_map_wont_stay_still(sim):
    """The Map Won't Stay Still (BURN)"""
    log = []

    # Printed directions shift. Only Maeve sees it.
    maeve_change = sim.modify_character_c_self("Maeve", -1.0, "sees map shift")
    yuul_change = sim.modify_character_c_self("Yuul", -0.5, "reality feels unstable")

    my_change = sim.modify_dyad("Maeve", "Yuul", -0.5, "Maeve sees what Yuul prophesies")

    log.extend([maeve_change, yuul_change, my_change])
    log.append({"note": "🔥 BURN: Reality drift begins"})
    log.append({"note": "→ The printed map shouldn't change. But it did."})

    return {"log": log}


# ============================================================================
# ACT II EVENTS - Escalation
# ============================================================================

def event_kit_overextends(sim):
    """Kit Overextends"""
    log = []

    # Kit pushes too far, hides exhaustion poorly
    kit_change = sim.modify_character_c_self("Kit", -1.0, "overextends on case")
    yuul_change = sim.modify_character_c_self("Yuul", -0.3, "worried about Kit")

    ky_change = sim.modify_dyad("Kit", "Yuul", -0.5, "Kit hiding strain")

    log.extend([kit_change, yuul_change, ky_change])
    log.append({"note": "→ He's not okay, and everyone can tell"})

    return {"log": log}


def event_maeve_voice_slips(sim):
    """Maeve's Voice Slips"""
    log = []

    # Maeve says something she shouldn't know. Rielle notices.
    maeve_change = sim.modify_character_c_self("Maeve", -0.5, "knowledge slip")
    rielle_change = sim.modify_character_c_self("Rielle", -0.3, "notices the slip")

    mr_change = sim.modify_dyad("Maeve", "Rielle", -1.0, "suspicion grows")

    log.extend([maeve_change, rielle_change, mr_change])
    log.append({"note": "→ 'How did you know that?'"})

    return {"log": log}


def event_rielle_fracture_sign(sim):
    """Rielle Shows Fracture Sign"""
    log = []

    # A moment of sharpness breaks through her jokes
    rielle_change = sim.modify_character_c_self("Rielle", -0.5, "mask slips")
    maeve_change = sim.modify_character_c_self("Maeve", -0.3, "sees Rielle's pain")

    mr_change = sim.modify_dyad("Maeve", "Rielle", +0.3, "moment of truth")

    log.extend([rielle_change, maeve_change, mr_change])
    log.append({"note": "→ The joke cracks, revealing something raw"})

    return {"log": log}


def event_trine_ritual_heavy(sim):
    """Trine Ritual (Heavy)"""
    log = []

    # The ritual takes more than it gives
    yuul_change = sim.modify_character_c_self("Yuul", -0.3, "ritual drains")
    maeve_change = sim.modify_character_c_self("Maeve", -0.5, "ritual costs")
    rielle_change = sim.modify_character_c_self("Rielle", -0.5, "ritual exhausts")

    log.extend([yuul_change, maeve_change, rielle_change])
    log.append({"note": "→ The ritual holds, but at a cost"})

    return {"log": log}


def event_soft_betrayal_h11(sim):
    """Soft Betrayal in H11"""
    log = []

    # A report is filed without warning
    target = random.choice(["Kit", "Maeve"])
    target_change = sim.modify_character_c_self(target, -1.0, "betrayed by colleague")

    # Trust in team erodes
    if target == "Kit":
        kr_change = sim.modify_dyad("Kit", "Rielle", -0.5, "report filed without warning")
        log.append(kr_change)
    else:
        mr_change = sim.modify_dyad("Maeve", "Rielle", -0.5, "report filed without warning")
        log.append(mr_change)

    log.append(target_change)
    log.append({"note": "→ Someone went behind their back"})

    return {"log": log}


def event_case_shifts(sim):
    """Case Shifts"""
    log = []

    # Evidence contradicts itself
    kit_change = sim.modify_character_c_self("Kit", -0.5, "evidence contradicts")
    maeve_change = sim.modify_character_c_self("Maeve", -0.5, "reality unstable")

    log.extend([kit_change, maeve_change])
    log.append({"note": "→ The facts don't line up anymore"})

    return {"log": log}


def event_maeve_memory_glitch(sim):
    """Maeve Memory Glitch"""
    log = []

    # She forgets a step, a face, a timeline
    maeve_change = sim.modify_character_c_self("Maeve", -1.0, "memory glitch")
    yuul_change = sim.modify_character_c_self("Yuul", -0.3, "recognizes the signs")

    my_change = sim.modify_dyad("Maeve", "Yuul", -0.5, "shared unraveling")

    log.extend([maeve_change, yuul_change, my_change])
    log.append({"note": "→ She should remember this. Why doesn't she?"})

    return {"log": log}


def event_yuul_warning(sim):
    """Yuul Warning"""
    log = []

    # She speaks a location like a confession
    yuul_change = sim.modify_character_c_self("Yuul", -0.5, "prophetic confession")
    maeve_change = sim.modify_character_c_self("Maeve", -0.5, "hears the warning")
    kit_change = sim.modify_character_c_self("Kit", -0.5, "doesn't want to believe")

    log.extend([yuul_change, maeve_change, kit_change])
    log.append({"note": "→ The location is spoken like a death sentence"})

    return {"log": log}


def event_mission_wrong_higher(sim):
    """Mission Goes Wrong (Higher Stakes)"""
    log = []

    # Blood, panic, consequences
    kit_change = sim.modify_character_c_self("Kit", -1.0, "mission goes wrong")
    rielle_change = sim.modify_character_c_self("Rielle", -1.0, "panic sets in")

    kr_change = sim.modify_dyad("Kit", "Rielle", -1.0, "blame and fear")

    log.extend([kit_change, rielle_change, kr_change])
    log.append({"note": "→ Blood. Panic. A miss, not a disaster. But close."})

    return {"log": log}


def event_trine_mistrust(sim):
    """Trine Mistrust"""
    log = []

    # Someone hesitates at the wrong moment
    hesitator = random.choice(["Maeve", "Rielle"])
    other = "Rielle" if hesitator == "Maeve" else "Maeve"

    h_change = sim.modify_character_c_self(hesitator, -0.5, "hesitates")
    o_change = sim.modify_character_c_self(other, -0.5, "notices hesitation")
    yuul_change = sim.modify_character_c_self("Yuul", -0.5, "trine fractures")

    mr_change = sim.modify_dyad("Maeve", "Rielle", -1.0, "trust breaks")

    log.extend([h_change, o_change, yuul_change, mr_change])
    log.append({"note": f"→ {hesitator} hesitates. The moment shatters."})

    return {"log": log}


def event_ritual_backfire(sim):
    """Ritual Backfire"""
    log = []

    # Light bends wrong. Someone gets hurt.
    yuul_change = sim.modify_character_c_self("Yuul", -1.0, "ritual backfires")
    victim = random.choice(["Maeve", "Rielle"])
    victim_change = sim.modify_character_c_self(victim, -1.0, "hurt by ritual")

    log.extend([yuul_change, victim_change])
    log.append({"note": f"→ Light bends wrong. {victim} gets hurt."})

    return {"log": log}


def event_dce_checks_in(sim):
    """DCE Checks In"""
    log = []

    # Questions that imply suspicion
    target = random.choice(["Kit", "Maeve"])
    target_change = sim.modify_character_c_self(target, -0.5, "DCE suspicion")

    log.append(target_change)
    log.append({"note": "→ The questions are friendly. The subtext isn't."})

    return {"log": log}


def event_h11_pressure(sim):
    """H11 Pressure"""
    log = []

    # Deadlines grow sharp
    kit_change = sim.modify_character_c_self("Kit", -0.5, "deadline pressure")
    maeve_change = sim.modify_character_c_self("Maeve", -0.3, "organizational strain")

    log.extend([kit_change, maeve_change])
    log.append({"note": "→ The pressure from above intensifies"})

    return {"log": log}


def event_town_hostile(sim):
    """Town Turns Hostile"""
    log = []

    # Eyes narrow. Hospitality reverses.
    yuul_change = sim.modify_character_c_self("Yuul", -0.5, "hostility")
    rielle_change = sim.modify_character_c_self("Rielle", -0.5, "town turns")

    log.extend([yuul_change, rielle_change])
    log.append({"note": "→ The smiles are gone now"})

    return {"log": log}


def event_maeve_intuition_spike(sim):
    """Maeve Intuition Spike"""
    log = []

    # She senses danger before it arrives
    maeve_change = sim.modify_character_c_self("Maeve", +0.3, "intuition spike")
    yuul_change = sim.modify_character_c_self("Yuul", -0.3, "danger sensed")

    my_change = sim.modify_dyad("Maeve", "Yuul", +0.5, "prophetic connection")

    log.extend([maeve_change, yuul_change, my_change])
    log.append({"note": "→ Maeve knows before Yuul speaks"})

    return {"log": log}


def event_reality_drift(sim):
    """Reality Drift"""
    log = []

    # The ground beneath their choices bends
    yuul_change = sim.modify_character_c_self("Yuul", -1.0, "reality drifts")
    maeve_change = sim.modify_character_c_self("Maeve", -1.0, "foundation shifts")

    log.extend([yuul_change, maeve_change])
    log.append({"note": "→ Reality is no longer solid"})

    return {"log": log}


def event_kit_soft_breakdown(sim):
    """Kit Soft Breakdown"""
    log = []

    # He cries without realizing he started
    kit_change = sim.modify_character_c_self("Kit", -1.0, "soft breakdown")
    yuul_change = sim.modify_character_c_self("Yuul", -0.5, "sees Kit break")

    ky_change = sim.modify_dyad("Kit", "Yuul", -0.5, "breakdown witnessed")

    log.extend([kit_change, yuul_change, ky_change])
    log.append({"note": "→ He didn't notice when the tears started"})

    return {"log": log}


def event_yuul_static_edge(sim):
    """Yuul Static Edge"""
    log = []

    # For a moment she sounds like two people
    yuul_change = sim.modify_character_c_self("Yuul", -1.0, "voice splits")
    maeve_change = sim.modify_character_c_self("Maeve", -0.5, "hears the split")

    my_change = sim.modify_dyad("Maeve", "Yuul", -1.0, "identity fractures")

    log.extend([yuul_change, maeve_change, my_change])
    log.append({"note": "→ Two voices, one throat"})

    return {"log": log}


def event_rielle_vanishes_briefly(sim):
    """Rielle Vanishes Briefly"""
    log = []

    # She loses time. Comes back grinning.
    rielle_change = sim.modify_character_c_self("Rielle", -1.0, "loses time")
    maeve_change = sim.modify_character_c_self("Maeve", -0.5, "notices absence")

    mr_change = sim.modify_dyad("Maeve", "Rielle", -0.5, "time gap")

    log.extend([rielle_change, maeve_change, mr_change])
    log.append({"note": "→ 'Where were you?' 'What do you mean?'"})

    return {"log": log}


def event_town_memory_gap(sim):
    """Town Memory Gap"""
    log = []

    # A collective lapse. No one can recall the last five minutes.
    yuul_change = sim.modify_character_c_self("Yuul", -0.5, "collective lapse")
    kit_change = sim.modify_character_c_self("Kit", -0.5, "memory gap")

    log.extend([yuul_change, kit_change])
    log.append({"note": "→ What just happened? No one remembers."})

    return {"log": log}


def event_coherence_failure(sim):
    """Coherence Failure"""
    log = []

    # The field shudders. Something fundamental slips.
    yuul_change = sim.modify_character_c_self("Yuul", -1.5, "coherence failure")
    maeve_change = sim.modify_character_c_self("Maeve", -1.0, "field shudders")

    my_change = sim.modify_dyad("Maeve", "Yuul", -1.0, "fundamental slip")

    log.extend([yuul_change, maeve_change, my_change])
    log.append({"note": "⚠️ The field itself trembles"})

    return {"log": log}


def event_yuul_last_prophecy(sim):
    """Yuul's Last Prophecy (CHOICE)"""
    log = []

    # Yuul's voice thins and deepens. Warning, memory, farewell.
    yuul_change = sim.modify_character_c_self("Yuul", -1.0, "last prophecy")
    maeve_change = sim.modify_character_c_self("Maeve", -1.0, "hears farewell")
    kit_change = sim.modify_character_c_self("Kit", -0.5, "warning received")

    my_change = sim.modify_dyad("Maeve", "Yuul", -1.0, "prophetic goodbye")

    log.extend([yuul_change, maeve_change, kit_change, my_change])
    log.append({"note": "→ Her voice is warning, memory, and farewell all at once"})

    return {"log": log}


def event_prophetic_isolation(sim):
    """Prophetic Isolation (BURN, CHOICE)"""
    log = []

    # Yuul retreats inward after frightening surge
    yuul_change = sim.modify_character_c_self("Yuul", -2.0, "prophetic isolation")
    kit_change = sim.modify_character_c_self("Kit", -1.0, "Yuul pushes away")
    maeve_change = sim.modify_character_c_self("Maeve", -0.5, "isolation trauma")

    ky_change = sim.modify_dyad("Kit", "Yuul", -2.0, "pushed away")
    my_change = sim.modify_dyad("Maeve", "Yuul", -1.5, "retreat inward")

    log.extend([yuul_change, kit_change, maeve_change, ky_change, my_change])
    log.append({"note": "🔥 BURN: Yuul isolation trauma"})
    log.append({"note": "→ She locks the door from inside"})

    return {"log": log}


def event_mirror_incident(sim):
    """Mirror Incident (BURN, CHOICE)"""
    log = []

    # Mirror cracks impossibly. Reality folds at edges.
    yuul_change = sim.modify_character_c_self("Yuul", -1.5, "mirror incident")
    maeve_change = sim.modify_character_c_self("Maeve", -1.0, "reality folds")

    my_change = sim.modify_dyad("Maeve", "Yuul", -1.0, "shared horror")

    log.extend([yuul_change, maeve_change, my_change])
    log.append({"note": "🔥 BURN: Mirror incident"})
    log.append({"note": "→ The crack shouldn't look like that"})

    return {"log": log}


def event_dce_investigation(sim):
    """DCE Investigation (BURN, CHOICE)"""
    log = []

    # Agents arrive with perfect questions
    kit_change = sim.modify_character_c_self("Kit", -1.0, "DCE investigation")
    maeve_change = sim.modify_character_c_self("Maeve", -1.0, "agents know too much")

    log.extend([kit_change, maeve_change])
    log.append({"note": "🔥 BURN: DCE investigation begins"})
    log.append({"note": "→ They already know something"})

    return {"log": log}


def event_dce_tightens_net(sim):
    """DCE Tightens Net (BURN, CHOICE)"""
    log = []

    # Paperwork discrepancies, shadowing teams, subtle tests
    kit_change = sim.modify_character_c_self("Kit", -1.5, "net tightening")
    maeve_change = sim.modify_character_c_self("Maeve", -1.0, "surveillance everywhere")
    rielle_change = sim.modify_character_c_self("Rielle", -0.5, "subtle tests")

    log.extend([kit_change, maeve_change, rielle_change])
    log.append({"note": "🔥 BURN: DCE net tightens"})
    log.append({"note": "→ The walls are closing in"})

    return {"log": log}


def event_dce_raid_safehouse(sim):
    """DCE Raid Safehouse (BURN, CHOICE)"""
    log = []

    # Fallback location compromised
    kit_change = sim.modify_character_c_self("Kit", -2.0, "safehouse compromised")
    rielle_change = sim.modify_character_c_self("Rielle", -1.0, "nowhere safe")

    kr_change = sim.modify_dyad("Kit", "Rielle", -1.0, "paranoia grows")

    log.extend([kit_change, rielle_change, kr_change])
    log.append({"note": "🔥 BURN: Safehouse raided"})
    log.append({"note": "→ Someone was there. Recently."})

    return {"log": log}


def event_house_11_review(sim):
    """Horizon 11 Review (BURN, CHOICE)"""
    log = []

    # H11 leadership receives quiet inquiries
    kit_change = sim.modify_character_c_self("Kit", -1.0, "internal review")
    maeve_change = sim.modify_character_c_self("Maeve", -1.0, "wrong questions")

    log.extend([kit_change, maeve_change])
    log.append({"note": "🔥 BURN: H11 under review"})
    log.append({"note": "→ Someone internal is asking the wrong questions"})

    return {"log": log}


def event_orders_from_above(sim):
    """Orders From Above (BURN, CHOICE)"""
    log = []

    # A directive arrives, feels rehearsed
    kit_change = sim.modify_character_c_self("Kit", -1.5, "rehearsed orders")
    maeve_change = sim.modify_character_c_self("Maeve", -1.5, "directive feels wrong")

    log.extend([kit_change, maeve_change])
    log.append({"note": "🔥 BURN: Orders from above"})
    log.append({"note": "→ Someone else wrote this"})

    return {"log": log}


# ============================================================================
# EVENT LOOKUP TABLE
# ============================================================================

EVENT_FUNCTIONS = {
    # Act I
    "kit_grounds_yuul_soft": event_kit_grounds_yuul_soft,
    "someone_notices": event_someone_notices,
    "rielle_impulse_soft": event_rielle_impulse_soft,
    "grace_moment": event_grace_moment,
    "bonfire_night": event_bonfire_night,
    "thing_avoided_soft": event_thing_avoided_soft,
    "mission_wrong_low": event_mission_wrong_low,
    "rielle_questions_early": event_rielle_questions_early,
    "maeve_reaches_early": event_maeve_reaches_early,
    "yuul_reversals_soft": event_yuul_reversals_soft,
    "yuul_vision_soft": event_yuul_vision_soft,
    "trine_ritual_stable": event_trine_ritual_stable,
    "soft_surveillance": event_soft_surveillance,
    "misaligned_questions": event_misaligned_questions,
    "quiet_heroics": event_quiet_heroics,
    "internal_suspicion": event_internal_suspicion,
    "case_solves_itself": event_case_solves_itself,
    "quiet_town_watches": event_quiet_town_watches,
    "yuul_forgets_date": event_yuul_forgets_date,
    "map_wont_stay_still": event_map_wont_stay_still,

    # Act II
    "kit_overextends": event_kit_overextends,
    "maeve_voice_slips": event_maeve_voice_slips,
    "rielle_fracture_sign": event_rielle_fracture_sign,
    "trine_ritual_heavy": event_trine_ritual_heavy,
    "soft_betrayal_h11": event_soft_betrayal_h11,
    "case_shifts": event_case_shifts,
    "maeve_memory_glitch": event_maeve_memory_glitch,
    "yuul_warning": event_yuul_warning,
    "mission_wrong_higher": event_mission_wrong_higher,
    "trine_mistrust": event_trine_mistrust,
    "ritual_backfire": event_ritual_backfire,
    "dce_checks_in": event_dce_checks_in,
    "h11_pressure": event_h11_pressure,
    "town_hostile": event_town_hostile,
    "maeve_intuition_spike": event_maeve_intuition_spike,
    "reality_drift": event_reality_drift,
    "kit_soft_breakdown": event_kit_soft_breakdown,
    "yuul_static_edge": event_yuul_static_edge,
    "rielle_vanishes_briefly": event_rielle_vanishes_briefly,
    "town_memory_gap": event_town_memory_gap,
    "coherence_failure": event_coherence_failure,
    "yuul_last_prophecy": event_yuul_last_prophecy,
    "prophetic_isolation": event_prophetic_isolation,
    "mirror_incident": event_mirror_incident,
    "dce_investigation": event_dce_investigation,
    "dce_tightens_net": event_dce_tightens_net,
    "dce_raid_safehouse": event_dce_raid_safehouse,
    "house_11_review": event_house_11_review,
    "orders_from_above": event_orders_from_above,
}


# ============================================================================
# ACT III EVENTS - Collapse or Transcendence
# ============================================================================

def event_first_warning_returns(sim):
    """The First Warning Returns"""
    log = []

    # Yuul grabs Maeve-eyes glassy, speech inverted
    yuul_change = sim.modify_character_c_self("Yuul", -1.0, "first warning returns")
    maeve_change = sim.modify_character_c_self("Maeve", -0.5, "hears dire warning")

    my_change = sim.modify_dyad("Maeve", "Yuul", -0.5, "prophetic terror")

    log.extend([yuul_change, maeve_change, my_change])
    log.append({"note": "→ A second warning, more frantic than the first"})

    return {"log": log}


def event_rielle_sees_it_too(sim):
    """Rielle Sees It Too"""
    log = []

    # Rielle corners Maeve with hard truth
    rielle_change = sim.modify_character_c_self("Rielle", -0.3, "speaks hard truth")
    maeve = sim.get_character("Maeve")

    if maeve and maeve.c_self < 6:
        maeve_change = sim.modify_character_c_self("Maeve", -1.0, "confronted by Rielle")
        log.append(maeve_change)

    mr_change = sim.modify_dyad("Maeve", "Rielle", -0.5, "harsh confrontation")

    log.extend([rielle_change, mr_change])
    log.append({"note": "→ 'You keep leaving. Kit's drowning. She's getting worse.'"})

    return {"log": log}


def event_photo_album_memory(sim):
    """The Photo Album"""
    log = []

    # Kit brings old photos - Yuul returns for one fragile night
    kit_change = sim.modify_character_c_self("Kit", +1.0, "photo album memory")
    yuul_change = sim.modify_character_c_self("Yuul", +2.0, "fully present for one night")

    # Mark as temporary (will need to be reverted)
    yuul = sim.get_character("Yuul")
    if yuul:
        yuul.apply_temp_buff(2.0, sim.round_number + 1)

    ky_change = sim.modify_dyad("Kit", "Yuul", +1.0, "precious memory")

    log.extend([kit_change, yuul_change, ky_change])
    log.append({"note": "→ He memorizes her. Every detail."})
    log.append({"note": "⏰ Yuul's coherence will fade next round"})

    return {"log": log}


def event_list_theory_obsession(sim):
    """The List Theory (Maeve's Obsession Solidifies)"""
    log = []

    # Maeve's obsession crystallizes
    maeve = sim.get_character("Maeve")
    if maeve:
        maeve.add_tag("obsession")

    if hasattr(sim, 'act3_system'):
        sim.act3_system.special_flags["obsession"] = True

    maeve_change = sim.modify_character_c_self("Maeve", +0.5, "obsession solidifies")

    log.append(maeve_change)
    log.append({"note": "🏷️ Maeve gains tag: obsession"})
    log.append({"note": "→ The List hunts Yuul. She can fight it."})

    return {"log": log}


def event_seeress_speaks(sim):
    """The Seeress Speaks"""
    log = []

    # Yuul's eyes go blank - The Seeress emerges
    yuul_change = sim.modify_character_c_self("Yuul", -1.0, "Seeress speaks")

    log.append(yuul_change)
    log.append({"note": "👁️ Yuul's eyes go blank. The Seeress looks out."})
    log.append({"note": "→ 'You can never leave this place.'"})

    return {"log": log}


def event_kit_breaks(sim):
    """Kit Breaks"""
    log = []

    # Kit finally snaps
    kit_change = sim.modify_character_c_self("Kit", -1.0, "breaks under pressure")

    kit = sim.get_character("Kit")
    if kit and kit.c_self <= 5:
        if hasattr(sim, 'act3_system'):
            sim.act3_system.special_flags["desperate_protector_mode"] = True
            log.append({"note": "⚔️ Kit enters DESPERATE PROTECTOR MODE"})

    log.append(kit_change)
    log.append({"note": "→ 'Do something. Please.'"})
    log.append({"note": "→ His breaking loads the gun the next card will fire"})

    return {"log": log}


def event_maeve_true_insight(sim):
    """Maeve's True Obsession - The Insight That Saves Them"""
    log = []

    # Maeve realizes the real pattern
    maeve_change = sim.modify_character_c_self("Maeve", +1.0, "True Insight achieved")

    if hasattr(sim, 'act3_system'):
        sim.act3_system.ending_paths_unlocked["miracle"] = True
        sim.act3_system.special_flags["true_insight_unlocked"] = True

    log.append(maeve_change)
    log.append({"note": "✨ MAEVE ACHIEVES TRUE INSIGHT"})
    log.append({"note": "→ The List feeds on extremes-BOTH dissolution AND ascension"})
    log.append({"note": "→ Survival means holding the middle"})
    log.append({"note": "🎯 MIRACLE ENDING PATH UNLOCKED"})

    return {"log": log}


def event_redchurch_prelude(sim):
    """Redchurch Prelude"""
    log = []

    # The moment before everything changes
    log.append({"note": "→ The moment before everything changes"})
    log.append({"note": "→ The air tastes metallic"})

    return {"log": log}


def event_kettle_blackout(sim):
    """The Kettle Blackout"""
    log = []

    # Daniel makes a call
    log.append({"note": "→ Daniel makes the call"})
    log.append({"note": "→ Does Maeve lie to protect them, or tell the truth?"})

    return {"log": log}


def event_dream_bleeds_through(sim):
    """The Dream Bleeds Through"""
    log = []

    # Reality drift - images repeat
    target = random.choice(["Yuul", "Maeve"])
    target_change = sim.modify_character_c_self(target, -0.5, "dream bleeds through")

    log.append(target_change)
    log.append({"note": "→ Images repeat. Edges double. Echo overlaps begin."})

    return {"log": log}


def event_coherence_whiplash(sim):
    """Coherence Whiplash"""
    log = []

    # High coherence drops, low coherence rises
    for char_name, char in sim.characters.items():
        if char.c_self >= 7:
            change = sim.modify_character_c_self(char_name, -1.0, "coherence whiplash (high drop)")
            log.append(change)
        elif char.c_self <= 4:
            change = sim.modify_character_c_self(char_name, +1.0, "coherence whiplash (low rise)")
            log.append(change)

    log.append({"note": "→ The field snaps toward the deadly middle"})

    return {"log": log}


def event_house_that_hears(sim):
    """The House That Hears"""
    log = []

    # The walls echo wrong
    target = random.choice(["Maeve", "Kit", "Yuul"])
    target_change = sim.modify_character_c_self(target, -0.5, "house listens")

    log.append(target_change)
    log.append({"note": "→ The walls echo wrong. A pattern repeats."})
    log.append({"note": "→ Something is listening."})

    return {"log": log}


def event_radio_bleeds(sim):
    """The Radio Bleeds"""
    log = []

    # Static resolves into DCE voices
    if hasattr(sim, 'act3_system'):
        sim.act3_system.dce_pressure += 1

    log.append({"note": "→ Static resolves into voices. DCE frequencies."})
    log.append({"note": "→ They're triangulating."})

    return {"log": log}


def event_daniel_calls_dce(sim):
    """Daniel Calls the DCE (BURN, CHOICE)"""
    log = []

    # Daniel thinks he's helping - calls the Directorate
    daniel = sim.get_character("Daniel")
    if daniel:
        daniel_change = sim.modify_character_c_self("Daniel", -1.5, "calls DCE")
        log.append(daniel_change)

    yuul_change = sim.modify_character_c_self("Yuul", -2.0, "DCE intervention looming")
    kit_change = sim.modify_character_c_self("Kit", -1.0, "betrayal from above")

    log.extend([yuul_change, kit_change])
    log.append({"note": "🔥 BURN: Daniel calls the Directorate"})
    log.append({"note": "→ 'They send three agents. For Yuul.'"})

    # Apply burn effects
    if hasattr(sim, 'act3_system'):
        sim.act3_system.pressure_baseline += 3.0
        sim.act3_system.dce_pressure += 3
        log.append({"note": "📈 Pressure baseline +3.0 (DCE intervention)"})

    return {"log": log}


def event_rielle_burns_redchurch(sim):
    """Rielle Burns Redchurch (BURN, CHOICE)"""
    log = []

    # Rielle acts alone - burns the wound-site
    rielle_change = sim.modify_character_c_self("Rielle", -2.0, "burns Redchurch")
    yuul_change = sim.modify_character_c_self("Yuul", -1.5, "screams across distance")

    # Sever the Trine
    my_change = sim.modify_dyad("Maeve", "Yuul", -2.0, "Trine ruptures")
    mr_change = sim.modify_dyad("Maeve", "Rielle", -2.0, "Trine ruptures")
    yr_change = sim.modify_dyad("Yuul", "Rielle", -2.0, "Trine ruptures")

    log.extend([rielle_change, yuul_change, my_change, mr_change, yr_change])
    log.append({"note": "🔥 BURN: Redchurch burns"})
    log.append({"note": "💔 THE WITCH TRINE SEVERS"})
    log.append({"note": "→ Rielle acts alone. The fire spreads."})

    # Apply burn effects
    if hasattr(sim, 'act3_system'):
        sim.act3_system.special_flags["trine_severed"] = True
        sim.act3_system.special_flags["redchurch_burned"] = True

    return {"log": log}


def event_the_mirror_transformation(sim):
    """The Mirror - Yuul's Ascension/Dissolution (BURN)"""
    log = []

    # Yuul stands before the Mirror - The Seeress dances
    yuul = sim.get_character("Yuul")

    if yuul:
        # Yuul becomes extreme - either dissolves toward 0 or ascends toward 10
        if yuul.c_self <= 3:
            # Dissolution path
            yuul_change = sim.modify_character_c_self("Yuul", -yuul.c_self, "dissolves into the Mirror")
            log.append(yuul_change)
            log.append({"note": "🔥 BURN: Yuul dissolves"})
            log.append({"note": "→ She steps through the glass. Gone."})
        else:
            # Ascension path
            ascension = 10.0 - yuul.c_self
            yuul_change = sim.modify_character_c_self("Yuul", ascension, "becomes the Seeress")
            log.append(yuul_change)
            log.append({"note": "🔥 BURN: Yuul transforms"})
            log.append({"note": "→ The Seeress dances. Yuul mirrors her. She BECOMES."})

    kit = sim.get_character("Kit")
    if kit:
        kit_change = sim.modify_character_c_self("Kit", -2.0, "watches transformation")
        log.append(kit_change)

    return {"log": log}


def event_the_list_manifests(sim):
    """The List Manifests (BURN, CHOICE)"""
    log = []

    # The entity that eats names descends
    log.append({"note": "🔥 BURN: THE LIST MANIFESTS"})
    log.append({"note": "→ The entity descends"})
    log.append({"note": "→ High coherence and low coherence both become prey"})

    # Hit extremes hardest
    for char_name, char in sim.characters.items():
        if char.c_self >= 8:
            change = sim.modify_character_c_self(char_name, -2.0, "marked by List (high)")
            log.append(change)
            char.marked_by_list = True
        elif char.c_self <= 2:
            change = sim.modify_character_c_self(char_name, -2.0, "marked by List (low)")
            log.append(change)
            char.marked_by_list = True

    log.append({"note": "→ Names begin to glow"})

    return {"log": log}


def event_kit_confession_sacred(sim):
    """Kit Confesses His Love (CHOICE)"""
    log = []

    # Kit finally speaks: "It's always been you."
    kit_change = sim.modify_character_c_self("Kit", +1.0, "confesses love")
    yuul_change = sim.modify_character_c_self("Yuul", +2.0, "remembers being a person")

    ky_change = sim.modify_dyad("Kit", "Yuul", +1.5, "sacred confession")

    log.extend([kit_change, yuul_change, ky_change])
    log.append({"note": "💕 Kit confesses: 'It's always been you.'"})
    log.append({"note": "→ Yuul remembers what it means to be loved"})

    # Check if dyad becomes sacred
    kit_yuul = sim.get_dyad("Kit", "Yuul")
    if kit_yuul and kit_yuul.c_dyad >= 9:
        log.append({"note": "✨ Kit-Yuul bond reaches SACRED threshold"})
        if hasattr(sim, 'act3_system'):
            sim.act3_system.ending_paths_unlocked["disappearance"] = True
            log.append({"note": "🎯 DISAPPEARANCE ENDING PATH UNLOCKED"})

    return {"log": log}


def event_dce_restraint_order(sim):
    """DCE Restraint Order"""
    log = []

    # Daniel decides: defect or authorize the raid
    daniel = sim.get_character("Daniel")

    if daniel and daniel.c_self <= 4:
        # Daniel defects
        daniel_change = sim.modify_character_c_self("Daniel", +1.0, "defects to protect H11")
        log.append(daniel_change)
        log.append({"note": "→ Daniel tears up the restraint order"})
        log.append({"note": "→ 'I won't let them take her.'"})

        if hasattr(sim, 'act3_system'):
            sim.act3_system.dce_pressure -= 1
    else:
        # Daniel authorizes
        kit_change = sim.modify_character_c_self("Kit", -1.0, "DCE closing in")
        yuul_change = sim.modify_character_c_self("Yuul", -0.5, "hunted")

        log.extend([kit_change, yuul_change])
        log.append({"note": "→ Daniel signs the order"})
        log.append({"note": "→ The net tightens"})

        if hasattr(sim, 'act3_system'):
            sim.act3_system.dce_pressure += 1

    return {"log": log}


def event_choirbreak_moment(sim):
    """The Choirbreak Moment"""
    log = []

    # A fracture in sound - everyone loses coherence except Maeve with True Insight
    log.append({"note": "→ A fracture in sound. Reality splinters."})

    has_true_insight = False
    if hasattr(sim, 'act3_system'):
        has_true_insight = sim.act3_system.special_flags.get("true_insight_unlocked", False)

    for char_name, char in sim.characters.items():
        if char_name == "Maeve" and has_true_insight:
            # Maeve is protected
            log.append({"note": f"  ✓ Maeve protected by True Insight"})
        else:
            change = sim.modify_character_c_self(char_name, -1.0, "choirbreak fracture")
            log.append(change)

    return {"log": log}


def event_thread_cuts(sim):
    """The Thread Cuts"""
    log = []

    # A Sacred dyad shatters
    sacred_dyads = [rel for rel in sim.relationships if rel.is_sacred]

    if sacred_dyads:
        # Pick a random sacred dyad to shatter
        import random
        target_dyad = random.choice(sacred_dyads)

        dyad_change = sim.modify_dyad(target_dyad.char_a, target_dyad.char_b, -3.0, "thread cuts")
        log.append(dyad_change)
        log.append({"note": f"💔 SACRED DYAD SHATTERS: {target_dyad.char_a}-{target_dyad.char_b}"})
        log.append({"note": "→ The thread cuts. Pressure drops. Chaos rises."})
    else:
        # No sacred dyads - hit strongest dyad
        strongest = max(sim.relationships, key=lambda r: r.c_dyad)
        dyad_change = sim.modify_dyad(strongest.char_a, strongest.char_b, -2.0, "thread strains")
        log.append(dyad_change)
        log.append({"note": "→ The strongest thread strains under pressure"})

    return {"log": log}


def event_name_eater_stirs(sim):
    """The Name Eater Stirs"""
    log = []

    # High coherence names begin to glow - marked as prey
    log.append({"note": "→ The Name Eater stirs"})

    marked_any = False
    for char_name, char in sim.characters.items():
        if char.c_self >= 7:
            char.marked_by_list = True
            change = sim.modify_character_c_self(char_name, -0.5, "name glows")
            log.append(change)
            log.append({"note": f"  ⚠️ {char_name}'s name begins to GLOW"})
            marked_any = True

    if marked_any:
        log.append({"note": "→ High coherence = visible prey"})
    else:
        log.append({"note": "→ No high coherence targets... yet"})

    return {"log": log}


# Add to EVENT_FUNCTIONS lookup
EVENT_FUNCTIONS.update({
    # Act III
    "first_warning_returns": event_first_warning_returns,
    "rielle_sees_it_too": event_rielle_sees_it_too,
    "photo_album_memory": event_photo_album_memory,
    "list_theory_obsession": event_list_theory_obsession,
    "seeress_speaks": event_seeress_speaks,
    "kit_breaks": event_kit_breaks,
    "maeve_true_insight": event_maeve_true_insight,
    "redchurch_prelude": event_redchurch_prelude,
    "kettle_blackout": event_kettle_blackout,
    "dream_bleeds_through": event_dream_bleeds_through,
    "coherence_whiplash": event_coherence_whiplash,
    "house_that_hears": event_house_that_hears,
    "radio_bleeds": event_radio_bleeds,
    "daniel_calls_dce": event_daniel_calls_dce,
    "rielle_burns_redchurch": event_rielle_burns_redchurch,
    "the_mirror_transformation": event_the_mirror_transformation,
    "the_list_manifests": event_the_list_manifests,
    "kit_confession_sacred": event_kit_confession_sacred,
    "dce_restraint_order": event_dce_restraint_order,
    "choirbreak_moment": event_choirbreak_moment,
    "thread_cuts": event_thread_cuts,
    "name_eater_stirs": event_name_eater_stirs,
})

