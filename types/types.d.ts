import Tag from "tags.ts"
import Category from "categories.ts"

type Post = {
    id: string,
    title: string,
    date: string,
    chapter: string,
    tags: Tag[],
    category: Category,
}