import Image from "next/image"
import { robotoMono } from "../fonts"

export default function Banner() {
    return (
        <section style={robotoMono.style} className="mt-20 mx-auto max-w-2xl dark:text-white/90">
            <p className={`${robotoMono.className} animate-pulse hover:text-black/70 dark:hover:text-white` }>
                Every Weekend. Every Game.
            </p>
        </section>
    )
}