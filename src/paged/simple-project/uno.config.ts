import { defineConfig, presetUno } from 'unocss'

export default defineConfig({
  presets: [
    presetUno(),
  ],
  shortcuts: {
    'bg-base': 'bg-[var(--c-bg-base)]',
    'bg-surface': 'bg-[var(--c-bg-surface)]',
    'bg-elevated': 'bg-[var(--c-bg-elevated)]',
    'text-main': 'text-[var(--c-text)]',
    'text-muted': 'text-[var(--c-text-muted)]',
    'text-dim': 'text-[var(--c-text-dim)]',
    'text-primary': 'text-[var(--c-primary)]',
    'text-accent': 'text-[var(--c-accent)]',
    'border-base': 'border-[var(--c-border)]',
  },
})
