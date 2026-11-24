# SYNTRA Social — Icon System 1.3

## Scope
This pass extends the existing 1.1 outline icon language to notifications, profile actions, and messaging controls.

## New icon mappings
- Notifications: bell heading, mail/read-all action, close control.
- Notification types: settings/system, heart/like, comment, user-plus/follow, mail/message, bell/activity.
- Profile actions: edit, follow, block/protect, back to feed.
- Messaging: back-to-conversation and send action.

## Implementation
- Uses the existing `synIcon(name)` SVG renderer and the same 24 × 24 outline grid.
- SVGs inherit `currentColor`; icon-only controls have accessible labels.
- No data model, storage, navigation handler, or backend behavior was intentionally changed.
- Existing button labels remain alongside icons where applicable.

## Verification
- GitHub source read-back completed after updates.
- Static checks confirmed the added icon mappings, notification renderer, profile action markup, chat controls, and balanced script tags.
- Browser execution, mobile visual inspection, keyboard testing, and screen-reader testing remain pending.
