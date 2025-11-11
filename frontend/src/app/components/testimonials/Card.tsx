"use client";
import { CardTestimonial } from "@/app/interfaces/card";
import { Quote } from 'lucide-react';
import * as FlagIcons from 'country-flag-icons/react/3x2';

const nameToAlpha2: Record<string, string> = {
    US: "US",
    USA: "US",
    "United States": "US",
    "Estados Unidos": "US",
    Colombia: "CO",
};

const resolveCode = (countryName?: string, countryCode?: string) => {
    if (countryCode && countryCode.length === 2) return countryCode.toUpperCase();
    if (countryName) {
        const mapped = nameToAlpha2[countryName.trim()];
        if (mapped) return mapped;
    }
    return undefined;
};

const Card = ({ name, testimonial, logo, countryName, countryCode }: CardTestimonial) => {
    const alpha2 = resolveCode(countryName, countryCode);
    const FlagComp = alpha2 ? (FlagIcons as Record<string, any>)[alpha2] : undefined;
    return (
            <div className="group border border-gray-200 rounded-2xl shadow-md hover:shadow-xl transition-shadow duration-300 bg-[#F9F9F9] overflow-hidden w-full">
                <div className="border-t-4 border-[#FF6B6B] group-hover:border-[#192A56] transition-colors duration-300" />
                <div className="p-6 md:p-10">
                    <div className="grid grid-cols-1 md:grid-cols-2 items-center gap-8">
                        {/* Texto a la izquierda */}
                        <div>
                            <Quote className="w-10 h-10 text-[#FF6B6B] group-hover:text-[#192A56] transition-colors" />
                            <p className="mt-4 text-gray-700 leading-relaxed text-lg">
                                <span className="italic">{testimonial}</span>
                            </p>
                            <div className="mt-6">
                                <p className="text-base font-semibold text-[#111827]">{name}</p>
                                {(countryName || alpha2) && (
                                    <div className="mt-1 flex items-center gap-2 text-sm text-gray-500">
                                        {FlagComp && <FlagComp title={countryName || alpha2} className="w-6 h-4 rounded-sm shadow-sm" />}
                                        <span>{countryName || alpha2}</span>
                                    </div>
                                )}
                            </div>
                        </div>

                        {/* Imagen/logo a la derecha */}
                        <div className="relative flex justify-center md:justify-end">
                            {/* Barras decorativas superior/inferior */}
                            <span aria-hidden className="absolute -top-3 h-2 w-40 bg-[#C4A060] rounded hidden md:block" />
                            <span aria-hidden className="absolute -bottom-3 h-2 w-40 bg-[#C4A060] rounded hidden md:block" />
                            <div className="relative bg-white rounded-xl shadow-xl p-3">
                                {logo ? (
                                    <img src={logo} alt={`${name} logo`} className="w-64 h-64 object-contain rounded-lg" />
                                ) : (
                                    <div className="w-64 h-64 rounded-lg bg-gray-100" />
                                )}
                            </div>
                        </div>
                    </div>
                </div>
                <div className="border-b-4 border-[#FF6B6B] group-hover:border-[#192A56] transition-colors duration-300" />
            </div>
    );
};
export default Card;