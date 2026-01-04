"""
Event card system for the Narrative Coherence Engine
"""

import random
from typing import Dict, List, Callable, Any


class Event:
    """Represents a narrative event card"""

    def __init__(
        self,
        id: int,
        name: str,
        category: str,
        description: str,
        chaos_base: float,
        apply_func: Callable
    ):
        self.id = id
        self.name = name
        self.category = category
        self.description = description
        self.chaos_base = chaos_base
        self.apply_func = apply_func

    def apply(self, simulation) -> Dict[str, Any]:
        """Apply this event to the simulation"""
        return self.apply_func(simulation)

    def __repr__(self):
        return f"[{self.id}] {self.name} (Chaos: {self.chaos_base:+.0f})"


# Event card definitions
# Each event is defined as a function that takes the simulation and returns a log of changes

def event_1_yuul_vision_horror(sim):
    """Card 1: Yuul Has a Vision - Horror"""
    log = []
    chaos_change = 2

    # Base effects
    yuul_change = sim.modify_character_c_self("Yuul", -1, "sees something terrible")
    maeve_change = sim.modify_character_c_self("Maeve", -0.5, "stressed by Yuul's vision")
    dyad_change = sim.modify_dyad("Maeve", "Yuul", -1, "Maeve doesn't want to hear it")

    log.extend([yuul_change, maeve_change, dyad_change])

    # Conditional: if Maeve.c_self < 5, dyad impact doubles
    maeve = sim.get_character("Maeve")
    if maeve and maeve.c_self < 5:
        extra_change = sim.modify_dyad("Maeve", "Yuul", -1, "Maeve can't handle it (doubled impact)")
        log.append(extra_change)
        log.append({"note": "⚠ Maeve's low coherence doubles the dyad impact"})

    return {"chaos": chaos_change, "log": log}


def event_2_prophetic_isolation(sim):
    """Card 2: Prophetic Isolation"""
    log = []
    chaos_change = 0

    # Choose who suggests isolation (for this automation, randomly pick Maeve or Rielle)
    suggester = random.choice(["Maeve", "Rielle"])

    yuul_change = sim.modify_character_c_self("Yuul", -1, "isolated prophetically")
    kit_change = sim.modify_character_c_self("Kit", -0.5, "objects but powerless")

    log.extend([yuul_change, kit_change])
    log.append({"note": f"→ {suggester} suggests the isolation"})

    # Dyad changes based on suggester
    if suggester == "Maeve":
        dyad_change = sim.modify_dyad("Maeve", "Yuul", -1, "Maeve suggests isolation")
        log.append(dyad_change)
    elif suggester == "Rielle":
        dyad_change = sim.modify_dyad("Rielle", "Yuul", -1, "Rielle suggests isolation")
        log.append(dyad_change)

    # Kit-Maeve tension
    tension = sim.modify_dyad("Maeve", "Kit", -0.5, "tension over disagreement")
    log.append(tension)

    # Conditional: if Yuul.c_self < 4, isolation accelerates
    yuul = sim.get_character("Yuul")
    if yuul and yuul.c_self < 4:
        extra_change = sim.modify_character_c_self("Yuul", -0.5, "isolation accelerates (x1.5)")
        log.append(extra_change)
        log.append({"note": "⚠ Yuul's low coherence accelerates isolation"})

    return {"chaos": chaos_change, "log": log}


def event_3_yuul_speaks_reversals(sim):
    """Card 3: Yuul Speaks in Reversals"""
    log = []
    chaos_change = 2

    yuul_change = sim.modify_character_c_self("Yuul", -0.5, "speaks in reversals")
    log.append(yuul_change)

    # Check all dyads with Yuul
    yuul_dyads = sim.get_character_dyads("Yuul")

    for dyad in yuul_dyads:
        other_char = dyad.char_a if dyad.char_b == "Yuul" else dyad.char_b

        if dyad.c_dyad < 5:
            change = sim.modify_dyad("Yuul", other_char, -1, f"{other_char} pulls away (dyad < 5)")
            log.append(change)
        elif dyad.c_dyad >= 7:
            log.append({"note": f"→ {other_char} can still reach Yuul (dyad >= 7)"})

    # Kit tries harder (special case)
    kit_change = sim.modify_dyad("Kit", "Yuul", 0.5, "Kit tries harder")
    log.append(kit_change)

    return {"chaos": chaos_change, "log": log}


def event_4_mirror_incident(sim):
    """Card 4: The Mirror Incident"""
    log = []
    chaos_change = 5  # Reality breach

    # Randomly determine who finds her
    possible_witnesses = ["Maeve", "Kit", "Rielle"]
    witness = random.choice(possible_witnesses)

    yuul_change = sim.modify_character_c_self("Yuul", -2, "the mirror incident")
    witness_change = sim.modify_character_c_self(witness, -0.5, f"disturbed by finding Yuul")

    log.append(yuul_change)
    log.append(witness_change)
    log.append({"note": f"→ {witness} finds Yuul"})

    # Dyad effect depends on bond strength
    witness_yuul_dyad = sim.get_dyad("Yuul", witness)
    if witness_yuul_dyad:
        if witness_yuul_dyad.c_dyad >= 7:
            change = sim.modify_dyad("Yuul", witness, 1, f"{witness} feels deep concern")
            log.append(change)
        elif witness_yuul_dyad.c_dyad < 5:
            change = sim.modify_dyad("Yuul", witness, -1, f"{witness} feels fear")
            log.append(change)

    # Check for cascade
    yuul = sim.get_character("Yuul")
    if yuul and yuul.c_self <= 3:
        log.append({"warning": "⚠⚠⚠ CASCADE MAY TRIGGER - Yuul at critical threshold!"})

    return {"chaos": chaos_change, "log": log}


def event_5_kit_grounds_yuul(sim):
    """Card 5: Kit Tries to Ground Yuul"""
    log = []
    chaos_change = -1  # Stabilizing attempt

    kit = sim.get_character("Kit")

    # Success chance based on Kit's coherence
    success_chance = kit.c_self * 0.2 if kit else 0
    success = random.random() < success_chance

    if kit and kit.c_self >= 5 and success:
        # Successful grounding
        yuul_change = sim.modify_character_c_self("Yuul", 1, "grounded by Kit")
        kit_change = sim.modify_character_c_self("Kit", -0.5, "exhausted by effort")
        dyad_change = sim.modify_dyad("Kit", "Yuul", 1, "successful grounding attempt")

        log.append({"note": f"✓ Kit succeeds in grounding Yuul (chance: {success_chance:.0%})"})
        log.extend([yuul_change, kit_change, dyad_change])
    else:
        # Failed attempt
        yuul_change = sim.modify_character_c_self("Yuul", -0.5, "grounding attempt fails")
        kit_change = sim.modify_character_c_self("Kit", -0.5, "exhausted and failed")

        log.append({"note": f"✗ Kit fails to ground Yuul (Kit c_self: {kit.c_self:.1f})"})
        log.extend([yuul_change, kit_change])

    return {"chaos": chaos_change, "log": log}


def event_6_someone_notices(sim):
    """Card 6: Someone Notices (Kit's feelings for Yuul)"""
    log = []
    chaos_change = 2

    # Randomly pick who notices
    possible_observers = ["Maeve", "Rielle"]
    observer = random.choice(possible_observers)

    kit_change = sim.modify_character_c_self("Kit", -0.5, "vulnerability exposed")
    log.append(kit_change)
    log.append({"note": f"→ {observer} notices Kit's feelings for Yuul"})

    # Yuul may learn about it
    if random.random() < 0.5:
        yuul_change = sim.modify_character_c_self("Yuul", 0.5, "feels seen")
        log.append(yuul_change)

    # Observer reaction depends on who they are
    if observer == "Maeve":
        # More likely to offer help
        if random.random() < 0.7:
            dyad_change = sim.modify_dyad("Kit", "Maeve", 1, "Maeve offers support")
            log.append(dyad_change)
        else:
            dyad_change = sim.modify_dyad("Kit", "Maeve", -1, "awkwardness")
            log.append(dyad_change)
    elif observer == "Rielle":
        # More likely to be awkward
        if random.random() < 0.6:
            dyad_change = sim.modify_dyad("Kit", "Rielle", -1, "awkwardness")
            log.append(dyad_change)
        else:
            dyad_change = sim.modify_dyad("Kit", "Rielle", 1, "surprisingly supportive")
            log.append(dyad_change)

    # Kit-Yuul dyad
    kit_yuul_change = sim.modify_dyad("Kit", "Yuul", 0.5, "secret becoming real")
    log.append(kit_yuul_change)

    return {"chaos": chaos_change, "log": log}


def event_7_kit_overextends(sim):
    """Card 7: Kit Overextends"""
    log = []
    chaos_change = 1

    kit = sim.get_character("Kit")

    # Severity depends on Kit's current state
    if kit and kit.c_self < 5:
        kit_change = sim.modify_character_c_self("Kit", -2, "overextends at breaking point")
        log.append({"warning": "⚠ BREAKING POINT - Kit is overextended"})

        # May trigger Maeve intervention
        if random.random() < 0.6:
            maeve_change = sim.modify_character_c_self("Maeve", -0.5, "intervenes for Kit")
            dyad_change = sim.modify_dyad("Kit", "Maeve", 1, "Maeve intervenes")
            log.append({"note": "→ Maeve intervenes"})
            log.append(maeve_change)
            log.append(dyad_change)
    else:
        kit_change = sim.modify_character_c_self("Kit", -1, "overextends")

    log.insert(0, kit_change)

    # May snap at Maeve
    if random.random() < 0.4:
        dyad_change = sim.modify_dyad("Kit", "Maeve", -0.5, "Kit snaps at Maeve")
        log.append(dyad_change)

    # Doesn't blame Yuul
    log.append({"note": "→ Kit doesn't blame Yuul"})

    return {"chaos": chaos_change, "log": log}


def event_8_trine_ritual(sim):
    """Card 8: Trine Ritual Required"""
    log = []

    # Calculate Trine health
    trine_dyads = [
        sim.get_dyad("Maeve", "Yuul"),
        sim.get_dyad("Maeve", "Rielle"),
        sim.get_dyad("Yuul", "Rielle")
    ]

    trine_avg = sum(d.c_dyad for d in trine_dyads if d) / len(trine_dyads)

    # Success chance
    success_chance = trine_avg * 0.15
    success = random.random() < success_chance

    log.append({"note": f"WITCH TRINE RITUAL (avg dyad: {trine_avg:.1f}, chance: {success_chance:.0%})"})

    if trine_avg < 6 or not success:
        # Failure
        chaos_change = 6
        log.append({"warning": "✗ TRINE RITUAL FAILS"})

        for char_name in ["Maeve", "Yuul", "Rielle"]:
            change = sim.modify_character_c_self(char_name, -1, "Trine ritual failure")
            log.append(change)

        for dyad in trine_dyads:
            if dyad:
                change = sim.modify_dyad(dyad.char_a, dyad.char_b, -2, "Trine ritual failure")
                log.append(change)
    else:
        # Success
        chaos_change = 0
        log.append({"note": "✓ TRINE RITUAL SUCCEEDS"})

        for char_name in ["Maeve", "Yuul", "Rielle"]:
            change = sim.modify_character_c_self(char_name, 1, "Trine ritual success")
            log.append(change)

        for dyad in trine_dyads:
            if dyad:
                change = sim.modify_dyad(dyad.char_a, dyad.char_b, 1, "Trine ritual success")
                log.append(change)

    return {"chaos": chaos_change, "log": log}


def event_9_rielle_questions_maeve(sim):
    """Card 9: Rielle Questions Maeve's Choice"""
    log = []

    maeve = sim.get_character("Maeve")

    # Maeve's response depends on her coherence
    if maeve and maeve.c_self >= 5:
        # She listens
        chaos_change = -1
        log.append({"note": "→ Maeve listens to Rielle's concerns"})

        maeve_change = sim.modify_character_c_self("Maeve", 0.5, "reflects on choice")
        yuul_change = sim.modify_character_c_self("Yuul", 0.5, "benefits from intervention")

        # Initial tension, then resolution
        dyad_change_1 = sim.modify_dyad("Maeve", "Rielle", -0.5, "initial tension")
        dyad_change_2 = sim.modify_dyad("Maeve", "Rielle", 1, "resolved through listening")
        dyad_change_3 = sim.modify_dyad("Maeve", "Yuul", 1, "Maeve course-corrects")

        log.extend([maeve_change, yuul_change, dyad_change_1, dyad_change_2, dyad_change_3])
    else:
        # She's defensive
        chaos_change = 0
        log.append({"note": "→ Maeve is defensive, doesn't listen"})

        dyad_change = sim.modify_dyad("Maeve", "Rielle", -0.5, "tension unresolved")
        log.append(dyad_change)

    return {"chaos": chaos_change, "log": log}


def event_10_yuuls_last_prophecy(sim):
    """Card 10: Yuul's Last Prophecy"""
    log = []

    yuul = sim.get_character("Yuul")
    yuul_change = sim.modify_character_c_self("Yuul", -1, "delivers prophecy")
    log.append(yuul_change)

    # Clarity depends on Yuul's coherence
    if yuul and yuul.c_self >= 4:
        # Delivered clearly, more likely believed
        chaos_change = 0
        log.append({"note": "→ Prophecy delivered clearly"})

        # Others listen and act
        for char_name in ["Maeve", "Kit", "Rielle"]:
            if random.random() < 0.7:
                change = sim.modify_character_c_self(char_name, 0.5, "heeds prophecy")
                dyad_change = sim.modify_dyad("Yuul", char_name, 1, "believed")
                log.extend([change, dyad_change])
    else:
        # Word salad, likely dismissed
        chaos_change = 3
        log.append({"note": "→ Prophecy comes out as word salad"})

        for char_name in ["Maeve", "Kit", "Rielle"]:
            if random.random() < 0.6:
                dyad_change = sim.modify_dyad("Yuul", char_name, -1, "dismissed")
                log.append(dyad_change)

    return {"chaos": chaos_change, "log": log}


def event_11_mission_goes_wrong(sim):
    """Card 11: Mission Goes Wrong"""
    log = []
    chaos_change = 2

    # Randomly pick decision maker
    decision_maker = random.choice(["Maeve", "Kit", "Rielle"])
    log.append({"note": f"→ {decision_maker} makes the critical call"})

    # Someone gets protected, someone gets abandoned
    all_chars = ["Maeve", "Kit", "Rielle", "Yuul"]
    protected = random.choice([c for c in all_chars if c != decision_maker])
    abandoned = random.choice([c for c in all_chars if c != decision_maker and c != protected])

    decision_change = sim.modify_character_c_self(decision_maker, -1, "burden of decision")
    abandoned_change = sim.modify_character_c_self(abandoned, -1, "abandoned in crisis")

    log.append(decision_change)
    log.append({"note": f"→ {protected} protected, {abandoned} abandoned"})
    log.append(abandoned_change)

    # Dyad impacts
    dyad_positive = sim.modify_dyad(decision_maker, protected, 1, "protected in crisis")
    dyad_negative = sim.modify_dyad(decision_maker, abandoned, -2, "abandoned in crisis")

    log.extend([dyad_positive, dyad_negative])

    return {"chaos": chaos_change, "log": log}


def event_12_dce_investigation(sim):
    """Card 12: DCE Investigation"""
    log = []
    chaos_change = 4

    log.append({"warning": "⚠ DCE INVESTIGATION - External threat"})

    # Everyone suffers
    yuul_change = sim.modify_character_c_self("Yuul", -1, "paranoia justified")
    kit_change = sim.modify_character_c_self("Kit", -1, "protective stress")

    log.extend([yuul_change, kit_change])

    for char_name in ["Maeve", "Rielle"]:
        change = sim.modify_character_c_self(char_name, -0.5, "external pressure")
        log.append(change)

    # May unite or fracture
    unite = random.random() < 0.5

    if unite:
        log.append({"note": "→ H11 unites against external threat"})
        for dyad in sim.relationships:
            change = sim.modify_dyad(dyad.char_a, dyad.char_b, 0.5, "unite against DCE")
            log.append(change)
    else:
        log.append({"note": "→ Internal blame fractures the group"})
        # Random dyad takes a hit
        dyad = random.choice(sim.relationships)
        change = sim.modify_dyad(dyad.char_a, dyad.char_b, -0.5, "blame under pressure")
        log.append(change)

    return {"chaos": chaos_change, "log": log}


def event_13_thing_theyve_been_avoiding(sim):
    """Card 13: The Thing They've Been Avoiding"""
    log = []

    # Pick two characters for the conversation
    all_chars = ["Maeve", "Kit", "Rielle", "Yuul"]
    char_a, char_b = random.sample(all_chars, 2)

    log.append({"note": f"→ {char_a} and {char_b} have THE CONVERSATION"})

    # Success depends on both having c_self > 5
    char_a_obj = sim.get_character(char_a)
    char_b_obj = sim.get_character(char_b)

    both_stable = (char_a_obj and char_a_obj.c_self > 5) and (char_b_obj and char_b_obj.c_self > 5)

    if both_stable:
        # Resolved
        chaos_change = 0
        log.append({"note": "✓ Conversation resolves the tension"})

        change_a = sim.modify_character_c_self(char_a, 1, "resolved tension")
        change_b = sim.modify_character_c_self(char_b, 1, "resolved tension")
        dyad_change = sim.modify_dyad(char_a, char_b, 2, "breakthrough conversation")

        log.extend([change_a, change_b, dyad_change])
    else:
        # Rupture
        chaos_change = 3
        log.append({"warning": "✗ Conversation leads to RUPTURE"})

        change_a = sim.modify_character_c_self(char_a, -1, "conversation rupture")
        change_b = sim.modify_character_c_self(char_b, -1, "conversation rupture")
        dyad_change = sim.modify_dyad(char_a, char_b, -3, "rupture")

        log.extend([change_a, change_b, dyad_change])

    return {"chaos": chaos_change, "log": log}


def event_14_bonfire_night(sim):
    """Card 14: Bonfire Night (rare peace)"""
    log = []

    # Calculate group average c_self
    avg_c_self = sum(c.c_self for c in sim.characters.values()) / len(sim.characters)

    if avg_c_self <= 5:
        # Group too damaged for this
        log.append({"note": "✗ Group too damaged for bonfire night (avg: {:.1f})".format(avg_c_self)})
        return {"chaos": 0, "log": log}

    chaos_change = -2
    log.append({"note": f"✓ BONFIRE NIGHT - Rare moment of peace (avg c_self: {avg_c_self:.1f})"})

    # Check if chaos is low for doubled effect
    effect_multiplier = 2 if sim.chaos < 10 else 1

    # Everyone benefits
    for char_name, char in sim.characters.items():
        bonus = random.uniform(0.5, 1.0) * effect_multiplier
        change = sim.modify_character_c_self(char_name, bonus, "bonfire night")
        log.append(change)

    # All dyads improve
    for dyad in sim.relationships:
        bonus = 0.5 * effect_multiplier
        change = sim.modify_dyad(dyad.char_a, dyad.char_b, bonus, "bonfire night")
        log.append(change)

    if effect_multiplier > 1:
        log.append({"note": "⚡ Effect doubled due to low chaos!"})

    return {"chaos": chaos_change, "log": log}


def event_15_kit_confesses_not_to_yuul(sim):
    """Card 15: Kit Confesses (Not to Yuul)"""
    log = []
    chaos_change = 1

    # Pick confidant
    confidant = random.choice(["Maeve", "Rielle"])
    log.append({"note": f"→ Kit confesses his feelings to {confidant}"})

    # Kit's reaction
    if random.random() < 0.5:
        kit_change = sim.modify_character_c_self("Kit", 0.5, "relief from confession")
        log.append({"note": "→ Kit feels relief"})
    else:
        kit_change = sim.modify_character_c_self("Kit", -0.5, "shame from confession")
        log.append({"note": "→ Kit feels shame"})

    log.append(kit_change)

    # Confidant bears the burden
    confidant_change = sim.modify_character_c_self(confidant, -0.5, "burden of Kit's secret")
    log.append(confidant_change)

    # Dyad reaction
    if confidant == "Maeve":
        # More likely supportive
        if random.random() < 0.7:
            dyad_change = sim.modify_dyad("Kit", "Maeve", 1, "Maeve forms support network")
            log.append({"note": "→ Maeve offers strong support"})
        else:
            dyad_change = sim.modify_dyad("Kit", "Maeve", -1, "awkwardness")
            log.append({"note": "→ Things get awkward"})
        log.append(dyad_change)
    elif confidant == "Rielle":
        # Awkward but accepted
        dyad_change = sim.modify_dyad("Kit", "Rielle", 0.5, "awkward but accepted")
        log.append({"note": "→ Rielle accepts awkwardly"})
        log.append(dyad_change)

    # Yuul doesn't know yet
    log.append({"note": "→ Yuul doesn't know yet"})

    return {"chaos": chaos_change, "log": log}


def event_16_maeve_reaches_out(sim):
    """Card 16: Maeve Reaches Out to Yuul"""
    log = []

    maeve = sim.get_character("Maeve")
    yuul = sim.get_character("Yuul")

    # Effectiveness depends on Maeve having capacity to give
    if maeve and maeve.c_self > 6:
        chaos_change = -1
        log.append({"note": "→ Maeve reaches out with genuine care"})

        # Strong effect
        yuul_bonus = 2 if yuul and yuul.c_self >= 2 else 1
        maeve_change = sim.modify_character_c_self("Maeve", 1, "doing the right thing")
        yuul_change = sim.modify_character_c_self("Yuul", yuul_bonus, "feels truly seen by Maeve")
        dyad_change = sim.modify_dyad("Maeve", "Yuul", 2, "breakthrough moment")

        log.extend([maeve_change, yuul_change, dyad_change])

        if yuul and yuul.c_self < 2:
            log.append({"warning": "⚠ May have come too late for Yuul"})
    else:
        chaos_change = 0
        log.append({"note": "→ Maeve tries but lacks capacity"})

        # Weak effect
        maeve_change = sim.modify_character_c_self("Maeve", -0.5, "tries but can't give enough")
        yuul_change = sim.modify_character_c_self("Yuul", 0.5, "appreciates effort")
        dyad_change = sim.modify_dyad("Maeve", "Yuul", 0.5, "appreciated attempt")

        log.extend([maeve_change, yuul_change, dyad_change])

    return {"chaos": chaos_change, "log": log}


def event_17_yuul_warns_redchurch(sim):
    """Card 17: Yuul Warns About Redchurch"""
    log = []
    chaos_change = 4  # Prophetic weight

    yuul_change = sim.modify_character_c_self("Yuul", -1, "delivers Redchurch prophecy")
    log.append(yuul_change)

    log.append({"warning": "⚠ REDCHURCH WARNING - Prophetic weight"})

    # Is she believed?
    yuul = sim.get_character("Yuul")
    maeve = sim.get_character("Maeve")

    # More likely believed if this is early or if Yuul is coherent
    believed = (yuul and yuul.c_self >= 4) or random.random() < 0.4

    if believed:
        log.append({"note": "✓ WARNING BELIEVED - Action can be taken"})

        maeve_change = sim.modify_character_c_self("Maeve", 1, "can prevent disaster")
        dyad_change = sim.modify_dyad("Maeve", "Yuul", 2, "believed and acted upon")

        log.extend([maeve_change, dyad_change])
    else:
        log.append({"warning": "✗ WARNING DISMISSED as paranoia"})

        maeve_change = sim.modify_character_c_self("Maeve", -1, "burden of dismissed prophecy")
        dyad_change = sim.modify_dyad("Maeve", "Yuul", -3, "not believed")

        log.extend([maeve_change, dyad_change])

    return {"chaos": chaos_change, "log": log}


def event_18_kit_makes_promise(sim):
    """Card 18: Kit Makes a Promise"""
    log = []
    chaos_change = 2  # Dramatic setup

    # Assume promise is to/about Yuul
    log.append({"note": "→ Kit makes a solemn promise about Yuul"})

    kit_change = sim.modify_character_c_self("Kit", 2, "finds purpose in promise")
    yuul_change = sim.modify_character_c_self("Yuul", 1, "feels hope from Kit's promise")
    dyad_change = sim.modify_dyad("Kit", "Yuul", 1, "promise deepens bond")

    log.extend([kit_change, yuul_change, dyad_change])

    # Dramatic irony check
    if sim.chaos > 15:
        log.append({"warning": "⚠⚠⚠ DRAMATIC IRONY FLAG - Promise becomes tragic setup"})
        log.append({"note": "The players know this promise may be impossible to keep..."})

    return {"chaos": chaos_change, "log": log}


def event_19_rielles_impulse(sim):
    """Card 19: Rielle's Impulse (unpredictable)"""
    log = []

    rielle = sim.get_character("Rielle")

    # 50/50 helpful or harmful, but more likely helpful if Rielle is stable
    if rielle and rielle.c_self > 7:
        helpful_chance = 0.7
    else:
        helpful_chance = 0.5

    helpful = random.random() < helpful_chance

    if helpful:
        chaos_change = -2
        log.append({"note": "✓ Rielle's impulse is HELPFUL"})

        rielle_change = sim.modify_character_c_self("Rielle", 1, "good impulse pays off")
        log.append(rielle_change)

        # Random positive dyad change
        other_char = random.choice(["Maeve", "Kit", "Yuul"])
        other_change = sim.modify_character_c_self(other_char, 1, f"helped by Rielle's impulse")
        dyad_change = sim.modify_dyad("Rielle", other_char, 1, "helpful impulse")

        log.extend([other_change, dyad_change])
    else:
        chaos_change = 3
        log.append({"warning": "✗ Rielle's impulse is HARMFUL"})

        rielle_change = sim.modify_character_c_self("Rielle", -0.5, "impulse backfires")
        log.append(rielle_change)

        # Random negative impacts
        affected = random.sample(["Maeve", "Kit", "Yuul"], 2)
        for char_name in affected:
            change = sim.modify_character_c_self(char_name, -0.5, "caught in Rielle's chaos")
            dyad_change = sim.modify_dyad("Rielle", char_name, -1, "harmful impulse")
            log.extend([change, dyad_change])

    return {"chaos": chaos_change, "log": log}


def event_20_grace_moment(sim):
    """Card 20: Grace Moment (pure stabilization)"""
    log = []
    chaos_change = -1

    # Pick two random characters
    all_chars = list(sim.characters.keys())
    char_a, char_b = random.sample(all_chars, 2)

    log.append({"note": f"✨ GRACE MOMENT between {char_a} and {char_b}"})

    # Get their coherence to see if they need it most
    char_a_obj = sim.get_character(char_a)
    char_b_obj = sim.get_character(char_b)

    both_struggling = (char_a_obj and char_a_obj.c_self < 5) and (char_b_obj and char_b_obj.c_self < 5)

    effect_multiplier = 2 if both_struggling else 1

    change_a = sim.modify_character_c_self(char_a, 0.5 * effect_multiplier, "grace moment")
    change_b = sim.modify_character_c_self(char_b, 0.5 * effect_multiplier, "grace moment")
    dyad_change = sim.modify_dyad(char_a, char_b, 1 * effect_multiplier, "grace moment")

    log.extend([change_a, change_b, dyad_change])

    if both_struggling:
        log.append({"note": "⚡ Effect doubled - both needed it most"})

    return {"chaos": chaos_change, "log": log}


# Create the event deck
def create_event_deck() -> List[Event]:
    """Create all 20 event cards"""
    return [
        Event(1, "Yuul Has a Vision - Horror", "yuul_vulnerability",
              "Yuul sees something terrible. Tries to tell Maeve. Maeve doesn't want to hear it.",
              2, event_1_yuul_vision_horror),

        Event(2, "Prophetic Isolation", "yuul_vulnerability",
              "Someone suggests isolating Yuul for her own good. Kit objects but is powerless.",
              0, event_2_prophetic_isolation),

        Event(3, "Yuul Speaks in Reversals", "yuul_vulnerability",
              "Yuul's speech becomes fragmented. Some can still reach her, others pull away.",
              2, event_3_yuul_speaks_reversals),

        Event(4, "The Mirror Incident", "yuul_vulnerability",
              "Someone finds Yuul having a reality-breaking experience. Reality breach.",
              5, event_4_mirror_incident),

        Event(5, "Kit Tries to Ground Yuul", "kit_feelings",
              "Kit attempts to stabilize Yuul. Success depends on his own coherence.",
              -1, event_5_kit_grounds_yuul),

        Event(6, "Someone Notices", "kit_feelings",
              "Someone realizes Kit has feelings for Yuul. Reactions vary.",
              2, event_6_someone_notices),

        Event(7, "Kit Overextends", "kit_feelings",
              "Kit pushes himself too hard caring for others. May reach breaking point.",
              1, event_7_kit_overextends),

        Event(8, "Trine Ritual Required", "trine",
              "The Witch Trine must perform a ritual. Success depends on their collective bond strength.",
              0, event_8_trine_ritual),

        Event(9, "Rielle Questions Maeve's Choice", "trine",
              "Rielle confronts Maeve about her handling of Yuul. Will Maeve listen?",
              0, event_9_rielle_questions_maeve),

        Event(10, "Yuul's Last Prophecy", "trine",
              "Yuul delivers a crucial prophecy. Will it be coherent enough to believe?",
              0, event_10_yuuls_last_prophecy),

        Event(11, "Mission Goes Wrong", "external_pressure",
              "A mission fails. Someone must make a hard choice about who to protect.",
              2, event_11_mission_goes_wrong),

        Event(12, "DCE Investigation", "external_pressure",
              "External authorities investigate H11. Everyone suffers from the pressure.",
              4, event_12_dce_investigation),

        Event(13, "The Thing They've Been Avoiding", "external_pressure",
              "Two characters must finally have THE conversation. Make or break.",
              0, event_13_thing_theyve_been_avoiding),

        Event(14, "Bonfire Night", "salvation",
              "A rare moment of peace and connection. Only possible if group is stable enough.",
              -2, event_14_bonfire_night),

        Event(15, "Kit Confesses (Not to Yuul)", "salvation",
              "Kit tells someone else about his feelings. They become his confidant.",
              1, event_15_kit_confesses_not_to_yuul),

        Event(16, "Maeve Reaches Out to Yuul", "salvation",
              "Maeve makes a genuine effort to connect with Yuul. More effective if Maeve is stable.",
              0, event_16_maeve_reaches_out),

        Event(17, "Yuul Warns About Redchurch", "wild_card",
              "Yuul prophecies about Redchurch. Will anyone believe her?",
              4, event_17_yuul_warns_redchurch),

        Event(18, "Kit Makes a Promise", "wild_card",
              "Kit makes a solemn promise about protecting Yuul. Dramatic setup.",
              2, event_18_kit_makes_promise),

        Event(19, "Rielle's Impulse", "wild_card",
              "Rielle acts on impulse. Could be brilliant or catastrophic.",
              0, event_19_rielles_impulse),

        Event(20, "Grace Moment", "wild_card",
              "Pure stabilization. Two characters share an unexpected moment of grace.",
              -1, event_20_grace_moment),
    ]
