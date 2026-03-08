import emailjs from "@emailjs/browser";

type ContactPayload = {
  name: string;
  email: string;
  text: string;
};

const serviceId = import.meta.env.VITE_EMAILJS_SERVICE_ID;
const templateId = import.meta.env.VITE_EMAILJS_TEMPLATE_ID;
const publicKey = import.meta.env.VITE_EMAILJS_PUBLIC_KEY;

export const sendContactMessage = async (payload: ContactPayload): Promise<void> => {
  if (!serviceId || !templateId || !publicKey) {
    throw new Error("EMAILJS_NOT_CONFIGURED");
  }

  await emailjs.send(
    serviceId,
    templateId,
    {
      name: payload.name,
      email: payload.email,
      text: payload.text,
    },
    {
      publicKey,
    },
  );
};
