import Link from "next/link"
import { FaYoutube, FaTwitter, FaGithub, FaLaptop } from "react-icons/fa"
import { robotoMono } from "../fonts"

export default function Navbar() {
    return (
        <nav className="bg-slate-680 p-4 top-0 drop-shadow-xl z-10">
            <div className="prose prose-xl mx-auto flex justify-between flex-col sm:flex-row">
                <h1 className={`${robotoMono.className} ml-auto mr-auto underlinetext-3xl font-extrabold grid place-content-center mb-2 md:mb-0 text-2xl font-bold grid place-content-center mb-2 md:mb-0`} >
                    <Link href="/" className="text-white-700 text-white/90 no-underline hover:text-white">
                        Every Weekend. Every Game.
                    </Link>
                </h1>
            </div>
        </nav>
    )
}