const REPO = 'imptype/discord';

const get = (path = '') =>
	fetch(`https://api.github.com/repos/${REPO}${path}`, {
		headers: process.env.GITHUB_TOKEN ? { Authorization: `Bearer ${process.env.GITHUB_TOKEN}` } : {},
	}).then((r) => (r.ok ? r.json() : Promise.reject(r.status)));

async function load() {
	const [repo, release, tags] = (
		await Promise.allSettled([get(), get('/releases/latest'), get('/tags?per_page=1')])
	).map((r) => (r.status === 'fulfilled' ? r.value : undefined));

	return {
		repo: REPO,
		url: `https://github.com/${REPO}`,
		stars: (repo?.stargazers_count ?? null) as number | null,
		forks: (repo?.forks_count ?? null) as number | null,
		version: (release?.tag_name ?? tags?.[0]?.name ?? null) as string | null,
	};
}

// Runs once per build.
let cache: ReturnType<typeof load> | undefined;
export const getRepoStats = () => (cache ??= load());