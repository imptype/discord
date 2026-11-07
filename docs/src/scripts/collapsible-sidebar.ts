// Collapse / peek / pin behaviour shared by the left sidebar and the right one (TOC).
// Flips data-{name}-collapsed and data-{name}-peek on <html>; the CSS does the sliding.

interface Options {
	name: string;
	storageKey: string;
	toggle: string;
	pane: () => HTMLElement | null;
	media: string;
	edge: 'left' | 'right';
	edgeSize?: number;
	closeDelay?: number;
}

export function setupCollapsibleSidebar({
	name,
	storageKey,
	toggle,
	pane,
	media,
	edge,
	edgeSize = 6,
	closeDelay = 150,
}: Options) {
	const root = document.documentElement;
	const active = matchMedia(media);
	const collapsedAttr = `data-${name}-collapsed`;
	const peekAttr = `data-${name}-peek`;

	let closeTimer = 0;
	const cancelClose = () => {
		clearTimeout(closeTimer);
		closeTimer = 0;
	};
	const peek = (on: boolean) => {
		cancelClose();
		root.toggleAttribute(peekAttr, on);
	};
	const scheduleClose = () => {
		if (closeTimer) return;
		closeTimer = window.setTimeout(() => {
			closeTimer = 0;
			peek(false);
		}, closeDelay);
	};

	document.addEventListener('click', (event) => {
		if (!(event.target as Element).closest(toggle)) return;
		if (root.hasAttribute(collapsedAttr)) root.removeAttribute(collapsedAttr);
		else root.setAttribute(collapsedAttr, '');
		peek(false);
		try {
			localStorage.setItem(storageKey, root.hasAttribute(collapsedAttr) ? '1' : '0');
		} catch {}
	});

	document.addEventListener('mousemove', (event) => {
		if (!active.matches || !root.hasAttribute(collapsedAttr)) return;
		// clientWidth excludes the page scrollbar
		const atEdge = edge === 'left' ? event.clientX <= edgeSize : event.clientX >= root.clientWidth - edgeSize;
		if (atEdge) {
			peek(true);
		} else if (root.hasAttribute(peekAttr)) {
			const r = pane()?.getBoundingClientRect();
			const inside =
				!!r && event.clientX >= r.left && event.clientX <= r.right && event.clientY >= r.top && event.clientY <= r.bottom;
			if (inside) cancelClose();
			else scheduleClose();
		}
	});
	document.addEventListener('mouseleave', () => {
		if (root.hasAttribute(peekAttr)) scheduleClose();
	});
}
