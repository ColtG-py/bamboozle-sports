import Link from "next/link"
import { robotoMono } from "../fonts"
import Subscribe from "./Subscribe"
import { FaCoffee } from "react-icons/fa"

export default function Footer() {
    return (
        <footer className="mt-2">
            <nav className="bg-slate-800">
                <div className="prose prose-xl mx-auto flex-row">
                    
                    <p>This is all AI generated.</p>  
                </div>              
            </nav>
        </footer>
    )
}