"use client";

import Image from "next/image";
import userImg from "../../../../../public/user.png";
import { useState } from "react";
import { loginBasic, loginJWT, storeTokens, setStoredUsername } from "../../../../api/api";

export default function LoginComponent() {
	const [username, setUsername] = useState("");
	const [password, setPassword] = useState("");
	const [loading, setLoading] = useState(false);
	const [error, setError] = useState<string | null>(null);

	const handleSubmit = async (e: React.FormEvent) => {
		e.preventDefault();
		setError(null);
		setLoading(true);
		try {
			// 1) Intento de login básico (puede establecer cookie de sesión o devolver user)
			await loginBasic({ username, password });

			// 2) Obtener tokens JWT (si el flujo usa SimpleJWT)
			const tokens = await loginJWT({ username, password });
					storeTokens(tokens, true);
					setStoredUsername(username, true);
					if (typeof window !== 'undefined') {
						window.dispatchEvent(new CustomEvent('auth-changed', { detail: { authed: true } }));
					}

			// Aquí podrías redirigir a dashboard o cerrar modal, etc.
		} catch (err: any) {
			setError(err?.message || "Error al iniciar sesión");
		} finally {
			setLoading(false);
		}
	};

	return (
		<div className="max-w-md w-[92vw] sm:w-[80vw] md:w-[70vw] lg:w-[420px] mx-auto bg-white rounded-2xl shadow p-6">
			<div className="flex flex-col items-center mb-6">
				<div className="w-20 h-20 relative mb-3">
					<Image src={userImg} alt="user" fill className="object-contain rounded-full" />
				</div>
				<h3 className="text-xl font-semibold">Inicia sesión</h3>
				<p className="text-xs text-gray-500">Ingresa con tu usuario y contraseña</p>
			</div>

			<form onSubmit={handleSubmit} className="space-y-4">
				<div>
					<label className="block text-sm font-medium mb-1">Usuario</label>
					<input
						type="text"
						className="w-full border rounded-lg px-3 py-2 focus:outline-none focus:ring-1 focus:ring-[#ED5E32]"
						value={username}
						onChange={(e) => setUsername(e.target.value)}
						required
					/>
				</div>
				<div>
					<label className="block text-sm font-medium mb-1">Contraseña</label>
					<input
						type="password"
						className="w-full border rounded-lg px-3 py-2 focus:outline-none focus:ring-1 focus:ring-[#ED5E32]"
						value={password}
						onChange={(e) => setPassword(e.target.value)}
						required
					/>
				</div>

				{error && <p className="text-sm text-red-600">{error}</p>}

				<button
					type="submit"
					disabled={loading}
					className="w-full bg-[#ED5E32] text-white py-2 rounded-lg font-semibold hover:opacity-90 disabled:opacity-60"
				>
					{loading ? "Ingresando..." : "Ingresar"}
				</button>
			</form>
		</div>
	);
}

