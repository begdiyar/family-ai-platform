import type { Config } from 'tailwindcss'

export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        // ── Primary: Deep Warm Indigo ────────────────────────────────
        primary: {
          DEFAULT: '#3C3888',   // ~10:1 on white, ~5:1 on canvas — WCAG AA
          50:  '#EDEAF8',
          100: '#D2CEF2',
          200: '#A5A0E5',
          light: '#EDEAF8',
          700: '#26235E',
        },
        // ── Accent: Deep Warm Terracotta ─────────────────────────────
        accent: {
          DEFAULT: '#885040',
          light: '#EEE4DC',
          700: '#5A2A1E',
        },
        // ── Deep Dusty Blue ──────────────────────────────────────────
        violet: {
          DEFAULT: '#385C8A',
          light: '#DDE8F2',
          700: '#1C3C68',
        },
        // ── Deep Muted Sage ───────────────────────────────────────────
        sage: {
          DEFAULT: '#386858',
          50:  '#E2EDE8',
          100: '#BCDAD0',
          700: '#1C4438',
        },
        // ── Category Palette (all deep, zero pastels) ─────────────────
        comm:       { DEFAULT: '#2C5678', light: '#DDEAF5', 700: '#143A58' },
        trust:      { DEFAULT: '#286250', light: '#D8EDE7', 700: '#104030' },
        conflict:   { DEFAULT: '#744E26', light: '#EEE2D4', 700: '#4A2A0E' },
        love:       { DEFAULT: '#74364A', light: '#EEE0E6', 700: '#4A1628' },
        recovery:   { DEFAULT: '#386050', light: '#DAE9E4', 700: '#143E30' },
        parenting:  { DEFAULT: '#4A5A2C', light: '#E2E8D8', 700: '#2A3A12' },
        traditions: { DEFAULT: '#463E80', light: '#E4E0F5', 700: '#2A2460' },
        // ── Core Neutrals ─────────────────────────────────────────────
        surface: '#E8E2D4',      // warm taupe — page background
        canvas:  '#F4EFE4',      // warm cream — card/elevated surface
        sidebar: '#27253A',      // deep warm slate — sidebar anchor
        sand:    '#C2B8A4',      // warm border/divider
        ink:     '#17152A',      // deep warm near-black
        muted:   '#68647C',      // secondary text
        // ── Semantic ─────────────────────────────────────────────────
        success: '#386858',
        warning: '#886028',
        danger:  '#843048',
      },

      height: {
        '13': '3.25rem',
        '18': '4.5rem',
      },

      borderRadius: {
        card:  '24px',
        btn:   '14px',
        input: '14px',
        pill:  '9999px',
      },

      boxShadow: {
        // Layered, expressive — creates real depth between elements
        card:  '0 2px 12px rgba(23,21,42,0.10), 0 12px 36px rgba(23,21,42,0.12)',
        hover: '0 8px 32px rgba(60,56,136,0.24), 0 4px 12px rgba(23,21,42,0.10)',
        soft:  '0 1px 4px rgba(23,21,42,0.07), 0 4px 14px rgba(23,21,42,0.08)',
        glow:  '0 0 0 4px rgba(60,56,136,0.22)',
        modal: '0 32px 80px rgba(23,21,42,0.22), 0 12px 32px rgba(23,21,42,0.14)',
        inner: 'inset 0 1px 4px rgba(23,21,42,0.12)',
      },

      fontFamily: {
        sans: ['"Plus Jakarta Sans"', 'system-ui', 'sans-serif'],
      },

      fontSize: {
        display: ['48px', { lineHeight: '1.1', letterSpacing: '-0.03em', fontWeight: '800' }],
      },

      backgroundImage: {
        // Deep brand gradient
        'gradient-brand':   'linear-gradient(135deg, #3C3888 0%, #385C8A 100%)',
        'gradient-peach':   'linear-gradient(135deg, #885040 0%, #3C3888 100%)',
        'gradient-sage':    'linear-gradient(135deg, #386858 0%, #385C8A 100%)',
        'gradient-violet':  'linear-gradient(135deg, #385C8A 0%, #3C3888 100%)',
        'gradient-gold':    'linear-gradient(135deg, #886028 0%, #885040 100%)',
        // Hero and surface gradients — noticeably deep, not pale
        'gradient-hero':    'linear-gradient(145deg, #DAD6EE 0%, #D2DDF0 50%, #D6E8E2 100%)',
        'gradient-warm':    'linear-gradient(135deg, #E8E2D4 0%, #EDEAF8 100%)',
        'gradient-rose':    'linear-gradient(135deg, #EDEAF8 0%, #DDE8F2 100%)',
        'gradient-surface': 'linear-gradient(135deg, #E8E2D4 0%, #E6E2F5 100%)',
      },

      animation: {
        'fade-up':    'fadeUp 0.4s cubic-bezier(0.16,1,0.3,1)',
        'fade-in':    'fadeIn 0.3s ease-out',
        'scale-in':   'scaleIn 0.25s cubic-bezier(0.16,1,0.3,1)',
        'slide-up':   'slideUp 0.35s cubic-bezier(0.16,1,0.3,1)',
        float:        'float 4s ease-in-out infinite',
        'pulse-soft': 'pulseSoft 2s ease-in-out infinite',
        'spin-slow':  'spin 3s linear infinite',
      },

      keyframes: {
        fadeUp: {
          '0%':   { opacity: '0', transform: 'translateY(12px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        fadeIn: {
          '0%':   { opacity: '0' },
          '100%': { opacity: '1' },
        },
        scaleIn: {
          '0%':   { opacity: '0', transform: 'scale(0.94)' },
          '100%': { opacity: '1', transform: 'scale(1)' },
        },
        slideUp: {
          '0%':   { opacity: '0', transform: 'translateY(20px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        float: {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%':      { transform: 'translateY(-8px)' },
        },
        pulseSoft: {
          '0%, 100%': { opacity: '1' },
          '50%':      { opacity: '0.6' },
        },
      },

      transitionTimingFunction: {
        spring: 'cubic-bezier(0.16,1,0.3,1)',
      },
    },
  },
  plugins: [],
} satisfies Config
