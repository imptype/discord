export interface Param {
	name?: string;
	type?: string;
	default?: string;
	doc?: string;
}

// Must match MODULE in scripts/genapi.py. Module level functions and decorators use it as their `of`.
const MODULE = 'discord';

const esc = (s: string) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

/** Escapes text and turns `code` into <code>. */
export const fmtInline = (s: string) => esc(s).replace(/`([^`]+)`/g, '<code>$1</code>');

/** Colours every identifier in a type like list[float]. */
export const fmtType = (s: string) =>
	s.replace(/([A-Za-z_][\w.]*)|([^A-Za-z_]+)/g, (_, id, rest) =>
		id ? `<span class="py-cls">${id}</span>` : esc(rest),
	);

/** Colours a default value: strings, numbers, everything else (None, True, ...). */
export const fmtValue = (v: string) => {
	const c = /^["']/.test(v) ? 'py-str' : /^-?[\d.]/.test(v) ? 'py-num' : 'py-kw';
	return `<span class="${c}">${esc(v)}</span>`;
};

const sigParams = (params: Param[]) =>
	params
		.map((p) => `<span class="py-var">${p.name}</span>${p.default ? ` = ${fmtValue(p.default)}` : ''}`)
		.join(', ');

export const classSig = (name: string, params: Param[]) =>
	`<span class="py-kw">class</span> <span class="py-cls py-name">${name}</span>(${params.length ? `<em>${sigParams(params)}</em>` : ''})`;

export function memberSig(m: { of: string; name: string; kind: string; type?: string; params: Param[]; returns?: Param }) {
	if (m.kind === 'attr') {
		return `${m.of}.<span class="py-var py-name">${m.name}</span>${m.type ? `: <em>${fmtType(m.type)}</em>` : ''}`;
	}
	// 'deco' is a function meant to be used as @discord.name, so it gets an @ in front instead of a keyword.
	const prefix =
		m.kind === 'async'
			? '<span class="py-ctl">await</span> '
			: m.kind === 'cls'
				? '<span class="py-kw">classmethod</span> '
				: m.kind === 'deco'
					? '<span class="py-fn">@</span>'
					: '';
	// The module name (discord) is coloured like a class name, as in VS Code. Class names stay plain.
	const owner = m.of === MODULE ? `<span class="py-cls">${m.of}</span>` : m.of;
	const args = m.params.length ? `<em>${sigParams(m.params)}</em>` : '';
	const ret = m.returns?.type ? ` -&gt; <em>${fmtType(m.returns.type)}</em>` : '';
	return `${prefix}${owner}.<span class="py-fn py-name">${m.name}</span>(${args})${ret}`;
}
