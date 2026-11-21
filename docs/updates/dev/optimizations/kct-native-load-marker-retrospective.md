# KCT Native restoration: investigation postmortem

This note records both the technical cause indicated by the successful fix and the investigation mistakes that delayed it. It is intended as a debugging model for future stateful runtime issues, not as a recipe limited to KCT.

## Outcome and confidence

On the tested Native save, troop trees updated after load and the user reported stable 60 FPS. The change immediately preceding that result replaced `grc_cavalry` with `grc_archers` as the completion marker used by the poll and the restore routine. The full restore routine already ran migrations and wrote the marker at its end; the interval-zero trigger already had a three-operation hot path.

The best-supported cause is a stale completion marker. The previous gate treated `grc_cavalry` as proof that restoration had completed. A save that retained that value could therefore skip the restore even though the troop data was still wrong. Changing the expected completion value made that old state eligible for restoration; the successful run then wrote `grc_archers`, after which subsequent polls exited at the comparison.

This explanation fits the one-change runtime result and code path. We did not directly log or inspect the class stored in the user’s save, so “the save retained `grc_cavalry`” remains a strong inference, not an observed value. The runtime confirmation covers the save and session the user tested; it does not by itself prove every save version, all three troop families, or repeated load cycles.

## What made the investigation take too long

### We treated nearby success signals as proof of the desired result

The user repeatedly distinguished “configured nodes” or a setup message from troops actually receiving their saved tree data. Those are separate stages:

1. The template/tree data exists.
2. The Native load poll runs.
3. Its gate allows the restore call.
4. The restore copies data to each intended real troop.
5. The troop records visible to the game are correct.

Messages at stages 1 or 2 cannot establish stages 3–5. We should have named these boundaries at the start and treated the visible troop state as the acceptance criterion. The user had already supplied the decisive symptom; repeatedly asking for more generic confirmation added friction without narrowing the cause.

### We asserted lifecycle behavior instead of checking it

The Native poll used a non-hero troop’s class as a completion marker. We assumed Native reset that runtime class on every save load. That assumption became embedded in comments and the trigger gate, but we had no log showing the class value before the gate. Since the completion marker participates in save-backed game state, it was unsafe to infer its reset behavior from the troop being non-hero or from the marker’s intended role.

The correct question was not “should Native reset this?” but “what exact value does this save present at the gate, and what branch does that value take?” We eventually changed the marker token; the same save then restored correctly. That was a much stronger experiment than reasoning from the comment, but a gate diagnostic would have exposed the stale-state hypothesis earlier.

### We debugged the restore body before proving the call path

Several changes targeted troop copying, default data, or custom factions while the Native trigger itself might not be reaching the restore routine. That mixed two independent questions:

- **Reachability:** Did the Native trigger fire, pass its completion gate, and call the script?
- **Correctness:** Once called, did the script restore the correct troops and leave valid data?

Changes to Calradian/Falcon initialization could only answer the second question if the first was already established. We needed one diagnostic at the gate (marker value and decision), one at restore entry (force flag and party), and a final per-category count/result. A “configured” message from another path was not a substitute.

### We did not treat frame cost as a separate invariant

An interval-zero trigger can execute every rendered frame. Putting broad troop scans, record copies, or migrations directly on that recurring path can make a correct fix unacceptably expensive. Earlier performance regressions made the user’s constraint clear: a solution that restores troops but damages FPS is a failed solution.

The eventual design preserves an O(1) recurring check and runs the heavy restore only when the completion marker says it is needed. The marker is written after restoration and migrations finish. Correctness and performance therefore have separate checks: the expected troops must update, and subsequent frames must stop repeating the expensive work. The reported 60 FPS is important runtime evidence for the tested save, not a guarantee for every save or machine.

### We made the user carry too much of the diagnosis

The user had to repeat in-game tests after changes that were described as ready without proof that the relevant Native path had run. They also had to correct assumptions about what the messages meant and who controlled the PC. A future agent should not use screenshots or ask the user to repeat the same action when a targeted source/build inspection can answer the next question. The user controls the game; ask for a short runtime check only after producing a specific compiled build and state exactly what result distinguishes the remaining hypotheses.

## A stronger process for the next stateful bug

### 1. Define the acceptance result in user-visible terms

Write down the expected state and the observable failure in one sentence. Here it would have been: “After loading this save in Native, the Falcon and Calradian real troops must match their configured trees immediately, and the map must remain at the user’s stable FPS.” Keep setup messages, internal calls, and the final state as separate facts.

### 2. Draw the real execution path and mark every gate

Trace from the actual event or polling loop through conditions and early exits to the final state write. For each gate, record its source state, initial value, persistence, and who writes it. Do this separately for Native and WSE; WSE has a save-loaded callback, while Native in this project relies on a simple-trigger poll.

For this bug the decisive path was:

```text
Native interval-zero compatibility trigger
  -> read trp_cstm_load_check class
  -> compare with completion marker
  -> call forced KCT restore when not complete
  -> restore generic CSTM and preset troops; run repairs/migrations
  -> write completion marker last
  -> later frames stop at the cheap comparison
```

This diagram immediately highlights two independent failure modes: a stale marker can block the call, while a faulty copy routine can run successfully and still leave troops wrong.

### 3. Instrument the branch boundary, not just the feature

Before another speculative fix, make the relevant boundary report enough to decide the next step:

- Trigger: sentinel value and whether the gate allows the call.
- Restore entry: Native/WSE caller, party, force flag, and marker value.
- Restore body: counts for generic CSTM, Falcon, and Calradian troops visited and actually copied.
- Completion: final counts and marker written.

Use messages/logs that correspond to those boundaries. Keep per-frame diagnostics quiet after the first useful event. If the trigger is gated off, a message inside the restore script cannot diagnose why; place the diagnostic before that gate.

### 4. Form a falsifiable hypothesis and change one thing

State what observation the hypothesis predicts. For example: “If a saved marker is blocking the trigger, changing only the completion token should make this same save enter the restore path.” Keep the save, module output, in-game location, and action fixed. Do not bundle unrelated copy logic, timing, marker semantics, and performance changes into one test.

If the result contradicts the prediction, update the model before making another code edit. Do not repeat an unchanged test or claim completion because the compile succeeded.

### 5. Verify both the authored source and the installed build

Compile after source changes. Inspect the generated trigger count, compatibility slot, interval, and operation count; ensure the game’s configured module directory received the output. A valid source diff does not prove the installed module contains it, and a successful compile does not prove the runtime path executed.

### 6. Test correctness, repeat behavior, and cost separately

First verify the real troops visibly match the configured tree. Then verify the completion marker prevents the expensive path from running again. Finally compare FPS under the same save and scene. When available, use runtime counters/logs to prove call count; do not infer “once” solely from a plausible code shape.

### 7. Keep compatibility and ownership explicit

Preserve dummy trigger entries and generated counts unless a deliberate save-compatibility change is intended. Keep Native and WSE code paths distinct and commit boundaries clear. Do not operate the user’s PC/game when they have said they control it. Present one specific, low-effort runtime check only after the build and diagnostics are ready.

## KCT-specific facts to retain

- The Native poll occupies an existing compatibility slot; the compiled module must keep 140 simple triggers.
- The Native trigger hot path has three operations and uses an interval of zero.
- `script_kct_restore_troops_after_load` is shared restore logic; the Native poll passes `force_restore=1`.
- The successful tested change uses `grc_archers` as the new completion marker and writes it after restoration/migrations.
- Do not state that the exact old marker was observed in the save; it was inferred from the controlled change and runtime result.

## Relevant files

- `modmerger/mods/kingdom_custom_troop_tree_creator/kingdom_custom_troop_tree_creator_simple_triggers.py` — Native marker poll.
- `modmerger/mods/kingdom_custom_troop_tree_creator/kct_scripts/load_restore.py` — restore path, gates, diagnostics, and final marker writes.
- `source/simple_triggers/dummy_empty_triggers.py` — compatibility slot hosting the Native poll.
- `source/module_simple_triggers.py` — preserves historical trigger count and ordering.
