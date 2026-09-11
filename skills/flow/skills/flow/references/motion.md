# Motion refinement

Give motion a job: acknowledge input, connect states, explain spatial change, or express a fitting moment. Judge frequency, travel, duration, and competing activity together. Frequent interactions usually benefit from less movement; keyboard input does not automatically forbid animation.

Use the existing motion language and implementation facilities. A transition often suffices for state changes; gestures may need velocity-preserving springs, while authored sequences may need keyframes. Avoid a new dependency for a small effect.

Choose timing by distance, purpose, and observed responsiveness. Existing tokens are useful starting points, not proof of quality. Do not fabricate measurements or treat a chosen curve as an empirical fact. Avoid forcing every entrance, exit, or group into the same easing or stagger.

Retarget or cancel cleanly on rapid input. Keep controls available while decoration runs. Prefer transform and opacity where appropriate, but test the actual implementation; property names alone do not prove compositor execution or acceptable performance. Layout animation can be justified when it explains a real layout change.

Respect reduced motion with a meaningful static or gentler result. Essential state must survive with animation removed. Hover enhancements need equivalent touch and keyboard behaviour. Stop unnecessary work when hidden, dismissed, or superseded.

Inspect the result at normal speed, with rapid retriggering and interruption. Slower playback can reveal discontinuities but does not establish natural timing. Report source-only review separately from observed runtime behaviour.
