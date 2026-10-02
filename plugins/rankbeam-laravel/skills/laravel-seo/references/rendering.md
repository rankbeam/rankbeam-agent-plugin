# Verify the head that users and crawlers receive

Choose the actual stack. Package dependencies only suggest a stack; inspect the route and its rendered template/component.

## Blade

Render `@seo($post)` once inside the real page's `<head>`, using the model variable the controller actually supplies. It already emits title, description, canonical, robots when needed, social tags and available JSON-LD. Remove only superseded tags from this same head producer; preserve unrelated custom tags and consent integrations.

Test a successful raw response, not only the Blade source. One valid title, description and absolute canonical are the checker's baseline. Omitted default `index,follow` is normal. JSON-LD is only required where the page/use case calls for it.

## Inertia (Vue / React / Svelte)

Pass `SEO::forInertia($model)` from the controller as a page prop. It has `title`, `meta` and `link` entries. Vue and React use Inertia's `Head`; each generated meta/link must carry the provided `head-key`. Framework list `key` alone does not deduplicate head elements. Svelte uses `svelte:head` and should have one owner for those tags.

For Vue, bind the provided attribute object rather than creating absent `name`, `property` or `hreflang` props. Inertia 2's head serializer can turn an explicitly bound undefined prop into the literal string `"undefined"`:

```vue
<Head :title="seo.title">
    <meta v-for="m in seo.meta" :key="m['head-key']" v-bind="m" />
    <link v-for="l in seo.link" :key="l['head-key']" v-bind="l" />
</Head>
```

Use only renderer-produced attribute objects here. Check the actual DOM for `name="undefined"`, `property="undefined"` or `hreflang="undefined"` as well as duplicate tags. Filter absent attributes when adapting the recipe to a different renderer or head manager.

React's Inertia head serializer needs the same omission of absent properties. Spread each renderer-produced meta object; add `hrefLang` only to actual alternates:

```jsx
<Head title={seo.title}>
    {seo.meta.map(m => <meta key={m['head-key']} {...m} />)}
    {seo.link.map(l => <link key={l['head-key']} head-key={l['head-key']}
        rel={l.rel} href={l.href} {...(l.hreflang ? { hrefLang: l.hreflang } : {})} />)}
</Head>
```

`forInertia()` intentionally omits scripts. JSON-LD comes from `SEO::toArray($model)['script']` and needs the documented root-view and navigation treatment. Read the maintained [Inertia guide](https://docs.rankbeam.dev/guide/inertia-json) and the installed version's renderer before implementing this path. Do not invent a `Head` script API or inject untrusted raw HTML. Rankbeam renderer-produced JSON is escaped for script safety; arbitrary user strings are not equivalent.

Check the initial raw HTML separately from the browser DOM. Client-only insertion does not establish crawler/social-scraper visibility. If SSR/prerender is absent, state that limitation and scope the SSR work with the user; do not claim a metadata-only patch enabled SSR. After navigation rich page → bare page → rich page, check that previous schema and social fields disappear and no duplicates accumulate.

## Livewire

The first full response can use the same Blade directive. With `wire:navigate`, old JSON-LD scripts can remain after page transitions. Use the maintained [Livewire cleanup recipe](https://docs.rankbeam.dev/guide/livewire) for the installed version. It removes stale URL-marked scripts and duplicate same-page scripts, including when the destination has no schema. Test rich → bare → rich and repeat visits. Never delete every script in the document.

## Claims and coverage

Save raw local response bytes as UTF-8 HTML, run `scripts/check-head.php`, and examine its findings and limitations. The helper parses inert HTML with PHP DOM; it is not a browser, HTML5 conformance validator, full accessibility audit or schema validator. Valid JSON-LD syntax does not imply valid vocabulary or rich-result eligibility. Missing social tags are not always a defect; report them only when the page's requirements call for them.

Always preserve intentional `noindex`, multilingual alternates and explicit canonical decisions. Check server `X-Robots-Tag`, status and redirects separately. A source-only inspection or unavailable browser is a stated verification gap, not a reason to manufacture a pass.
