import { blogs } from "../../../../api/test";
import BlogDetails from "@/app/components/blog/Details";
import { CardBlog } from "@/app/interfaces/card";

interface Props {
  params: Promise<{ id: string }>;
}

export default async function BlogDetailPage({ params }: Props) {
  const { id } = await params;
  const numId = Number(id);
  const list: CardBlog[] = blogs as unknown as CardBlog[];
  const blog = list.find((b) => b.id === numId);

  if (!blog) {
    return (
      <main className="container mx-auto px-4 py-16">
        <h1 className="text-2xl font-semibold text-gray-800">Blog no encontrado</h1>
        <p className="text-gray-600 mt-2">El artículo que buscas no existe o fue movido.</p>
      </main>
    );
  }

  return (
    <main className="container mx-auto px-4 py-8">
      <BlogDetails blog={blog} />
    </main>
  );
}
