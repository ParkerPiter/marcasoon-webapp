"use client";

import { CardService } from "@/app/interfaces/card";
import { Asterisk } from 'lucide-react';
type Props = CardService;

const Card = ({ id, title, bullets }: Props) => {
  return (
    <div className="group border border-gray-200 rounded-lg shadow-lg hover:shadow-2xl transition-shadow duration-300 flex flex-col bg-white overflow-hidden">
        <div className="border-t-4 border-[#FF6B6B] group-hover:border-[#192A56] transition-colors duration-300"></div>
        
        <div className="p-6 flex flex-col h-full">
            <p className="text-xl text-center font-semibold text-[#192A56]">{title}</p>
            <hr className="my-4" />
            <div className="flex-grow">
                <ul className="text-sm space-y-3">
                    {bullets.map((item, index) => (
                      <li key={index} className="flex items-start mt-2 gap-2">
                        <Asterisk className="flex-shrink-0 mt-0.5 w-5 h-5 text-[#192A56]" />
                        <span className="text-gray-700">{item}</span>
                      </li>
                    ))}
                </ul>
            </div>

            <div className="mt-auto pt-6">
                <button
                    className="w-full uppercase font-bold bg-[#FF6B6B] text-white py-3 px-4 rounded-lg hover:bg-[#192A56] transition-colors duration-300 hover:cursor-pointer"
                    onClick={() => {
                        // Aquí puedes abrir un modal de contacto o navegar a details del servicio
                        // e.g., router.push('/contact')
                    }}
                >
                    Saber más
                </button>
            </div>
        </div>
      </div>
      
  );
};

export default Card;
