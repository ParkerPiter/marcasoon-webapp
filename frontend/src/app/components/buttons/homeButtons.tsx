"use client";

import { MoveRight } from "lucide-react";
import Link from "next/link";

export const HomeButtons = () => {
  return (
    <div className="flex flex-col sm:flex-row gap-4 md:justify-start justify-center mt-8 px-2 md:px-0 md:w-full ">
        <Link
            href="/contact"
            className="bg-[#192A56] hover:bg-[#FF6B6B] text-white font-semibold py-3 px-6 rounded-md transition-colors duration-300 flex items-center justify-center "
        >
            <span>Contáctanos</span>
            <MoveRight className="ml-2" />
        </Link>
    </div>
  );
};
export default HomeButtons;