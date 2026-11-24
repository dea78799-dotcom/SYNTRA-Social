# SYNTRA Social — Post Card and Overflow Menu 1.5

## Scope
Refine feed and discovery post cards, then add a compact overflow action panel without changing the post data model.

## Post card refinements
- Softer layered charcoal surface, subtle border, and restrained shadow.
- Consistent card radius and spacing on mobile.
- Better text wrapping and long author-name handling.
- More consistent post action spacing and touch targets.

## Overflow menu
- Replaces the old three-dot action that immediately invoked report/delete behavior.
- Opens a contextual panel from feed and discovery post cards.
- For the local user's own post, exposes a delete action with confirmation and the existing media cleanup flow.
- For another user's post, exposes a report entry. Reporting remains a local placeholder until a moderation backend exists.
- Uses a native button with `aria-controls` and `aria-expanded`.
- Closes on outside click or Escape; Escape restores focus to the opener.

## Data and safety boundaries
- Does not add server-side reporting or claim that reports reach moderators.
- Does not change authentication, post persistence, or the media storage model.
- Deletion is limited to posts owned by the local profile and retains the existing confirmation and media deletion logic.

## Verification
- GitHub source read-back and static checks are required after the update.
- Browser interaction, Android viewport, keyboard, and assistive-technology testing remain pending.
