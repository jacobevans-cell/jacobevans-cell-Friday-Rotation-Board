# Friday Rotation Board — Handoff Package v2

This supersedes the original handoff after the September 4, 2026 staffing change.

**TEMPORARY PUBLIC MODE (Sep 4, 2026):** The site is locked to Friday-off requests only. Rotation, assignments, workload totals, training labels, and calendar views remain in source but are intentionally hidden from staff until availability requests are processed and a real schedule is approved.

**Current status:** the Friday Rotation Board has been rebuilt for four active Friday-duty staff and now includes a Friday-off request workflow. The unrelated volleyball site in the repository root remains untouched.

---

## 1. What changed on September 4, 2026

Two people are no longer in the active Friday-duty rotation:

- **Dorr**
- **Darien McKinley**, who was labeled **Coach** in the original page/data

The active Friday rotation is now:

- **Lingam**
- **Evans**
- **Latoya**
- **Meda**

The schedule was not merely edited by replacing names one-for-one. All future assignments from **September 4, 2026 forward** were rebalanced around the four remaining staff.

August history is preserved. Historical appearances by `Coach` were relabeled `McKinley` for clarity; they were not erased.

---

## 2. Repo and page boundaries

| Thing | Location |
|---|---|
| GitHub repo | `https://github.com/jacobevans-cell/Sports-Calendar` |
| Working branch | `claude/interactive-website-conversion-ht86sn` |
| Friday board | `friday-schedule/index.html` |
| Handoff | `friday-schedule/HANDOFF.md` |
| Served URL after merge | `https://jacobevans-cell.github.io/Sports-Calendar/friday-schedule/` |

### Do not touch

The repository root `index.html` is the unrelated volleyball site. The Friday board remains a separate page and is not linked from the volleyball homepage unless the user explicitly asks.

---

## 3. New schedule model

The school-year date inventory is unchanged:

- **42 Fridays total**
- **36 Fridays with school**
- **6 no-school Fridays**
- **8 training Fridays**
- **2 completed Fridays**
- **26 regular Fridays**

From September 4 forward:

### Regular Fridays

- Exactly **2 of the 4 active staff** work 7:30 a.m.–1:30 p.m.
- The other two are off.

The 25 regular Fridays from September 4 forward use these pair counts:

| Pair | Count |
|---|---:|
| Lingam + Evans | 5 |
| Lingam + Latoya | 4 |
| Lingam + Meda | 4 |
| Evans + Latoya | 4 |
| Evans + Meda | 4 |
| Latoya + Meda | 4 |

This is the mathematically even pairing distribution for 25 two-person dates.

### Training Fridays

All four active staff are working.

- Two active staff cover students 7:30–11:30.
- At 11:30, one of those two stays with Cortni through dismissal and misses training.
- The other morning staff member joins training.
- The other two active staff attend training 11:30–1:30.
- The office shift 11:30–1:30 remains open for administration to assign.

Future stay-back rotation:

| Friday | Morning pair | Stays with Cortni | Joins training at 11:30 |
|---|---|---|---|
| Sep 18, 2026 | Evans + Meda | Evans | Meda |
| Oct 23, 2026 | Latoya + Lingam | Latoya | Lingam |
| Nov 13, 2026 | Evans + Latoya | Evans | Latoya |
| Jan 29, 2027 | Lingam + Meda | Lingam | Meda |
| Feb 26, 2027 | Latoya + Evans | Latoya | Evans |
| Mar 26, 2027 | Lingam + Evans | Lingam | Evans |
| Apr 23, 2027 | Meda + Lingam | Meda | Lingam |

Combined with the already-completed August 21 training, every remaining staff member ends the year with exactly two missed trainings.

---

## 4. New fairness result

The revised active-staff totals, including August history, are:

| Staff | Friday workdays | Trainings missed |
|---|---:|---:|
| Lingam | 22 | 2 |
| Evans | 22 | 2 |
| Latoya | 22 | 2 |
| Meda | 22 | 2 |

This exact 22/22/22/22 and 2/2/2/2 result is intentional.

---

## 5. Hard invariants after this rebuild

Assert all of these after any schedule change:

1. 42 Fridays total.
2. 36 with school; 6 closed.
3. 8 training; 2 completed; 26 regular.
4. `staff[]` is exactly `Lingam, Evans, Latoya, Meda`.
5. No assignment dated **2026-09-04 or later** may contain Dorr, Coach, or McKinley.
6. Every future regular Friday has exactly two active staff with `Full Day 7:30–1:30`.
7. Every future training Friday has:
   - exactly one `Full-Day Coverage — Misses Training`
   - exactly one `Morning Coverage + Training`
   - exactly two `Training 11:30–1:30`
8. Every active staff member totals exactly **22 workdays**.
9. Every active staff member totals exactly **2 missed trainings**.
10. A person's `.ics` event count must equal their summary total, so each active staff calendar export must contain **22 events**.
11. Open office shifts remain exactly the 8 training Fridays.

If approved day-off requests later force a true exception, document the exception rather than quietly falsifying the fairness totals.

---

## 6. Source data and editing rule

The page is still self-contained. The schedule lives in:

```html
<script type="application/json" id="data"> ... </script>
```

The pretty `schedule-data.json` supplied with the handoff is a readable snapshot. The page does not fetch it.

Important top-level additions:

```jsonc
{
  "staff": ["Lingam","Evans","Latoya","Meda"],
  "formerStaff": ["Dorr","McKinley"],
  "rotationEffectiveDate": "2026-09-04",
  "requestManagerEmail": "jacob.evans@explore.academy"
}
```

When changing assignments, update the inline JSON first, then regenerate the pretty snapshot.

---

## 7. Friday-off request workflow

A new **Friday availability requests** section appears above the schedule.

Staff can:

1. choose their name,
2. choose a future school Friday,
3. mark the request as either:
   - `Cannot work this Friday`
   - `Prefer this Friday off`
4. indicate whether they can swap to another Friday,
5. add an optional note,
6. see their current assignment for that date,
7. open a structured, pre-addressed Gmail message to the schedule manager,
8. or copy the structured request text.

### Why email instead of localStorage

The old handoff correctly warned that browser-only request storage would create a different truth on every device. The new request flow deliberately does **not** use localStorage for submitted requests.

Requests go to the schedule manager's school inbox. Staff must still press **Send** in Gmail; the page never sends mail silently.

The standardized subject begins:

`[Friday Off Request]`

That makes requests easy to search/filter in Gmail.

### Approval rule

Submitting a request does **not** modify the posted rotation. The schedule changes only after the request is approved and coverage is rebuilt. This prevents a request from silently creating a one-person Friday.

---

## 8. How to rebalance around requests

Treat requests as scheduling constraints.

### Hard request

`Cannot work this Friday`

- Do not assign that staff member on that date.
- If they are already assigned, move their duty to another eligible staff member and compensate elsewhere to preserve fairness as closely as possible.

### Soft request

`Prefer this Friday off`

- Honor it when possible.
- It may be overridden if student coverage or training coverage would otherwise fail.

### Rebalance priorities

In order:

1. Maintain required student coverage.
2. Never assign Dorr or McKinley on future dates.
3. Honor all approved hard requests.
4. Keep training structure valid.
5. Minimize the number of unrelated assignments changed.
6. Keep final staff workday totals as even as possible.
7. Keep missed-training totals as even as possible.
8. Avoid repeatedly pairing the same two staff when an equally valid alternative exists.

After any rebalance, rerun every invariant in §5.

---

## 9. UI behavior affected by the four-person rotation

Because the page derives views from `staff[]`, changing it to four automatically updates:

- identity chips,
- coverage grid columns,
- card coverage bars,
- workload heatmap rows,
- personal stat tiles,
- `.ics` exports,
- request-form staff choices.

The overall dashboard now shows **Active Friday staff: 4** and the fairness note reports the exact 22-workday balance.

---

## 10. Existing implementation traps still apply

Do not undo these:

1. Dash normalization before status/type lookup.
2. Local date parsing with `new Date(y, m-1, d)`, not `new Date("YYYY-MM-DD")`.
3. Coverage-bar CSS specificity using `currentColor`.
4. Explicit `[hidden]{display:none}` where custom display rules would beat the browser rule.
5. Escape data before injecting intentional HTML.
6. ICS folding by UTF-8 octets, not JavaScript character count.
7. ICS event times remain floating local times.
8. Framed viewers use the copy-text calendar fallback.
9. Textarea line-ending normalization is expected.
10. `today` comes from the browser clock at page load.

---

## 11. Verification performed for this rebuild

Data checks performed:

- original file matched the GitHub branch blob before editing,
- 42 total Friday records retained,
- type counts remain 26 regular / 8 training / 2 completed / 6 closed,
- active staff count is 4,
- no future Dorr/McKinley/Coach assignments remain,
- each active staff member computes to 22 workdays,
- each active staff member computes to 2 missed trainings,
- future regular pair counts are 5/4/4/4/4/4 as specified,
- every future training has one stay-back and one morning-plus-training role,
- JavaScript passes `node --check`.

The application logic and ICS exporter remain the same except for the new request UI and the changed schedule data.

---

## 12. Future request data is the next source of change

The schedule is balanced **before** staff availability requests.

As requests arrive, do not preserve the 22/2 totals at the expense of real campus availability. Coverage comes first. The purpose of the fairness target is to choose among valid schedules, not to force someone onto a date they cannot work.

The safest continuation prompt is:

> Here are the approved Friday-off requests. Rebalance the schedule using HANDOFF.md §8. Preserve all hard constraints, change as few unrelated assignments as possible, and report the new per-person totals plus which §5 invariants changed.

---

## 13. Current ownership boundary

This branch contains the Friday board work. Do not merge it into the volleyball homepage or alter the volleyball standings workflow unless the user separately requests that work.
