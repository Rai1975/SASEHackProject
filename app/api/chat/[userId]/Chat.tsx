import { useEffect, useState } from "react";
import { io, Socket } from "socket.io-client";

  const myFunction = ({ userId }: User) => {
    console.log(userId);
  };
  


let socket: Socket;

const Chat = ({ userId }) => {
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState("");

  useEffect(() => {
    // Initialize socket connection
    socket = io();

    socket.on("receiveMessage", (message) => {
      setMessages((prevMessages) => [...prevMessages, message]);
    });

    return () => {
      socket.off("receiveMessage");
      socket.disconnect();
    };
  }, []);

  const handleSend = async (e) => {
    e.preventDefault();
    const messageData = { userId, text: newMessage };

    socket.emit("sendMessage", messageData);

    await fetch('/api/messages', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(messageData),
    });

    setNewMessage("");
  };

  return (
    <div>
      <div className="chat-messages">
        {messages.map((msg, index) => (
          <p key={index}>{msg.text}</p>
        ))}
      </div>
      <form onSubmit={handleSend}>
        <input
          type="text"
          value={newMessage}
          onChange={(e) => setNewMessage(e.target.value)}
          placeholder="Type a message"
        />
        <button type="submit">Send</button>
      </form>
    </div>
  );
};

export default Chat;
