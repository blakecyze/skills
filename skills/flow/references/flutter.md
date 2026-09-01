# Flutter

Loaded when the target is Flutter or Dart.

## Where tokens live

Prefer a `ThemeExtension` over a bare constants class. It survives light and dark switching, it is reachable from any `BuildContext`, and it keeps the values out of widget files.

```dart
@immutable
class FlowTokens extends ThemeExtension<FlowTokens> {
  final double space1, space2, space3, space4, space6, space8;
  final double radiusSm, radiusMd, radiusLg;
  // copyWith and lerp required by the interface
}
```

Access as `Theme.of(context).extension<FlowTokens>()!`. A literal `16` inside a widget's padding is FLOW-04, regardless of whether 16 happens to be correct.

Text styles belong in `TextTheme`. A `TextStyle` constructed inline is a scale escape.

## Spacing idioms

Prefer `Gap` or `SizedBox` between children over `Padding` around each child. Padding on children is where asymmetric spacing comes from, because the gap between two padded siblings is the sum of two paddings and nobody computes it.

`Column(spacing: ...)` and `Row(spacing: ...)` exist in current Flutter and are preferable to interleaved `SizedBox` widgets. They also make FLOW-01 visible in the source, since the uniform gap is written once.

`Padding` with `EdgeInsets.all()` on a card whose child is itself padded is the most common source of FLOW-10 in Flutter.

## Widgets that generate findings

- **`Card`** ships with elevation *and* a shape border. Adding a `Container` decoration behind it is FLOW-05.
- **`Container`** used purely to add padding should be `Padding`. Used purely to add colour, `ColoredBox`. A `Container` doing one job is a rebuild cost and a readability cost.
- **`IconButton`** defaults to a 48dp target, which is correct. Wrapping a bare `Icon` in `GestureDetector` gives you the icon's size as the target, which usually fails FLOW-11.
- **`ListTile`** enforces Material metrics that may fight a custom density class. Fine, but do not then hand-tune half of them.
- **`Expanded` inside long text** produces full-width measures on tablets. FLOW-12. Constrain with `ConstrainedBox(maxWidth: ...)`.

## Focus and semantics

Focus rings are not automatic on custom widgets. `InkWell` and `Material` buttons handle it; a `GestureDetector` does not. If a tappable widget is built from `GestureDetector`, it needs `Focus`, a visible focus decoration, and a `Semantics` label.

Never remove a `Semantics` node to fix a layout problem. That is a behaviour change and belongs in the deferred list.

## Theming both modes

`ThemeData.light()` and `.dark()` need separate token instances. Auditing only one mode is a documented failure mode. Elevation in dark mode comes from a lighter surface tint, not from a heavier shadow, because shadows are close to invisible on dark backgrounds.

## Text scaling

Respect `MediaQuery.textScaler`. Fixed-height containers around scalable text overflow at large accessibility sizes. Prefer `IntrinsicHeight`, `minHeight` constraints, or letting the row wrap. An overflow ellipsis on a settings label at 200% text scale is a Tier 1 finding.
