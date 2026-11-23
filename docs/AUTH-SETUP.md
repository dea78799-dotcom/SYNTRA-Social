# SYNTRA Social — Auth setup checklist (B1)

**Supabase project:** SYNTRA-Social  
**Project ref:** qmrhlbovksrspmauijrz  
**Region:** ap-southeast-1 (Singapore)  
**Status:** Database schema and profile-creation trigger are deployed. The project owner reports that the Email provider has been enabled; this setting is not independently readable through the current connector. URL configuration, email-delivery verification, frontend integration and end-to-end account tests remain pending.

This guide is for the project owner configuring the Supabase Dashboard. Do not paste passwords, access tokens, service-role keys, or recovery codes into GitHub issues, chat, or frontend code.

## 1. Email provider

The project owner reports that Email sign-in is enabled in Supabase Authentication → Sign In / Providers.

Before testing real accounts, verify in the Dashboard:

- Password-based sign-in is enabled.
- Email confirmation is enabled.
- Anonymous sign-in remains disabled for the first release.
- Third-party providers remain disabled until redirect and account-linking behavior has been reviewed.

If SMTP is not configured, Supabase's default email service may have delivery limits. Do not launch registration publicly until email delivery and rate limits are understood and tested.

## 2. Configure URL settings

Open Authentication → URL Configuration.

- Set Site URL to the exact deployed SYNTRA Social origin (not the Supabase project URL).
- Add the exact local development origin to Redirect URLs only when local development is being used.
- Add the exact production callback/origin used by the application.
- Avoid broad wildcard redirect patterns.
- Verify confirmation and password-reset links return to the intended SYNTRA Social page.

Do not guess the production URL. Confirm the deployed website's actual domain before saving these values.

## 3. Profile creation behavior

The database migration `syntra_social_auth_profile_trigger` installs:

- `auth.users` after-insert trigger `on_auth_user_created`
- `public.handle_new_user()` with a fixed empty search_path and SECURITY DEFINER
- a `profiles` row for each newly created auth user
- a generated fallback username when supplied metadata is invalid

The username unique index is case-insensitive. A username collision should be handled by the database trigger fallback; the client must still show a friendly validation error and must not assume a requested username was reserved until registration succeeds.

Only pass non-sensitive profile metadata such as `username` and `display_name` to signUp. Never put email, phone, birth date, password, or private details into public profile metadata.

## 4. Client integration requirements

The current `index.html` is a local-only prototype. Do not replace local storage behavior or expose real user data until the following are implemented:

- A dedicated sign-in / sign-up screen with accessible labels and validation.
- Supabase client initialized from the project URL and publishable key only.
- Session restore on page load and explicit sign-out.
- Email confirmation and password-reset flows.
- Auth state listener with safe UI updates.
- Error handling that does not reveal whether an arbitrary email address has an account.
- Server-side RLS tests before any profile/post query is enabled.
- Clear separation between local demo data and authenticated server data.

The browser may use the project URL and publishable key. Never use a secret key or service-role key in browser code, GitHub Pages, screenshots, or client-side environment variables.

## 5. Required test matrix before enabling registration

Use dedicated test accounts; do not use the project owner's personal account as the only test identity.

| Test | Expected result |
|---|---|
| Sign up with valid email and password | Confirmation email is sent; account remains unconfirmed until verified |
| Confirm email | User can establish a session |
| Profile trigger | Exactly one matching profile row is created |
| Duplicate username | Registration/profile creation does not overwrite another user's profile |
| Wrong password | Generic authentication failure; no sensitive detail |
| Password reset | Link returns to the approved SYNTRA origin |
| Sign out | Session is cleared |
| Anonymous profile query | No private profile data is returned |
| User A reads User B's private profile | Denied |
| User A updates User B's profile | Denied |
| Security Advisor | No unresolved critical/high findings |

## 6. Current implementation boundary

The database currently has nine application tables with RLS enabled. The profile trigger has been deployed and checked. Email provider enablement is owner-reported, not connector-verified. This does **not** mean registration, email delivery, profile discovery, or the web client integration has been tested.

Keep the public prototype local-only until the test matrix and the later post/media authorization policies pass.
