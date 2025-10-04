export interface CardPrice {
    id:number,
    title: string,
    description: string;
    client_objetive: string;
    includes: string[];
    price:number;
}

export interface CardTestimonial {
    id:number,
    name: string;
    testimonial: string;
}