import type { ButtonHTMLAttributes } from "react";

type Variant = "primary" | "secondary" | "link";

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: Variant;
}

const VARIANT_CLASSES: Record<Variant, string> = {
  primary: "rounded-md px-4 py-2.5 text-sm font-medium bg-brand-purple text-white hover:bg-brand-purple-dark disabled:opacity-50",
  secondary:
    "rounded-md px-4 py-2.5 text-sm font-medium bg-zinc-900 text-white hover:bg-zinc-700 disabled:opacity-50 dark:bg-zinc-50 dark:text-zinc-900 dark:hover:bg-zinc-200",
  link: "text-sm font-medium text-brand-blue hover:underline",
};

export default function Button({ variant = "primary", className = "", ...props }: ButtonProps) {
  return <button className={`${VARIANT_CLASSES[variant]} ${className}`} {...props} />;
}
