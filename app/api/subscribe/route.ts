import { NextRequest, NextResponse } from 'next/server'
import mailchimp from '@mailchimp/mailchimp_marketing';
 

mailchimp.setConfig({
  apiKey: process.env.MAILCHIMP_API_KEY,
  server: process.env.MAILCHIMP_API_SERVER, // e.g. us1
});
 
export async function POST(Request: NextRequest) {
  console.log("in here")

  const json = await Request.json();
  console.log(json.email);
 
  if (!json.email) {
    return NextResponse.json({ error: 'Email is required' });
  }
 
  try {
    await mailchimp.lists.addListMember(process.env.MAILCHIMP_AUDIENCE_ID!, {
      email_address: json.email,
      status: 'subscribed',
    });
    console.log("should be good")
    return NextResponse.json({ error: '' });
  } catch (error: any) {
    console.log(error)
    return NextResponse.json({ error: error.message || error.toString() });
  }
};