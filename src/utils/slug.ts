export function emojiSlug(name: string): string {
  return name
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '');
}

function codePointSuffix(emoji: string): string {
  return [...emoji]
    .map((c) => c.codePointAt(0)?.toString(16) ?? '')
    .join('-');
}

// Returns slugs parallel to `items`. When two names slugify to the same value,
// disambiguates by appending the emoji's code-point hex so SEO-friendly slugs
// stay clean for the common case.
export function buildEmojiSlugs(items: Array<{ name: string; emoji: string }>): string[] {
  const counts = new Map<string, number>();
  for (const item of items) {
    const base = emojiSlug(item.name);
    counts.set(base, (counts.get(base) ?? 0) + 1);
  }
  return items.map((item) => {
    const base = emojiSlug(item.name);
    return (counts.get(base) ?? 0) > 1 ? `${base}-${codePointSuffix(item.emoji)}` : base;
  });
}
