import { defineConfig } from 'unocss'

export default defineConfig({
  shortcuts: {
    // Business-specific shortcuts
    'business-card': 'bg-white rounded-lg shadow-md border border-gray-200',
    'business-header': 'text-2xl font-bold text-gray-900',
    'business-text': 'text-gray-700 leading-relaxed',
  },
  theme: {
    colors: {
      // Professional business color palette
      'business-primary': '#0F4C81',
      'business-secondary': '#2D5F8B',
      'business-accent': '#E67E22',
      'business-success': '#27AE60',
      'business-warning': '#F39C12',
      'business-danger': '#E74C3C',
      'business-bg': '#FAFBFC',
      'business-surface': '#FFFFFF',
      'business-border': '#E1E5E9',
    }
  }
})
