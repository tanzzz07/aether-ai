import { defineConfig } from 'eslint-define-config';

export default defineConfig([
  {
    ignores: ['.next/**'],
  },
  {
    files: ['**/*.{ts,tsx}'],
    languageOptions: {
      ecmaVersion: 'latest',
      sourceType: 'module',
    },
    rules: {},
  },
]);