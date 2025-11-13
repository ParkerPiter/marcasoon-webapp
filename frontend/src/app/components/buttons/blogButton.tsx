"use client";

import { MoveRight } from "lucide-react";
import Link from "next/link";

export const BlogButtons = () => {
  return (
    <div className="flex flex-col sm:flex-row gap-4 md:justify-start justify-center mt-8 px-2 md:px-0 md:w-full ">
        <Link
            href="/blog"
            className="bg-[#FF6B6B] hover:bg-[#FF6B6B] text-white font-semibold py-3 px-6 rounded-md transition-colors duration-300 flex items-center justify-center "
        >
            <span>Leer más</span>
            <MoveRight className="ml-2" />
        </Link>
    </div>
  );
};
export default BlogButtons;