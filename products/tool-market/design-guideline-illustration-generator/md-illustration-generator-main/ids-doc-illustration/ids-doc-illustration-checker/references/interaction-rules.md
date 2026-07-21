# Interaction Rules

Use these rules for `react` code blocks in IDS component docs.

## React Block Shape

Each block should define a single top-level `function App()`.

Do not use:

- `import`
- `export`
- TypeScript annotations
- old `render(...)` snippets

## Forbidden Runtime Patterns

These are blocking unless explicitly justified by a component-specific exception:

- `defaultOpen`
- `defaultVisible`
- `open={true}`
- `visible={true}`
- bare `open` or `visible` JSX boolean props
- `message.*`
- `notification.*`
- bare `<ConfigProvider>` in Markdown code blocks

Use `<Infrad.ConfigProvider>` or `const { ConfigProvider } = Infrad` if a config provider is needed.

## Floating Layers

For static documentation illustrations, avoid real always-open floating components that portal to `body` and cover the document while scrolling.

Missing `getPopupContainer` / `getContainer` is a hint, not automatically blocking. It becomes a real issue only when the demo escapes the illustration area or interrupts reading.

### Select / DatePicker / TimePicker / Cascader / TreeSelect (position: absolute dropdowns)

These use `position: absolute` for their dropdowns. Containment requires:

- `getPopupContainer={() => ref.current}` on the component
- wrapper div with `position: 'relative'`
- MutationObserver fix for the open-state "是什么" illustration

Missing any of these is blocking for open-state illustrations.

### Modal / Drawer (position: fixed overlays)

Modal and Drawer use `position: fixed` for their backdrop. `overflow: hidden` alone cannot contain them — they escape to viewport level. Containment requires all four on the **outermost Page Shell div** (the div wrapping topbar + sidebar + content):

- `transform: 'translateZ(0)'` — creates a new containing block for fixed descendants
- `position: 'relative'`
- `overflow: 'hidden'`
- `getContainer={() => ref.current}` on the Modal/Drawer component

**Flag as blocking** if a react block contains `Modal` or `Drawer` and any of the above is missing on the outer container. Also flag if `ref` is attached to the content panel only (not the full Page Shell div).

## Page Shell Scene Figures

Scene figures that use the Page Shell layout (topbar + sidebar + content area) must follow this rule:

- **`content` panel must NOT have `overflow: hidden`** — fake-div dropdowns or any self-drawn floating layers are rendered as normal children inside the content panel. Adding `overflow: hidden` clips them and makes the dropdown invisible. Flag this as a blocking issue. Height must not be artificially inflated to compensate; it should be driven by content, not hardcoded.

## 1.3.x Compare Figures with Dropdown Components (AutoComplete, Select, etc.)

When a 1.3.x 推荐/不推荐 compare figure contains a dropdown component (AutoComplete, Select, Cascader, etc.) with `open` prop:

### paddingBottom requirement (BLOCKING)

The **panel div** (the white scene panel with `border: '1px solid #f0f0f0'`) MUST have `paddingBottom: 160` (or more if options > 4). This is mandatory because:

- The dropdown is rendered via `getPopupContainer={() => ref.current}` — it is positioned `absolute` inside the `wrapper` div, NOT inside the `panel` div.
- The color bar and label row immediately follow the `panel` in the DOM.
- Without `paddingBottom`, the dropdown (which does not occupy document flow) overlaps the color bar and label row below the panel.
- Adding `paddingBottom: 160` to the panel makes the panel tall enough so the color bar and label are pushed below the dropdown's visible area.

Flag as **blocking** if the panel contains a dropdown component with `open` and does not have `paddingBottom` of at least 160px.

Correct structure:
```js
const panel = { background: '#fff', border: '1px solid #f0f0f0', borderBottom: 'none', padding: 16, paddingBottom: 160 };
```

### getBoundingClientRect requirement (BLOCKING)

When computing the dropdown position in the MutationObserver `fix()` function inside a 1.3.x compare figure, **MUST use `getBoundingClientRect()`** — NOT `offsetTop` / `offsetLeft`:

```js
// ✅ Correct
const cRect = ref.current.getBoundingClientRect();
const tRect = trigger.getBoundingClientRect();
const top = tRect.bottom - cRect.top + 4;
const left = tRect.left - cRect.left;

// ❌ Wrong — offsetTop is relative to offsetParent (the panel with padding:16),
//    not to the wrapper div. Causes the dropdown to appear shifted up/left.
const offsetTop = trigger.offsetTop + trigger.offsetHeight + 4;
const left = trigger.offsetLeft;
```

Flag as **blocking** if the fix function uses `trigger.offsetTop` or `trigger.offsetLeft` instead of `getBoundingClientRect()` in a 1.3.x compare figure context (where the trigger is nested inside a panel div with padding).
