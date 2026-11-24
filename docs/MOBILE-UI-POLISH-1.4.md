# SYNTRA Social — Mobile UI Polish 1.4

## Scope
A visual refinement pass based on a real mobile screenshot supplied during review. The existing dark charcoal, gold, and purple identity is retained.

## Changes
- Replaced the story-row emoji symbols for Add story, Ideas, Creativity, Gaming, and Technology with the existing custom SVG icon renderer. The SYNTRA story marker remains the letter S.
- Increased mobile feed bottom clearance to reduce the chance that the fixed bottom navigation obscures the final post.
- Increased bottom-navigation control hit areas and standardized icon sizing.
- Made the central create-post action more visually distinct while preserving its existing button ID and handler.
- Improved mobile secondary-text contrast.
- Standardized alignment and minimum height for composer and post-action controls.

## Compatibility constraints
- No storage, feed data, routes, or action handlers were intentionally changed.
- Existing IDs and data-filter attributes are preserved.
- The patch is CSS and icon-rendering focused.

## Verification
- GitHub read-back completed.
- Static checks confirmed the story SVG mappings and initializer, mobile safe-area spacing, touch-target rules, contrast override, unique style block, and balanced script/head tags.
- Browser runtime, visual regression, device rotation, keyboard navigation, and screen-reader checks remain pending.
