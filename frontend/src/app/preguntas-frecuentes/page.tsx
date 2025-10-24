"use client";
import FaqComponent from "../components/faq/bigFaqComponent";

export default function FaqsPage() {
    return (
        <div>
            <FaqComponent
                title="Preguntas Frecuentes"
                subtitle="Resuelve tus dudas más comunes sobre nuestros servicios y procesos."
                items={[
          {
            question: "¿Qué es una marca y por qué es tan importante para mi negocio?",
            answer: "Tu marca es la identidad de tu negocio: es tu nombre, logo y todo lo que te hace único. Registrarla es el único camino para protegerla legalmente en el mercado, asegurando que nadie más pueda copiar o robar tu idea. Es la base fundamental para construir una empresa segura, respetada y con valor."
          },
          {
            question: "¿La protección de mi marca aplica a nivel mundial?",
            answer: "El registro de una marca es territorial, lo que significa que la protección inicial es válida solo en el país donde se registra. Sin embargo, a través del Protocolo de Madrid, te facilitamos un solo trámite para que puedas registrar tu marca en múltiples países a la vez, incluyendo EE. UU., de manera eficiente."
          },
          {
            question: "¿Mi registro es un proceso rápido?",
            answer: "El proceso de registro con la USPTO (la oficina de marcas de EE. UU.) suele tomar entre 8 y 12 meses. Nuestra misión es guiarte para que el camino sea lo más rápido y fluido posible, minimizando demoras y obstáculos gracias a nuestra experiencia."
          },
          {
            question: "¿Cómo puedo saber si mi marca está disponible para registro?",
            answer: "La única forma segura es a través de una búsqueda profesional y profunda. Evitar una búsqueda adecuada es el error más común y la causa principal de rechazos. Nosotros realizamos un análisis exhaustivo en las bases de datos oficiales para identificar cualquier marca idéntica o similar que pueda representar un riesgo. Con nuestro informe, tomas la mejor decisión."
          },
            {
            question: '¿Qué son las "Clases de Niza" y por qué debo elegir la correcta?',
            answer: 'La Clasificación de Niza es un sistema internacional que agrupa productos y servicios en 45 categorías (o "clases"). Es la base para tu solicitud de registro. Es vital elegirlas correctamente porque tu marca solo estará protegida legalmente para los productos o servicios específicos que declares. Si no incluyes una clase importante para tu negocio, podrías dejar una puerta abierta a que un competidor use tu marca en ese sector. Nosotros te asesoramos para elegir las clases adecuadas que blinden tu negocio completamente.'
          },
            {
            question: "¿Qué pasa si mi marca ya está registrada?",
            answer: "Si tu marca no está disponible, no es el final. Te asesoraremos para encontrar la mejor alternativa legal. Podemos ayudarte a modificarla o a crear una nueva que sea única y viable, para que puedas seguir adelante con tu negocio sin tener que empezar de cero."
          },
            {
            question: "¿Qué incluye el servicio de Marcasoon?",
            answer: "Nuestro servicio es integral. No solo nos encargamos del papeleo. Te ofrecemos una asesoría completa que incluye la búsqueda inicial de viabilidad, la preparación y presentación de la solicitud, y el monitoreo de tu marca durante todo el proceso ante la USPTO."
          },
            {
            question: "¿Cómo funciona la Garantía de Éxito?",
            answer: "Creemos firmemente en nuestro trabajo. Si tu marca es rechazada por un error de nuestra parte en la solicitud o en la asesoría, te devolvemos el 100% de nuestros honorarios profesionales. Tu inversión está protegida, dándote total tranquilidad."
          },
            {
            question: "¿El costo del servicio incluye las tarifas del gobierno?",
            answer: "No. El costo de nuestro servicio profesional cubre nuestra asesoría y gestión experta. Las tarifas gubernamentales de la USPTO o de la OMPI son un pago separado que se gestiona directamente a las oficinas. Te daremos un desglose transparente de todos los costos."
          },
            {
            question: "¿Qué pasa después del registro? ¿Tengo que renovar mi marca?",
            answer: "¡Absolutamente! El registro de una marca en EE. UU. (USPTO) es válido por 10 años, pero debes presentar una Declaración de Uso (Secciones 8 y 15) entre el quinto y sexto año para mantenerla activa. Si no se presenta, tu marca se cancela. Dentro de nuestro servicio, te monitoreamos y te notificamos con suficiente tiempo para que nunca pierdas tu protección."
          },
          {
            question: "¿Qué me diferencia de otros servicios de registro de marca?",
            answer: "No somos solo un portal automatizado. Somos tu aliado. Te damos la tranquilidad de estar en manos de expertos que entienden tanto el proceso legal complejo como tu cultura de negocio. Nuestro objetivo es que tu marca se convierta en un activo fuerte, seguro y respetado, no solo en un certificado."
          }
            ]}
        />
    </div>
    );
}