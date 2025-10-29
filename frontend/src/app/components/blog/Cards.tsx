"use client";

import { blogs } from '../../../../api/test';
import BlogCard from './Card';

const BlogCards = () => {
	return (
		<div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 md:px-22 px-6">
			{blogs.map((b) => (
				<BlogCard key={b.id} blog={b} />
			))}
		</div>
	);
};

export default BlogCards;