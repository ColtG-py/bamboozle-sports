import Image from "next/image"

export default function MyProfilePic() {
    return (
        <section className="w-full mx-auto mb-20">
            <Image
                className="border-4 border-black dark:border-slate-500 drop-shadow-xl shadow-black mx-auto mt-8"
                src="/images/fooseball.jpg"
                width={600}
                height={600}
                alt="Fooseball"
                priority={true}
            />
        </section>
    )
}