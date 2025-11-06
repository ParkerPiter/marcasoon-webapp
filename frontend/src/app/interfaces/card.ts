export interface CardPrice {
    id:number,
    title: string,
    description: string;
    client_objective: string;
    includes: string[];
    //price: { amount: number, currency: string };
    price: number;
}

export interface CardBlog {
    id:number,
    title: string,
    summary: string;
    image?: string;
}

export interface CardService {
    id:number,
    title: string,
    bullets: string[];
}

export interface CardTestimonial {
    id:number,
    name: string;
    testimonial: string;
    logo?: string;
    countryName?: string;
    countryCode?: string; 
}

export interface FaqItem {
    question: string;
    answer: string;
}

export interface FaqProps {
    title?: string;
    subtitle?: string;
    items: FaqItem[];
    defaultOpenIndex?: number;
}
export interface SearchCard {
    logo: string; // URL de la imagen del logo
    liveOrDeadStatus: "Live" | "Dead"; // estado de la marca
    correspondenceName: string; // nombre del corresponsal
    transactionDate: string; // fecha (YYYY-MM-DD)
}
