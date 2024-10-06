import Chat from "./Chat";

const ChatPage = ({ params }) => {
  return (
    <div>
      <h1>Chat with {params.userId}</h1>
      <Chat userId={params.userId} />
    </div>
  );
};

export default ChatPage;
