// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

// https://astro.build/config

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
      	TableOfContents: './src/components/TableOfContents.astro', // for dynamic page contents on right
        Header: './src/components/Header.astro',
        Sidebar: './src/components/Sidebar.astro',
        MobileMenuFooter: './src/components/Empty.astro',
			},
      customCss: [
        './src/styles/smooth-scroll.css', 
        // './src/styles/luau-theme.css',
        './src/styles/sidebar-layout.css'
      ],
      head: [
        {
          tag: 'script',
          content:
            "try{if(localStorage.getItem('sidebar-collapsed')==='1')document.documentElement.setAttribute('data-sidebar-collapsed','')}catch(e){}",
        },
      ],
			sidebar: [
				{
					label: 'Guides',
					items: [
						// Each item here is one entry in the navigation menu.
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
