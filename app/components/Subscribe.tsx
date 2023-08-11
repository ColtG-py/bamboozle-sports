"use client";

import { zodResolver } from "@hookform/resolvers/zod"
import { useForm } from "react-hook-form"
import * as z from "zod"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import {
    Form,
    FormControl,
    FormField,
    FormItem,
    FormMessage,
  } from "@/components/ui/form"
import { toast } from "@/components/ui/use-toast"

interface SubscribeResponse {
  error: string;
}

const FormSchema = z.object({
    email: z.string().min(5, {
      message: "Email must be at least 5 characters.",
    }),
})

export default function Subscribe() {

    const subscribe = async (email: string) => {
        const res = await fetch('/api/subscribe', {
        body: JSON.stringify({
            email: email,
        }),
        headers: {
            'Content-Type': 'application/json',
        },
        method: 'POST',
        });

        const { error } = await res.json() as SubscribeResponse;
    };

    const form = useForm<z.infer<typeof FormSchema>>({
      resolver: zodResolver(FormSchema),
    })
   
    function onSubmit(data: z.infer<typeof FormSchema>) {
        toast({
            title: "Thanks, you've subscribed 🎉",
            description: "You'll be sent an email the next time an article is posted. Thanks for your support!"
        })
        subscribe(data['email'])
    }
   
    return (
      <Form {...form}>
        <div className="text-white">
            <form onSubmit={form.handleSubmit(onSubmit)} className="flex w-full max-w-sm items-center space-x-2 text-white">
            <FormField
                control={form.control}
                name="email"
                render={({ field }) => (
                <FormItem>
                    <FormControl className="text-black">
                    <Input placeholder="Email" {...field} />
                    </FormControl>
                    <FormMessage />
                </FormItem>
                )}
            />
            <Button type="submit">Subscribe.</Button>
            </form>
        </div>
      </Form>
    )
  }
