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
    <div className="group border border-gray-200 rounded-lg shadow-lg hover:shadow-2xl transition-shadow duration-300 flex flex-col bg-white overflow-hidden w-full">
            <div className="border-t-4 border-[#FF6B6B] group-hover:border-[#192A56] transition-colors duration-300" />
            <div className="p-6 flex flex-col h-full">
                <blockquote className="text-gray-700 italic leading-relaxed text-center mb-4">
                    <Quote className="inline-block w-5 h-5 mr-1 text-[#FF6B6B] align-text-top group-hover:text-[#192A56] transition-colors duration-300" />
                    {testimonial}
                </blockquote>
                <div className="mt-0 pt-2">
                    {logo && (
                        <div className="flex justify-center mb-4">
                            <img src={logo} alt={`${name} logo`} className="h-36 w-36 object-contain rounded-3xl" />
                            
                        </div>
                    )}
                    <p className="text-lg font-semibold text-center text-[#192A56] tracking-wide">
                        {name}
                    </p>
                    {(countryName || alpha2) && (
                        <div className="mt-1 flex items-center justify-center gap-2 text-sm text-gray-600">
                            {FlagComp && (
                                <FlagComp title={countryName || alpha2} className="w-6 h-4 rounded-sm shadow-sm" />
                            )}
                            <span>{countryName || alpha2}</span>
                        </div>
                    )}
                </div>
            </div>
            <div className="border-b-4 border-[#FF6B6B] group-hover:border-[#192A56] transition-colors duration-300" />
        </div>
    );
};
export default Card;