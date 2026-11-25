# SYNTRA Social 2.49 — Offline recovery

## What it does

SYNTRA stores a minimal device-local recovery marker when the current signed-in account loses connectivity or the app moves into the background. When connectivity returns and the app becomes visible, it schedules an authenticated refresh.

## Retry policy

- Initial delay: approximately 15 seconds.
- Exponential backoff: doubles after each failed attempt.
- Maximum delay: 5 minutes, plus up to 5 seconds of jitter.
- The marker is cleared after the full recovery refresh succeeds.

## Privacy and account isolation

The marker contains only the account ID, attempt count, and timestamps. It does not contain session tokens, passwords, post text, media, or pending write payloads. A marker is retried only while the same account is signed in.

## Scope and limitations

This version retries reads/refreshes only. It does not queue post publishing, comments, likes, or other writes offline, avoiding duplicate or ambiguous writes after reconnect. Existing local composer drafts remain local. Real Android background/resume and network-loss tests are still required.
