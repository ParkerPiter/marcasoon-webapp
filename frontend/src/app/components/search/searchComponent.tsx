"use client";

import { useState } from "react";
import SearchCards from "./SearchCards";
import type { SearchCard as SearchCardType } from "@/app/interfaces/card";
import { searchTrademarksByName } from "../../../../api/api";

export default function SearchComponent() {
	const [query, setQuery] = useState("");
	const [loading, setLoading] = useState(false);
	const [error, setError] = useState<string | null>(null);
	const [results, setResults] = useState<SearchCardType[]>([]);

	const onSubmit = async (e: React.FormEvent) => {
		e.preventDefault();
		const q = query.trim();
		if (!q) return;
		setLoading(true);
		setError(null);
		try {
			const data = await searchTrademarksByName(q);
			setResults(data);
		} catch (err: any) {
			setError(err?.message || "Error al buscar");
		} finally {
			setLoading(false);
		}
	};

	return (
		<div className="w-full max-w-4xl mx-auto">
			<form onSubmit={onSubmit} className="flex gap-2 mb-6">
				<input
					type="text"
					value={query}
					onChange={(e) => setQuery(e.target.value)}
					placeholder="Buscar marca (ej: google)"
					className="flex-1 border border-gray-300 rounded-md px-4 py-2 focus:outline-none focus:ring-2 focus:ring-[#192A56]"
				/>
				<button
					type="submit"
					disabled={loading || !query.trim()}
					className="bg-[#192A56] hover:bg-[#0f1c3a] text-white font-semibold px-5 py-2 rounded-md disabled:opacity-50"
				>
					{loading ? "Buscando..." : "Buscar"}
				</button>
			</form>

			{error && (
				<div className="text-red-600 text-sm mb-4">{error}</div>
			)}

			<SearchCards items={results} />
		</div>
	);
}
