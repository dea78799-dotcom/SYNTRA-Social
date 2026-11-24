# SYNTRA Social — Mobile composer repair 2.0

## User-facing changes

- On phones, the create-post dialog opens as a bottom sheet instead of a centered desktop-style modal.
- The dialog has a viewport-aware maximum height and internal scrolling, including safe-area spacing.
- The media selection row becomes two equal-width touch controls on small screens.
- The publish/cancel row remains visible during dialog scrolling.
- The text field and controls receive visible keyboard-focus treatment.

## Accessibility and interaction

- The dialog declares dialog semantics, modal state, and a labelled title.
- The post text field has an accessible name.
- Escape closes the composer.
- Background page scrolling is locked while the composer is open.
- Closing the composer restores focus to the control that opened it.

## Validation performed

- Read the latest index.html back from GitHub after commit.
- Confirmed the new style block appears exactly once.
- Confirmed mobile bottom-sheet rules, scroll locking/unlocking, Escape handling, focus restoration, dialog semantics, and textarea label are present.
- Confirmed the previous one-line open handler is absent.

## Validation still required

- Test on Android Chrome with the keyboard open and closed.
- Test short-height landscape and portrait screens.
- Test image/video selection, preview removal, cancel, and publish.
- Check that focus restoration and Escape behavior work on desktop browsers.

This change has not been visually verified in a live browser. It does not change media storage, publishing logic, or backend behavior.
