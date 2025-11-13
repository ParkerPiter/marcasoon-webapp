"use client";
import { useState } from "react";
import Loader from "../Loader";
import toast, {Toaster} from "react-hot-toast";
import { useForm } from 'react-hook-form'
import { ContactFormValues } from '../../interfaces/inputs';

const ContactoPage = () => {
    const [error, setError] = useState<string | null>(null);
    const [loading, setLoading] = useState(false);
    const { register, formState: { errors } } = useForm<ContactFormValues>();

    const sleep = (ms: number) => new Promise(res => setTimeout(res, ms));

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError(null);
        setLoading(true);
        const form = e.target as HTMLFormElement;
        const formData = new FormData(form);
        const data: ContactFormValues = {
            name: formData.get('name') as string,
            email: formData.get('email') as string,
            phone: formData.get('phone') as string || undefined,
            message: formData.get('message') as string,
        };
                try {
            const response = await fetch('/api/contact', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data),
            });
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
                        // Espera 1.5s antes de mostrar el toast tras recibir la respuesta
                        await sleep(1500);
                        toast.success("Tu mensaje ha sido enviado con éxito. ¡Gracias por contactarnos!");
                        form.reset();
        } catch (err: any) {
                    setError("Hubo un error al intentar enviar tu mensaje. Por favor, inténtalo de nuevo.");
                    // Mantener el loader visible y mostrar el toast de error tras 1.5s
                    await sleep(1500);
                    toast.error("No pudimos enviar tu mensaje. Inténtalo nuevamente.");
        } finally {
          setLoading(false);
        }
      };

    return (
    <div className="pt-2">
        <form onSubmit={handleSubmit} className="w-full space-y-4 px-12 ">
            <div>
                <label htmlFor="name" className="block text-sm font-semibold mb-1 text-[#192A56]">Nombre Completo</label>
                <input id="name" className="w-full border border-[#ED5E32] rounded-lg px-3 py-2 focus:outline-none focus:ring-1 focus:ring-[#ED5E32]"  {...register('name', { required: true })} />
                {errors.name && <span>Este campo es obligatorio</span>}
            </div>
            <div>
                <label htmlFor="email" className="block text-sm font-semibold mb-1 text-[#192A56]">Correo Electrónico</label>
                <input id="email" type="email" className="w-full border border-[#ED5E32] rounded-lg px-3 py-2 focus:outline-none focus:ring-1 focus:ring-[#ED5E32]" {...register('email', { required: true })} />
                {errors.email && <span>Este campo es obligatorio</span>}
            </div>
            <div>
                <label htmlFor="phone" className="block text-sm font-semibold mb-1 text-[#192A56]">Teléfono</label>
                <input id="phone" className="w-full border border-[#ED5E32] rounded-lg px-3 py-2 focus:outline-none focus:ring-1 focus:ring-[#ED5E32]" {...register('phone')} />
            </div>
            <div>
                <label htmlFor="message" className="block text-sm font-semibold mb-1 text-[#192A56]">Mensaje</label>
                <textarea id="message" className="w-full border border-[#ED5E32] rounded-lg px-3 py-2 focus:outline-none focus:ring-1 focus:ring-[#ED5E32]" {...register('message', { required: true })} />
                {errors.message && <span>Este campo es obligatorio</span>}
            </div>
            <button type="submit" disabled={loading} className="disabled:opacity-60 disabled:cursor-not-allowed">
                {loading ? <Loader /> : <span className="bg-[#192A56] hover:bg-[#FF6B6B] text-white font-semibold py-3 px-6 rounded-md transition-colors duration-300 hover:cursor-pointer">Enviar Mensaje</span>}
            </button>
            <Toaster position="top-right" />
        </form>
    </div>
    );
}

export default ContactoPage;