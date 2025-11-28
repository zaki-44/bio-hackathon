# Vite React + shadcn/ui

A modern React starter template with Vite, TypeScript, and shadcn/ui components.

## Features

- ⚡ Vite for fast development and building
- ⚛️ React 18 with TypeScript
- 🎨 Tailwind CSS for styling
- 🧩 shadcn/ui components
- 🔥 Hot Module Replacement (HMR)
- 📦 ESLint for code quality
- 🎯 Path aliases with `@/` prefix

## Getting Started

1. Install dependencies:
   ```bash
   npm install
   ```

2. Start the development server:
   ```bash
   npm run dev
   ```

3. Open your browser and navigate to `http://localhost:5173`

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

## Project Structure

```
src/
├── components/
│   └── ui/           # shadcn/ui components
├── lib/
│   └── utils.ts      # Utility functions
├── App.tsx           # Main app component
├── main.tsx          # App entry point
└── index.css         # Global styles with Tailwind
```

## Adding More shadcn/ui Components

To add more shadcn/ui components, you can use the shadcn CLI:

```bash
npx shadcn-ui@latest add [component-name]
```

For example:
```bash
npx shadcn-ui@latest add input
npx shadcn-ui@latest add select
npx shadcn-ui@latest add dialog
```
