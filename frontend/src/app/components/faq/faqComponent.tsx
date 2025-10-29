"use client";

import { useState } from "react";
import { ChevronDown, ChevronUp } from "lucide-react";
import { FaqItem, FaqProps } from "../../interfaces/card";
import Button from "../buttons/faqsButton";


const FaqComponent = ({
	title = "FAQs - Preguntas Frecuentes",
	subtitle = "Blindando Tu Marca: El Camino Legal",
	items,
	defaultOpenIndex = 0,
}: FaqProps) => {
	const [openIndex, setOpenIndex] = useState<number | null>(
		items.length ? defaultOpenIndex : null
	);

	const toggle = (idx: number) => {
		setOpenIndex((prev) => (prev === idx ? null : idx));
	};

	return (
		<section className="w-full py-10">
			<div className="container mx-auto px-4 grid grid-cols-1 md:grid-cols-3 gap-8">
				{/* Columna izquierda: título y subtítulo */}
				<div>
					<h2 className="text-3xl font-bold text-gray-900 mb-2">
						{title}
					</h2>
					<p className="text-gray-600">
						{subtitle}
					</p>
					<Button />
				</div>

				{/* Columna derecha: acordeón */}
				<div className="md:col-span-2 space-y-4">
					{items.map((item, idx) => {
						const isOpen = openIndex === idx;
						return (
							<div
								key={idx}
								className="border border-gray-200 rounded-sm bg-[#f8fafc]"
							>
								<button
									className="w-full text-left px-6 py-4 font-semibold text-gray-900 flex items-center justify-between hover:cursor-pointer"
									onClick={() => toggle(idx)}
									aria-expanded={isOpen}
									aria-controls={`faq-panel-${idx}`}
								>
									<span>
										{idx + 1}. {item.question}
									</span>
									{isOpen ? (
										<ChevronUp className="w-5 h-5 text-gray-700" />
									) : (
										<ChevronDown className="w-5 h-5 text-gray-700" />
									)}
								</button>
											{/* Panel con transición suave usando grid-rows */}
											<div
												id={`faq-panel-${idx}`}
												aria-hidden={!isOpen}
												className={`grid transition-all duration-300 ease-in-out ${
													isOpen ? "grid-rows-[1fr] opacity-100" : "grid-rows-[0fr] opacity-0"
												}`}
											>
												<div className="overflow-hidden px-6 pb-5 text-gray-700">
													{item.answer}
												</div>
											</div>
							</div>
						);
					})}
				</div>
			</div>
		</section>
	);
};

export default FaqComponent;

