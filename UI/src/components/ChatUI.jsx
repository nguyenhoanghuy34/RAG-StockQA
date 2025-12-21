import { useState, useRef, useEffect } from "react";
import { Send } from "lucide-react";

import SpotlightBackground from "..//components/effects/SpotlightBackground";
import backgroundChat from "../../images/background_chat.png";

export default function ChatUI() {
  const [messages, setMessages] = useState([
    { role: "bot", text: "Xin chào 👋 Bạn cần hỗ trợ gì?" },
  ]);
  const [input, setInput] = useState("");
  const endRef = useRef(null);

  const sendMessage = () => {
    if (!input.trim()) return;

    setMessages((prev) => [...prev, { role: "user", text: input }]);
    setInput("");

    setTimeout(() => {
      setMessages((prev) => [
        ...prev,
        { role: "bot", text: "Tôi đã nhận được tin nhắn." },
      ]);
    }, 600);
  };

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  return (
<SpotlightBackground background={backgroundChat}>
  {/* KHUNG CHAT KIỂU IPHONE 17 */}
  <div className="fixed inset-0 flex items-center justify-center pointer-events-none">
    <div className="pointer-events-auto w-[390px] h-[800px] flex flex-col rounded-3xl bg-white/90 backdrop-blur-md shadow-2xl">
      
{/* Header */}
<div className="rounded-t-3xl bg-gradient-to-r from-purple-700 to-sky-400 p-4 text-white flex flex-col">
  <h2 className="text-lg font-semibold">Chatbot Stock</h2>
  <p className="text-xs opacity-80 flex items-center gap-2">
    <span className="w-2 h-2 bg-green-400 rounded-full"></span>
    Online
  </p>
</div>

      {/* Messages */}
      <div className="flex-1 space-y-3 overflow-y-auto p-4">
        {messages.map((msg, idx) => (
          <div
            key={idx}
            className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}
          >
            <div
              className={`max-w-[75%] rounded-2xl px-4 py-2 text-sm ${
                msg.role === "user"
                  ? "bg-blue-600 text-white"
                  : "bg-gray-200 text-gray-800"
              }`}
            >
              {msg.text}
            </div>
          </div>
        ))}
        <div ref={endRef} />
      </div>

      {/* Input */}
      <div className="flex items-center gap-2 border-t p-3">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && sendMessage()}
          placeholder="Nhập tin nhắn..."
          className="flex-1 rounded-xl border px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <button
          onClick={sendMessage}
          className="rounded-xl bg-blue-600 p-2 text-white hover:bg-blue-700"
        >
          <Send size={18} />
        </button>
      </div>
    </div>
  </div>
</SpotlightBackground>
  );
}
