import { useState, useRef, useEffect } from "react";
import { Send } from "lucide-react";

import SpotlightBackground from "..//components/effects/SpotlightBackground";
import backgroundChat from "../../images/background_chat.png";
import avtUser from "../../images/avt_user.avif";

import { chatApi } from "../api/api";

export default function ChatUI() {
  const [messages, setMessages] = useState([
    { role: "bot", text: "Xin chào 👋 Bạn cần hỗ trợ gì?" },
  ]);
  const [input, setInput] = useState("");
  const endRef = useRef(null);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userText = input;

    // 1. Thêm tin nhắn user
    setMessages((prev) => [...prev, { role: "user", text: userText }]);
    setInput("");

    try {
      // 2. Gọi backend
      const data = await chatApi(userText);

      // 3. Thêm tin nhắn bot từ API
      setMessages((prev) => [
        ...prev,
        {
          role: "bot",
          text: data.answer,
        },
      ]);
    } catch (err) {
      // 4. Lỗi API
      setMessages((prev) => [
        ...prev,
        {
          role: "bot",
          text: "Hệ thống đang bận, vui lòng thử lại sau.",
        },
      ]);
    }
  };

  // Scroll xuống cuối mỗi lần có tin nhắn mới
  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  return (
    <SpotlightBackground background={backgroundChat}>
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
                className={`flex items-start gap-2 ${
                  msg.role === "user" ? "justify-end" : "justify-start"
                }`}
              >
                {msg.role === "bot" && (
                  <img
                    src="/images/avt_bot.jpg"
                    alt="AI"
                    className="w-8 h-8 rounded-full"
                  />
                )}

                <div
                  className={`max-w-[75%] break-words rounded-2xl px-4 py-2 text-sm ${
                    msg.role === "user"
                      ? "bg-gradient-to-r from-purple-700 to-blue-500 text-white text-justify"
                      : "bg-gray-200 text-gray-800 text-justify"
                  }`}
                >
                  {msg.text}
                </div>

                {msg.role === "user" && (
                  <img
                    src={avtUser}
                    alt="User"
                    className="w-8 h-8 rounded-full"
                  />
                )}
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
