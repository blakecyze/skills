# Habit mechanics

## Streaks

Choose a cadence that matches valuable practice. Show what qualifies and which period is being counted. Decide how grace, pause, and recovery work before writing motivational copy.

For time-based systems, specify the source of time, relevant timezone, day/week boundary, travel changes, offline completion, and duplicate sync. Preserve prior progress during migrations unless the brief explicitly changes the rules. Do not implement new policy by accident through a convenient date function.

For an irregular activity, a weekly target or cumulative progress may represent success more honestly than consecutive days. This is a design choice to evaluate against the user's brief, not an automatic replacement.

## XP, quests, and leaderboards

Name the useful action behind each reward. Check whether the cheapest way to earn points also achieves the user's goal. If repetition can farm points without useful progress, reconsider eligibility or make the metric's limited meaning explicit.

Keep one primary progress story legible. Explain ranking and resets; allow users to hide optional competition. Do not frame a rank drop as failure when someone met their own goal. Avoid piling several unrelated currencies onto a simple activity.

## Lives and scarcity

Establish the purpose of error costs: pacing, challenge, or a commercial limit. In learning tasks, inspect whether scarcity discourages attempts that the product ought to encourage. Make remaining capacity, refill rules, and available practice or recovery paths clear. Do not conceal commercial limits beneath a character's disappointment.

## Example checks

| Scenario | Question |
|---|---|
| Same lesson syncs twice | Does it count once under the chosen eligibility rule? |
| Work finishes across midnight | Which documented completion time determines credit? |
| User takes a planned break | Can they understand and control the consequence? |
| Goal met but ranking falls | Does the UI still acknowledge the user's useful progress? |
| Reminder disabled | Does the activity remain available without repeated pressure? |
| Service outage | Is user progress repaired according to an explicit policy? |

## Evidence boundary

[Duolingo's account of its streak experiments](https://blog.duolingo.com/how-duolingo-streak-builds-habit/) describes changes to streak celebrations and recovery. It is a first-party case study from one product. Its engagement results do not establish effects on learning or predict a new product's outcome. The choices above are design and implementation heuristics, not claimed experimental findings.
