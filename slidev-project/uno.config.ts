import { defineConfig, presetUno } from 'unocss'

export default defineConfig({
  presets: [
    presetUno(),
  ],
  shortcuts: {
    // Theme-aware shortcuts using CSS variables from SlideShell
    'bg-theme-base': 'bg-[var(--c-bg-base)]',
    'bg-theme-surface': 'bg-[var(--c-bg-surface)]',
    'text-theme-main': 'text-[var(--c-text-main)]',
    'text-theme-muted': 'text-[var(--c-text-muted)]',
    'border-theme': 'border-[var(--border-theme)]',
    'shadow-theme': 'shadow-[var(--shadow-theme)]',
    'text-theme-primary': 'text-[var(--c-primary)]',
    'bg-theme-primary': 'bg-[var(--c-primary)]',
  },
  theme: {
    colors: {
      // CSS variables will reference SlideShell theme definitions
    },
  },
})
