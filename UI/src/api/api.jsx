export async function chatApi(message) {
  const res = await fetch("http://127.0.0.1:8000/chat/response", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ message }),
  });

  if (!res.ok) {
    throw new Error("API error");
  }

  return await res.json();
}
