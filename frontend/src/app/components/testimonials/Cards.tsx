"use client";
import Card from "./Card";
import { testimonials } from '../../../../api/test'

const CardsTestimonial = () =>{
    return(
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {testimonials.map((testimonial) => (
                <Card
                 key={testimonial.id} 
                 name={testimonial.name}
                 testimonial={testimonial.quote}
                 />
            ))}
        </div>
    )
}

export default CardsTestimonial;
