# SYNTRA Social — Android mobile regression checklist 2.37

Purpose: verify the mobile experience on real Android phones after the 2.37 interaction-quality update. This checklist is manual; GitHub Actions only checks source-level invariants and does not simulate a real phone.

## Safety before testing

- Use only test accounts and sample posts. Do not enter real passwords, recovery codes, TOTP codes, private messages, or personal information into screenshots or bug reports.
- Do not share account UUIDs, QR enrollment images, access tokens, or private media links.
- Keep the existing data. Do not use account deletion, reset, or destructive cleanup actions as part of this test.

## Phone layout and navigation

- [ ] Open the deployed website in Chrome on Android.
- [ ] Confirm the page fits the screen width without horizontal scrolling.
- [ ] Confirm the bottom navigation stays visible and does not cover the last feed item.
- [ ] Tap every bottom navigation item once; confirm the correct view opens and the active item is indicated.
- [ ] Rotate the phone if supported; confirm the layout remains usable.
- [ ] Scroll to the bottom of a long screen; confirm the fixed navigation and safe-area padding do not overlap important controls.

## Post composer

- [ ] Open the post composer from the bottom Create button.
- [ ] Focus the text field and open the Android keyboard.
- [ ] Confirm the dialog can scroll and the Cancel / Publish actions remain reachable.
- [ ] Cancel a draft and confirm no post is created.
- [ ] Create a harmless test-only text post and confirm it appears once.
- [ ] Reopen the composer and confirm the previous draft is not unexpectedly duplicated.

## Feed, media, and notifications

- [ ] Scroll the feed and open a post detail; use Back and confirm the previous view is restored.
- [ ] Open an image in the media viewer; verify Close, Previous, Next, and Download controls are usable.
- [ ] If testing video, use a small non-sensitive sample file and verify playback controls.
- [ ] Open the notification center, mark items read, and verify the unread count updates.

## Account and cross-device checks

- [ ] Sign in using a dedicated test account on phone A.
- [ ] Sign in with the same test account on phone B.
- [ ] Create one harmless public test post on phone A; refresh phone B and verify whether the public post appears.
- [ ] Verify that private posts and private profile data are not exposed to a second unrelated test account.
- [ ] Sign out on one phone and confirm the other phone's session is not unexpectedly signed out.
- [ ] Do not test Owner moderation unless the Owner role was intentionally provisioned and TOTP MFA is configured by the project owner.

## Bug report format

Record only:
- Phone model and Android version
- Browser name and version
- Screen or action where the issue occurred
- Expected result
- Actual result
- Whether it happens every time

Do not include credentials, account identifiers, private message contents, or personal data.
