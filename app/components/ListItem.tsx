import Link from "next/link"
import getFormattedDate from "@/lib/getFormattedDate"
import { robotoMono } from "../fonts"
import { Post } from "../../types/types"
import { Tag } from "../../types/tags"
import {
    Card,
    CardDescription,
    CardHeader,
    CardTitle,
    CardFooter
  } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"


type Props = {
    post: Post
}

export default function ListItem({ post }: Props) {
    const { id, title, date, tags, category } = post
    const formattedDate = getFormattedDate(date)
    return (
        <li style={robotoMono.style} className="mt-4 dark:text-white/90">
            
            <div className="flex mb-1">
                <p className="mt-1 flex-none text-sm mr-2 animate-pulse">{formattedDate}</p>
                <Badge className="flex-none ml-auto" variant="secondary">{category}</Badge>
            </div>
            <Link href={`/posts/${id}`}>
                <Card className="hover:text-black/70 dark:hover:text-white">
                    <CardHeader>
                        <div className="flex">
                            <CardTitle className="text-2xl">{title} </CardTitle>
                            <Avatar className="flex-none ml-auto">
                                <AvatarImage src="https://i.ibb.co/3c4Tn7Y/CG.jpg" />
                                <AvatarFallback>CG</AvatarFallback>
                            </Avatar>
                        </div>
                    </CardHeader>
                </Card>
            </Link>
            <div className="flex mb-1">
                {tags.map((tag: Tag, index: number) => (
                    <Badge key={index} className="flex-none" variant="outline">
                        {tag}
                    </Badge>
                ))}  
            </div>
        </li>
    )
}