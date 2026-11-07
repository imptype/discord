// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

export default defineConfig({
	site: 'https://imptype.github.io',
	base: '/discord',
	markdown: { smartypants: false }, // disables unicode quote chars
	integrations: [
		starlight({
			title: 'iDiscord',
			components: {
				// SocialIcons: './src/components/SocialIcons.astro', // for github top right tag, stars, forks
				// ThemeSelect: './src/components/ThemeSelect.astro', // for toggle day/night top right
				TableOfContents: './src/components/TableOfContents.astro',
				Head: './src/components/Head.astro',
				Header: './src/components/Header.astro',
				Sidebar: './src/components/Sidebar.astro',
				PageTitle: './src/components/PageTitle.astro',
				MobileMenuFooter: './src/components/Empty.astro',
			},
			customCss: [
				'./src/styles/smooth-scroll.css',
				'./src/styles/icon-button.css',
				// './src/styles/luau-theme.css',
				'./src/styles/sidebar-layout.css',
			],
			sidebar: [
				{
					label: 'Guides',
					items: [
						{ label: 'Tutorial', slug: 'guides/tutorial' },
					],
				},
				{
					label: 'Reference',
					items: [{ autogenerate: { directory: 'reference' } }],
				},
				{
					label: 'Test',
					items: [
						{ label: 'NumberGroup', slug: 'test/example' },
					],
				},
			],
		}),
	],
});
