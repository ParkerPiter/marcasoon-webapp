"use client";
import { CardTestimonial } from "@/app/interfaces/card";
import { Quote } from 'lucide-react';
import Image from "next/image";

const Card = ({ name, testimonial, logo }: CardTestimonial) => {
    return (
        <div className="group border border-gray-200 rounded-lg shadow-lg hover:shadow-2xl transition-shadow duration-300 flex flex-col bg-white overflow-hidden">
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
                    <p className="text-sm font-semibold text-center text-[#192A56] tracking-wide">
                        {name}
                    </p>
                </div>
            </div>
            <div className="border-b-4 border-[#FF6B6B] group-hover:border-[#192A56] transition-colors duration-300" />
        </div>
    );
};
export default Card;