# Compare Figure Standard

Use this for `1.3.x` recommended/not-recommended figures.

## Default Visibility (Blocking)

The recommended/not-recommended difference must be visible on the first screen without any user interaction.

**Do not hide the key contrast inside:**

- `Collapse` / accordion
- `Tabs` (non-default tab)
- `Dropdown` / overflow menus
- `Popover` / `Tooltip`
- `Drawer` / `Modal`
- `Pagination` (second page or later)
- `Carousel` / slideshow

If the component under illustration is itself one of these interactive containers (e.g. a Collapse comparison figure), the key content must be shown in its **default open / expanded state** — not collapsed or hidden behind a click.

Flag as a **blocking error** if the comparison figure requires user interaction to reveal which side is recommended and which is not.

## Required Shape

The figure should compare two sides of the same business situation:

- left: correct decision
- right: corresponding incorrect decision

Avoid showing two valid alternatives side by side.

## Visual Skeleton

Each side should stack:

1. white scenario panel with fixed **minimum** height (`minHeight`), plus `flex: 1` to fill the side column — **never use a hardcoded `height`**
2. 4px status strip
3. label row

**Equal-height structure (mandatory):** `alignItems: 'stretch'` on the Flex parent alone is not enough when the two sides have different content heights. Each side's outer div must be a flex column (`display: 'flex', flexDirection: 'column'`) so the panel's `flex: 1` can expand to match the taller side:

```js
const side = { flex: 1, display: 'flex', flexDirection: 'column' };
const panel = { ..., minHeight: 200, flex: 1 };
```

Without `flexDirection: 'column'` on the side div, the panel height is still determined by its own content, and the shorter side will not stretch to match.

Required status colors:

- recommended strip: `#52c41a`
- not recommended strip: `#ff4d4f`
- recommended label background: `#f6ffed`
- not recommended label background: `#fff2f0`
- recommended label border: `1px solid #b7eb8f`
- not recommended label border: `1px solid #ffccc7`

Label row complete style (authoritative reference: agent_code_id=2046):

| Property | Recommended | Not Recommended |
|---|---|---|
| background | `#f6ffed` | `#fff2f0` |
| border | `1px solid #b7eb8f` | `1px solid #ffccc7` |
| borderTop | `none` (seamless with strip above) | `none` |
| padding | `10px 14px` | `10px 14px` |
| fontWeight | `700` | `700` |
| color (text) | `#389e0d` | `#cf1322` |
| fontSize | not specified, inherit default | not specified, inherit default |

The label row text should be only:

- `推荐`
- `不推荐`

## Business Scene Requirement (checked as warning by checker script)

The panel should show a concrete business scene. At minimum one of:

- `Table` or `Form` component
- Back-office page frame with Topbar (`background: '#001529'`) and Sidebar (`borderRight`)

For small, self-contained components (e.g. Rate, Tag, Badge) that have no natural page-level context, a card or list scene is acceptable. The checker reports this as a **warning**, not an error — confirm with the author before treating it as blocking.

Do not place only an isolated target component + Typography.Text description inside the panel.

## Content Quality

The panel must show a concrete business scene, such as a table, form, approval flow, export modal, release task, or sync task.

Relationship illustrations must draw component bodies, not colored tags standing in for components.
