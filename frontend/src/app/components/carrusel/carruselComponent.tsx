"use client";
import { carrusel } from "../../../../api/test";
import Image from "next/image";

const CarruselComponent = () => {
    // Duplicamos el arreglo para un bucle perfecto (la animación mueve el 50%)
    const items = [...carrusel, ...carrusel];

    return (
        <div className="w-full marquee py-4 ">
            <div className="marquee-track items-center">
                {items.map((item, idx) => (
                    <div key={`${item.id}-${idx}`} className="flex-shrink-0 px-8">
                        <Image
                            src={item.url}
                            alt={`Logo ${item.id}`}
                            width={140}
                            height={80}
                            className="object-contain opacity-80 hover:opacity-100 transition-opacity duration-300"
                        />
                    </div>
                ))}
            </div>
        </div>
    );
};

export default CarruselComponent;