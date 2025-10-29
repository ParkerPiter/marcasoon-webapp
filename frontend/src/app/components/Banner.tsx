"use client";

import Image from "next/image";
import banner from '../../../public/arte1.png';
import Link from "next/link";

const Banner = () => {
  return (
    <div className="relative w-full h-[48vh] md:h-[100vh] mb-0">
        <Image
            src={banner}
            alt="Banner"
            fill
            className="object-cover"
        />
        {/* <div className="absolute inset-0  bg-opacity-20 flex flex-col items-center justify-center text-center text-white px-4">
            <h1 className="text-3xl md:text-5xl font-bold mb-4">Protege tu marca con MarcaSoon</h1>
            <Link href="/contact" className="mt-4 inline-block bg-[#FF6B6B] hover:bg-[#192A56] text-white font-semibold py-2 px-4 rounded">
                Contáctanos
            </Link>
        </div> */}
    </div>
  );
};

export default Banner;