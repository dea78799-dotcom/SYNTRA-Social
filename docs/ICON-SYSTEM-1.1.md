# SYNTRA Social — Icon System 1.1

## Design direction
- Minimal, rounded-outline iconography with a calm, premium social-app feel.
- 24 × 24 SVG viewBox; default rendered size 21–23px.
- Stroke only, rounded joins and caps; use currentColor so active/hover states inherit the interface palette.
- No emoji as primary navigation symbols.

## Navigation icon mapping
| Label | Icon concept |
|---|---|
| Trang chủ | House |
| Khám phá | Search |
| Video | Play in rounded rectangle |
| Ảnh | Picture frame |
| Cộng đồng | Connected people |
| Đang theo dõi | Heart |
| Đã lưu | Bookmark |
| Tin nhắn | Envelope |
| Cài đặt | Gear |

## Mobile bottom bar
Home, Explore, Communities, Create, Inbox, Profile, Settings. The Create action is visually elevated with a filled SYNTRA gold tile.

## Composer
Photo, Video, Community actions use matching SVG line icons.

## Implementation
The icon renderer is inline in index.html as synIcon(name). Static navigation glyphs are converted when the page script initializes; composer actions use SVG markup directly. Existing click handlers and data attributes remain unchanged.

## Status and limitations
This update changes icon visuals only. No database/API changes. Browser interaction and small-screen visual QA have not yet been performed, so the next pass should verify icon alignment, touch targets, active states, and screen-reader labels.
