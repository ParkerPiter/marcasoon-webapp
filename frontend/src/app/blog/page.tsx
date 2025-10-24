import BlogCards from "../components/blog/Cards";

export default function BlogPage() {
  return (
    <main className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-6 text-gray-900">Blog</h1>
      <BlogCards />
    </main>
  );
}
