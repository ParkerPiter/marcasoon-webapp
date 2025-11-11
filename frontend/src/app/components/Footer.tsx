"use client";

import LogoComponent from "./LogoComponent";
import { Facebook, Mail, Instagram, Send } from "lucide-react";
import Link from "next/link";

const Footer = () => {
	return (
		<footer className="mt-16 text-white">
			{/* Main area */}
			<div className="bg-[var(--blue-color)]">
				<div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-12 grid grid-cols-1 md:grid-cols-3 gap-10">
					{/* Brand + about */}
					<div>
						<div className="mb-4">
							<LogoComponent />
						</div>
						<p className="text-gray-200/90 text-sm leading-relaxed max-w-md">
							Detrás de la palabra, lejos de los países Vokalia y Consonantia,
							viven los textos ciegos. Se separan en Bookmarksgrove cerca de la
							costa.
						</p>

						<div className="mt-6 flex items-center gap-3">
							{[Facebook, Instagram, Mail].map((Icon, i) => (
								<a
									href="#"
									key={i}
									className="inline-flex h-9 w-9 items-center justify-center rounded-full ring-1 ring-white/30 hover:ring-white/60 hover:bg-[#FF6B6B] transition"
									aria-label="social-link"
								>
									<Icon className="h-5 w-5 text-white" />
								</a>
							))}
						</div>
					</div>

					{/* Useful links */}
					<div>
						<h3 className="text-lg font-semibold mb-4">Enlaces útiles</h3>
						<ul className="space-y-3 text-gray-200/90">
							<li>
								<Link href="/contact" className="hover:text-white">Contacto</Link>
							</li>
							<li>
								<Link href="/blog" className="hover:text-white">Blog</Link>
							</li>
							<li>
								<Link href="/servicios#registro" className="hover:text-white">Registro de Marca</Link>
							</li>
							<li>
								<Link href="/about" className="hover:text-white">Sobre nosotros</Link>
							</li>
						</ul>
					</div>

					{/* Subscribe */}
					<div>
						<h3 className="text-lg font-semibold mb-2">Suscríbete</h3>
						<p className="text-gray-200/90 text-sm mb-4">
							No te pierdas nuestras novedades. ¡Suscríbete hoy!
						</p>

						<form
							onSubmit={(e) => e.preventDefault()}
							className="relative flex items-center"
						>
							<input
								type="email"
								required
								placeholder="Tu correo aquí"
								className="w-full rounded-full bg-white text-gray-800 placeholder:text-gray-500 py-3 pl-5 pr-14 outline-none"
							/>
							<button
								type="submit"
								className="absolute right-1 inline-flex items-center justify-center rounded-full bg-[var(--oragange-color)] hover:bg-[#e85f5f] text-white h-10 w-10"
								aria-label="Enviar"
							>
								<Send className="h-5 w-5" />
							</button>
						</form>
					</div>
				</div>
			</div>

			{/* Bottom bar */}
			<div className="bg-[#ED5E32]">
				<div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-3 flex flex-col md:flex-row items-center justify-between text-sm">
					<p className="opacity-95">© {new Date().getFullYear()} Marcasoon. Todos los derechos reservados.</p>
					<div className="flex gap-4 mt-2 md:mt-0">
						<Link href="/terminos-privacidad" className="hover:underline">Términos</Link>
						<Link href="/terminos-privacidad" className="hover:underline">Privacidad</Link>
						<Link href="#" className="hover:underline">Cookies</Link>
					</div>
				</div>
			</div>
		</footer>
	);
};

export default Footer;

