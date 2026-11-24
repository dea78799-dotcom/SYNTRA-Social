# SYNTRA Social 1.9 — Homepage visual refinement

Date: 2026-11-24

## User-facing changes

- Added a dedicated heading above the feed filters: “Bảng tin”.
- Added the supporting description: “Một nơi để khám phá ý tưởng, câu chuyện và cộng đồng.”
- Added a small “Đang thử nghiệm” status indicator to set expectations clearly.
- Applied responsive spacing and typography for desktop and narrow mobile screens.
- Kept the existing feed tabs and filter controls unchanged.

## Design intent

The homepage should communicate its purpose immediately. The new heading creates a clearer visual hierarchy between the top search bar, the feed navigation and the content stream. The beta label is intentionally restrained and does not compete with the main heading.

## Files changed

- `index.html`
- `README.md`

## Validation

The updated `index.html` was fetched again from the GitHub main branch. Automated content checks confirmed:
- The homepage heading appears exactly once.
- The Vietnamese title, description and beta status are present.
- Desktop and mobile CSS rules are present.
- The existing `#tabs` feed navigation remains in place.

A real rendered browser test on Android and desktop has not yet been completed. This update is a frontend visual refinement only; it does not add backend functionality or change data handling.
