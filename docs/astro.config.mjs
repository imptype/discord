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
				SocialIcons: './src/components/SocialIcons.astro', // for github top right tag, stars, forks
      	ThemeSelect: './src/components/ThemeSelect.astro', // for toggle day/night top right
			},
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
