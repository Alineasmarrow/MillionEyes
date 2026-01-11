# Guide: Adding Farris and Daniel to Event Effects

## Problem
Farris and Daniel rarely take damage because they're not included in most event effects. They end up nearly untouchable while the core crew dissolves.

## Solution
Add Farris and Daniel to events where it narratively makes sense:
- **Farris**: Household/crew/group events (he's part of the family)
- **Daniel**: DCE/institutional/pressure events (he's the liaison)

## Code Pattern

### Adding Farris to Group Events
```python
# After existing crew changes (Yuul, Maeve, Kit, Rielle):
farris = sim.get_character("Farris")
if farris and not farris.is_dead:
    farris_change = sim.modify_character_c_self("Farris", [SAME_DELTA], [SAME_REASON])
    log.append(farris_change)
```

### Adding Daniel to DCE/Pressure Events
```python
# After existing character changes:
daniel = sim.get_character("Daniel")
if daniel and not daniel.is_dead:
    daniel_change = sim.modify_character_c_self("Daniel", [PRESSURE_DELTA], "institutional pressure")
    log.append(daniel_change)
```

## Events That Need Farris

### Act 1 (Household/Crew)
- `bonfire_night` - +1.0 "warmth and belonging"
- `grace_moment` - +0.5 "shared moment"
- `thing_avoided_soft` - Can be random target including Farris
- `trine_ritual_stable` - +0.5 "ritual participant"
- `trine_ritual_heavy` - -0.3 "ritual strain"
- `map_wont_stay_still` - -0.5 "paranormal disturbance"
- `yuul_forgets_date` - -0.2 "household concern"
- `quiet_town_watches` - -0.3 "external pressure"

### Act 2 (Escalation)
- `mission_wrong_harder` - -0.8 "mission disaster"
- `kit_panic_attack` - -0.5 "witness to crisis"
- `maeve_voice_slips` - -0.5 "Maeve's instability affects household"
- `prophetic_collapse` - -1.0 "Yuul's breakdown traumatizes everyone"
- `something_breaks` - -0.5 "ominous household event"
- `kettle_moment` - +0.5 "domestic normalcy"
- `trine_shatters` - -1.5 "major fracture affects whole household"

### Act 3 (Crisis)
- `first_warning_returns` - -0.8 "group threat"
- `photo_album_memory` - +0.5 "shared memory"
- `coherence_whiplash` - -1.0 "field disturbance affects everyone"
- `house_that_hears` - -1.0 "Sanctuary compromised"

## Events That Need Daniel

### Act 1 (Institutional Pressure)
- `internal_suspicion` - -0.8 "H11 suspects something"
- `soft_surveillance` - -0.5 "DCE watching"
- `soft_betrayal_h11` - -1.0 "caught between loyalties"
- `misaligned_questions` - -0.3 "institutional friction"
- `quiet_town_watches` - -0.3 "surveillance pressure"

### Act 2 (DCE Escalation)
- `dce_warning` - -1.0 "DCE directly threatens"
- `jurisdiction_fight` - -0.8 "institutional conflict"
- `restraint_order` - -1.5 "legal pressure on Daniel"
- `someone_recognizes` - -0.5 "public exposure pressure"
- `dce_surveillance_intensifies` - -1.0 "DCE tracking intensifies"

### Act 3 (Endgame)
- `dce_restraint_order` - -2.0 "DCE endgame pressure"

## Guidelines

1. **Match the tone**: Farris/Daniel should take similar damage to others in the event
2. **Check context**: Not every event needs them (e.g., Kit-Yuul intimate moments)
3. **Always check is_dead**: Use the pattern `if farris and not farris.is_dead`
4. **Narrative sense**: Ask "Would this character realistically be affected?"

## Priority Events (High Frequency)

Update these first for maximum impact:
1. `bonfire_night` (Act 1 - group bonding)
2. `internal_suspicion` (Act 1 - Daniel's job)
3. `trine_ritual_heavy` (Act 2 - household stress)
4. `prophetic_collapse` (Act 2 - affects everyone)
5. `coherence_whiplash` (Act 3 - field event)

## Testing

After updating events, check:
- Farris and Daniel's coherence should drop at similar rates to the crew
- They should have scars by end of Act 2
- Neither should be "untouchable" in most runs
