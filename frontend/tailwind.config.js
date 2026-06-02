/** @type {import('tailwindcss').Config} */
export default {
  darkMode: "class",
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        "primary": "var(--primary)",
        "on-primary-fixed": "var(--on-primary-fixed)",
        "on-primary-container": "var(--on-primary-container)",
        "primary-fixed": "var(--primary-fixed)",
        "secondary-fixed": "var(--secondary-fixed)",
        "surface-container-low": "var(--surface-container-low)",
        "secondary": "var(--secondary)",
        "surface-dim": "var(--surface-dim)",
        "surface-container-highest": "var(--surface-container-highest)",
        "tertiary-fixed-dim": "var(--tertiary-fixed-dim)",
        "background": "var(--background)",
        "surface-variant": "var(--surface-variant)",
        "tertiary-fixed": "var(--tertiary-fixed)",
        "surface": "var(--surface)",
        "surface-bright": "var(--surface-bright)",
        "on-error": "var(--on-error)",
        "on-tertiary-container": "var(--on-tertiary-container)",
        "on-tertiary": "var(--on-tertiary)",
        "on-tertiary-fixed": "var(--on-tertiary-fixed)",
        "on-error-container": "var(--on-error-container)",
        "surface-container-lowest": "var(--surface-container-lowest)",
        "surface-container-high": "var(--surface-container-high)",
        "inverse-surface": "var(--inverse-surface)",
        "on-secondary": "var(--on-secondary)",
        "tertiary-container": "var(--tertiary-container)",
        "secondary-fixed-dim": "var(--secondary-fixed-dim)",
        "tertiary": "var(--tertiary)",
        "secondary-container": "var(--secondary-container)",
        "on-secondary-fixed-variant": "var(--on-secondary-fixed-variant)",
        "outline-variant": "var(--outline-variant)",
        "on-primary-fixed-variant": "var(--on-primary-fixed-variant)",
        "primary-container": "var(--primary-container)",
        "outline": "var(--outline)",
        "on-surface": "var(--on-surface)",
        "error-container": "var(--error-container)",
        "on-background": "var(--on-background)",
        "surface-container": "var(--surface-container)",
        "surface-tint": "var(--surface-tint)",
        "on-primary": "var(--on-primary)",
        "inverse-on-surface": "var(--inverse-on-surface)",
        "on-surface-variant": "var(--on-surface-variant)",
        "on-secondary-container": "var(--on-secondary-container)",
        "on-secondary-fixed": "var(--on-secondary-fixed)",
        "primary-fixed-dim": "var(--primary-fixed-dim)",
        "on-tertiary-fixed-variant": "var(--on-tertiary-fixed-variant)",
        "error": "var(--error)",
        "inverse-primary": "var(--inverse-primary)"
      },
      borderRadius: {
        "DEFAULT": "0.125rem",
        "lg": "0.25rem",
        "xl": "0.5rem",
        "full": "0.75rem"
      },
      spacing: {
        "unit": "4px",
        "component-padding-y": "0.375rem",
        "component-padding-x": "0.625rem",
        "container-padding": "1rem",
        "cell-padding": "0.25rem 0.5rem",
        "panel-gap": "0.5rem",
        "px-container": "1rem"
      },
      fontFamily: {
        "data-mono": ["JetBrains Mono", "monospace"],
        "body-sm": ["Inter", "sans-serif"],
        "label-caps": ["Inter", "sans-serif"],
        "display-md": ["IBM Plex Sans", "sans-serif"],
        "body-base": ["Inter", "sans-serif"],
        "header-sm": ["IBM Plex Sans", "sans-serif"]
      },
      fontSize: {
        "data-mono": ["12px", {"lineHeight": "16px", "letterSpacing": "-0.01em", "fontWeight": "500"}],
        "body-sm": ["12px", {"lineHeight": "16px", "letterSpacing": "0em", "fontWeight": "400"}],
        "label-caps": ["10px", {"lineHeight": "12px", "letterSpacing": "0.05em", "fontWeight": "700"}],
        "display-md": ["24px", {"lineHeight": "32px", "letterSpacing": "-0.02em", "fontWeight": "600"}],
        "body-base": ["13px", {"lineHeight": "18px", "letterSpacing": "0em", "fontWeight": "400"}],
        "header-sm": ["16px", {"lineHeight": "24px", "letterSpacing": "-0.01em", "fontWeight": "600"}]
      }
    },
  },
  plugins: [],
}

// force rebuild
