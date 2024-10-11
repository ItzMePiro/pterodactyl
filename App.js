import React, { useState, useEffect, useRef } from "react";
import axios from "axios";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { dracula } from "react-syntax-highlighter/dist/esm/styles/prism";

function App() {
  const [messages, setMessages] = useState([
    { role: "system", content: "You are an Assistant." },
  ]);
  const [userInput, setUserInput] = useState("");
  const [loading, setLoading] = useState(false);
  const chatRef = useRef(null);

  // Handle API Request
  const handleSendMessage = async () => {
    const newMessages = [...messages, { role: "user", content: userInput }];
    setMessages(newMessages);
    setUserInput("");
    setLoading(true);

    try {
      const response = await axios.post("http://127.0.0.1:11434/api/chat", {
        model: "phi3.5",
        messages: newMessages,
        stream: true,
      });

      const assistantReply = response.data; // Capture response
      setMessages([...newMessages, { role: "assistant", content: assistantReply }]);
    } catch (error) {
      console.error("Error fetching response:", error);
    } finally {
      setLoading(false);
    }
  };

  // Auto-scroll to the latest message
  useEffect(() => {
    chatRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  // Handle rendering code blocks
  const renderMessage = (message) => {
    if (message.role === "assistant" && message.content.includes("```")) {
      const codeBlock = message.content.match(/```(.*?)```/s);
      if (codeBlock) {
        return (
          <SyntaxHighlighter language="javascript" style={dracula}>
            {codeBlock[1]}
          </SyntaxHighlighter>
        );
      }
    }
    return <span>{message.content}</span>;
  };

  return (
    <div className="app">
      <div className="chat-window">
        {messages.map((message, index) => (
          <div key={index} className={`message ${message.role}`}>
            <strong>{message.role === "user" ? "You" : "Assistant"}: </strong>
            {renderMessage(message)}
          </div>
        ))}
        <div ref={chatRef} />
      </div>

      <div className="input-area">
        <input
          type="text"
          value={userInput}
          onChange={(e) => setUserInput(e.target.value)}
          placeholder="Type a message..."
        />
        <button onClick={handleSendMessage} disabled={loading}>
          {loading ? "Loading..." : "Send"}
        </button>
      </div>
    </div>
  );
}

export default App;
