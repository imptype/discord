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
				TableOfContents: './src/components/TableOfContents.astro', // dynamic right sidebar
				Head: './src/components/Head.astro', // helps decide right sidebar and collapse state
				Header: './src/components/Header.astro', // replaces top bar
				Sidebar: './src/components/Sidebar.astro', // custom left sidebar (search under 
                                                   // title, github button, daynight, bottom)
				PageTitle: './src/components/PageTitle.astro', // breadcrumb at top of doc pages
				MobileMenuFooter: './src/components/Empty.astro', // disable default mobile footer (dupes daynight)
			},
			customCss: [
				'./src/styles/smooth-scroll.css', // make header jumps scroll smoothly than teleport
				'./src/styles/icon-button.css', // reused icon buttons, daynight, hide sidebar
				// './src/styles/luau-theme.css', // maybe a theme in the future
				'./src/styles/sidebar-layout.css', // defines layout for sidebars, index, etc
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
					items: [ // shows what full api classes could look like
						{ label: 'NumberGroup', slug: 'test/example' },
					],
				},
			],
		}),
	],
});
