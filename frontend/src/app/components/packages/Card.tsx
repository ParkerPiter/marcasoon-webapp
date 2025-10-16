"use client";

import { CardPrice } from "@/app/interfaces/card";
import {CheckCircle2} from 'lucide-react';

const Card = ( { id, title, includes, description, price, client_objective } : CardPrice) => {
  return (
    <div className="group border border-gray-200 rounded-lg shadow-lg hover:shadow-2xl transition-shadow duration-300 flex flex-col bg-white overflow-hidden">
        <div className="border-t-4 border-[#FF6B6B] group-hover:border-[#192A56] transition-colors duration-300"></div>
        
        <div className="p-6 flex flex-col h-full">
            <p className="text-xl text-center font-semibold text-[#192A56]">Plan {title}</p>
            
            <div className="my-4 flex items-baseline justify-center text-center">
                <span className="text-5xl font-extrabold text-[#FF6B6B]">${price}</span>
                <span className="text-xl font-semibold text-black-500 ml-2">USD</span>
            </div>

            <div className="min-h-[60px] text-center">
                <p className="text-sm text-gray-600">
                    <span className="font-semibold">Ideal para:</span> {client_objetive}
                </p>
            </div>

            <hr className="my-4" />
            
            <div className="flex-grow">
                <ul className="text-sm space-y-3">
                    <span className="font-bold text-black-500">¿Qué incluye?:</span> 
                    {includes.map((item, index) => (
                      <li key={index} className="flex items-start mt-2 gap-2">
                        <CheckCircle2 className="flex-shrink-0 mt-0.5 w-5 h-5 text-[#192A56]" />
                        <span className="text-gray-700">{item}</span>
                      </li>
                    ))}
                </ul>
            </div>

            <div className="mt-auto pt-6">
                <button className="w-full uppercase font-bold bg-[#FF6B6B] text-white py-3 px-4 rounded-lg hover:bg-[#192A56] transition-colors duration-300 hover:cursor-pointer">
                    Select
                </button>
            </div>
        </div>
      </div>
      
  );
};

export default Card;
