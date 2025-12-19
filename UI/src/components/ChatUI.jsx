import { useState, useRef, useEffect } from "react";
import { Send } from "lucide-react";

export default function ChatUI() {
  const [messages, setMessages] = useState([
    { role: "bot", text: "Xin chào 👋 Bạn cần hỗ trợ gì?" },
  ]);
  const [input, setInput] = useState("");
  const endRef = useRef(null);

  const sendMessage = () => {
    if (!input.trim()) return;

    setMessages([...messages, { role: "user", text: input }]);
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
    <div className="flex h-screen items-center justify-center bg-gray-100 p-4">
      <div className="flex h-full w-full max-w-md flex-col rounded-2xl bg-white shadow-xl">
        
        {/* Header */}
        <div className="rounded-t-2xl bg-blue-600 p-4 text-white">
          <h2 className="text-lg font-semibold">AI Chatbot</h2>
          <p className="text-xs opacity-80">Online</p>
        </div>

        {/* Messages */}
        <div className="flex-1 space-y-3 overflow-y-auto p-4">
          {messages.map((msg, idx) => (
            <div
              key={idx}
              className={`flex ${
                msg.role === "user" ? "justify-end" : "justify-start"
              }`}
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
  );
}
