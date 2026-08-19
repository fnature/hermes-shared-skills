# Accessibility, Mobile, and Performance

## Accessibility baseline

Verify affected pages and interactions for:

- semantic landmarks and logical headings;
- meaningful image alt text; `alt=""` for truly decorative images;
- keyboard reachability and operation;
- visible focus indication;
- adequate text and UI contrast;
- associated form labels, instructions, and errors;
- meaningful links and button names;
- accessible menus and dialogs;
- reduced-motion preferences;
- native HTML before ARIA.

Do not repeat a nearby caption verbatim in alt text. Describe the image’s purpose in context, not every pixel.

Automated checks do not replace keyboard and representative screen-reader testing. Report unperformed manual checks as `BLOCKED`.

## Responsive and mobile

Verify representative narrow and wide viewports. Avoid horizontal scrolling, tiny text, clipped controls, unreachable navigation, fixed dimensions that break content, and interaction available only through hover. Maintain touch-friendly targets and readable line lengths.

## Performance

Prefer static HTML for content sites, appropriately sized compressed images, modern formats when compatible, local/system fonts when suitable, minimal third-party code, cacheable assets, compression, and deferred non-critical JavaScript.

Do not add a large framework or runtime merely for simple content pages or AI interoperability. Avoid layout shifts, blocking scripts, unnecessary animation, autoplay media, and unused JavaScript.

Measure production or a production-equivalent build. Source-level simplicity is encouraging but not a performance result. Report Lighthouse/Core Web Vitals claims only from real tool output, including the tested URL, device mode, and date.
