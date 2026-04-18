import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig(() => {
  const repo = process.env.GITHUB_REPOSITORY?.split('/')[1];
  const owner = process.env.GITHUB_REPOSITORY_OWNER;
  const isProjectPagesRepo =
    !!repo &&
    !!owner &&
    repo.toLowerCase() !== `${owner}.github.io`.toLowerCase();

  return {
    base: isProjectPagesRepo ? `/${repo}/` : '/',
    plugins: [react()],
  };
});
