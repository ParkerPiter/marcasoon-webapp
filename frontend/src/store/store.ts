import { getPlansAPI } from "../../api/api";
import type { CardPrice } from "@/app/interfaces/card";

export const PLANS_MIN_SPINNER_MS = 1200;
export const PLANS_FETCH_TIMEOUT_MS = 20000;

export async function loadPlansEnsuringDelay(
	minDelayMs: number = PLANS_MIN_SPINNER_MS,
	timeoutMs: number = PLANS_FETCH_TIMEOUT_MS
): Promise<{ data: CardPrice[]; error: string | null }> {
	const start = Date.now();
	const controller = new AbortController();
	const timerAbort = setTimeout(() => controller.abort("timeout"), timeoutMs);

	let data: CardPrice[] = [];
	let error: string | null = null;
	try {
		data = await getPlansAPI(undefined, { signal: controller.signal });
	} catch (e: any) {
		error = e?.name === "AbortError"
			? "La solicitud excedió el tiempo de espera."
			: (e?.message || "Error cargando planes");
	} finally {
		clearTimeout(timerAbort);
		const elapsed = Date.now() - start;
		const wait = Math.max(0, minDelayMs - elapsed);
		if (wait > 0) await new Promise((r) => setTimeout(r, wait));
	}

	return { data, error };
}
