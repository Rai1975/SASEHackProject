import clientPromise from '../../../lib/mongodb';

export async function GET(req) {
  const client = await clientPromise;
  const db = client.db();
  const messages = await db.collection('messages').find().toArray();
  return new Response(JSON.stringify(messages), { status: 200 });
}

export async function POST(req) {
  const client = await clientPromise;
  const db = client.db();
  const { message } = await req.json();

  await db.collection('messages').insertOne({ message, createdAt: new Date() });

  return new Response(JSON.stringify({ message: 'Message saved' }), { status: 201 });
}
