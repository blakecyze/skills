# Celebration scenarios

## Completion ritual

For publishing, sending, or launching, anticipation can acknowledge the user's action while the real operation is pending. The payoff belongs after confirmation. If work fails, move to a useful recovery state without a success sound or cheerful leftover animation.

For long-running jobs, let users leave. A completed job can present a result on return; do not force replay of an old ceremony. In batch work, aggregate feedback around the user's batch outcome rather than celebrating every item.

## Character reaction

Use an existing character's reaction vocabulary. A short nod can mark ordinary progress; a distinctive transformation can mark a rare achievement. Provide a meaningful still pose. The character may encourage another attempt, but should not act wounded when someone skips or leaves.

## Confetti

Use a bounded burst with a clear end. Keep the success message readable throughout. Avoid flashing or screen shake. Under reduced motion, use the static result or a restrained highlight if appropriate. Stop rendering and release resources after dismissal, navigation, or completion.

## Replay decisions

| Case | Decision to make |
|---|---|
| Event delivered twice | Recognise the same completion; avoid duplicate payoff |
| View remounts | Persist the real result; replay only if the product calls for it |
| Several milestones crossed at once | Prefer one highest-relevance acknowledgement |
| Success arrives after navigation | Update the result without spawning decoration in an unrelated view |
| User requests replay | Replay the effect without repeating the business action |
| Result later rolls back | Present the corrected state and recovery; do not leave success copy behind |

Test only cases the implementation can encounter. Apply suppression to the celebration, never to the underlying result or its accessible status.
