# Global Dark Mode Toggle — Design

## Decisions
- **Scope**: Full coverage across all 24 components + page.tsx
- **Toggle placement**: Header bar, next to existing controls (Sun/Moon icon)
- **Persistence**: localStorage + OS `prefers-color-scheme` fallback
- **Flash prevention**: Inline `<script>` in layout.tsx `<head>`
- **Tailwind strategy**: `darkMode: 'class'` on `<html>`

## Architecture
1. **Flash-prevention script** in `layout.tsx <head>` — reads localStorage/matchMedia, sets `dark` class before paint
2. **Tailwind config** — `darkMode: 'class'`
3. **ThemeProvider** — React context with `{ theme, toggleTheme }`, syncs localStorage + `<html>` class
4. **Component updates** — `dark:` variants on all backgrounds, text, borders, shadows

## Component Tiers
- **Tier 1 (mechanical)**: 18 components — add `dark:` class variants
- **Tier 2 (charts)**: 4 Recharts components — dynamic axis/grid/tooltip colors via `useTheme()`
- **Tier 3 (special)**: CrisisEventsBrowser, page.tsx multi-path returns

## Dark Palette Mapping
| Light | Dark |
|-------|------|
| `bg-white` | `dark:bg-gray-900` |
| `bg-gray-50` | `dark:bg-gray-950` |
| `bg-gray-100` | `dark:bg-gray-800` |
| `text-gray-900` | `dark:text-white` |
| `text-gray-600` | `dark:text-gray-400` |
| `text-gray-500` | `dark:text-gray-400` |
| `border-gray-200` | `dark:border-gray-700` |
| `border-gray-300` | `dark:border-gray-600` |
| Chart grid `#e5e7eb` | `#374151` |
