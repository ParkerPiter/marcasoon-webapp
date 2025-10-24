"use client";

import Image from "next/image";
import Link from "next/link";
import { CardBlog } from "@/app/interfaces/card";

const BlogCard = ({ blog }: { blog: CardBlog }) => {
  const imgSrc = blog.image ?? "/blog1.jpg";
  return (
    <article className="group relative overflow-hidden rounded-xl border border-gray-200 bg-white shadow-sm hover:shadow-md transition-shadow">
      {/* Bordes laterales al estilo testimonials pero en izquierda/derecha */}
      <div
        aria-hidden
        className="pointer-events-none absolute left-0 top-0 h-full w-1 bg-[#FF6B6B] group-hover:bg-[#192A56] transition-colors duration-300"
      />
      <div
        aria-hidden
        className="pointer-events-none absolute right-0 top-0 h-full w-1 bg-[#FF6B6B] group-hover:bg-[#192A56] transition-colors duration-300"
      />
      <Link href={`/blog/${blog.id}`} className="block">
        <div className="relative w-full aspect-[16/9] bg-gray-100">
          {/* Nota: usando next/image para optimización */}
          <Image src={imgSrc} alt={blog.title} fill className="object-cover" />
        </div>
        <div className="p-4">
          <h3 className="text-lg font-semibold text-gray-900 group-hover:text-[#192A56] transition-colors">
            {blog.title}
          </h3>
        </div>
      </Link>
    </article>
  );
};

export default BlogCard;
