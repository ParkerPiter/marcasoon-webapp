"use client";

import { CardPrice } from "@/app/interfaces/card";
import {Check} from 'lucide-react';

const Card = ( { id, title, includes, description, price, client_objetive } : CardPrice) => {
  return (
    <div className="border border-gray-300 rounded-lg p-6 shadow-md shadow-[#192a5667] hover:shadow-2xl transition-shadow duration-300 flex flex-col">
        <p className="text-xl" ><span className="font-bold">Plan</span> {title}</p>
        <div className="flex flex-col  h-full">
            <div>
                <div className="my-4 min-h-[60px] flex items-center justify-center">
                    <p className="text-3xl font-bold text-center text-[#192A56]" >${price} <span className="text-[#FF6B6B]">USD</span></p>
                </div>
                <div className="min-h-[80px]">
                    <p className="text-sm" ><span className="font-bold">Ideal para:</span> {client_objetive}</p>
                </div>
            </div>
            
            <div className="min-h-[200px]">
                <ul className="text-sm space-y-2" ><span className="font-bold">¿Qué incluye?:</span> 
                    {includes.map((item, index) => (
                      <li key={index} className="flex items-start gap-1">
                        <Check className="flex-shrink-0 mt-1 w-5 h-5 text-[#FF6B6B]" />
                        <span>{item}</span>
                      </li>
                    ))}
                </ul>
            </div>
            <div className="mt-auto flex justify-center w-full">
                <button className="w-full uppercase font-bold mt-4 button bg-[#FF6B6B] text-white py-2 px-4 rounded hover:cursor-pointer hover:bg-[#192A56]">Adquirir</button>
            </div>
            
        </div>
      </div>
      
  );
};

export default Card;
