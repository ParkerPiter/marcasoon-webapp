"use client";

import Image from "next/image";
import { CardBlog } from "@/app/interfaces/card";

const BlogDetails = ({ blog }: { blog: CardBlog }) => {
  const imgSrc = blog.image ?? "/blog1.jpg";
  // Renderizamos el summary respetando saltos de línea con white-space
  return (
    <article className="mx-auto max-w-3xl bg-white">
      <header className="mb-6">
        <h1 className="text-3xl font-bold text-gray-900">{blog.title}</h1>
      </header>
      <div className="relative w-full aspect-[16/9] bg-gray-100 rounded-lg overflow-hidden mb-6">
        <Image src={imgSrc} alt={blog.title} fill className="object-cover" />
      </div>
      <section>
        <p className="whitespace-pre-line text-gray-800 leading-relaxed">{blog.summary}</p>
      </section>
    </article>
  );
};

export default BlogDetails;
