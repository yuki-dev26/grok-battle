document.addEventListener("DOMContentLoaded", () => {
  const chatArea = document.getElementById("chatArea");
  const messageInput = document.getElementById("messageInput");
  const sendBtn = document.getElementById("sendBtn");
  const gaugeBar = document.getElementById("gaugeBar");
  const judgeComment = document.getElementById("judgeComment");

  let isProcessing = false;

  function appendMessage(role, text) {
    const div = document.createElement("div");
    div.className = `message ${role}`;
    div.innerHTML = `<div class="bubble">${text}</div>`;
    chatArea.appendChild(div);
    chatArea.scrollTop = chatArea.scrollHeight;
  }

  function updateGauge(score, comment) {
    // スコアは0-100。50が真ん中。
    // ユーザー有利(100)ならバーは100%（全部青）
    // 敵有利(0)ならバーは0%（全部赤＝背景色）
    gaugeBar.style.width = `${score}%`;

    // コメント更新（アニメーション付き）
    judgeComment.style.opacity = 0;
    setTimeout(() => {
      judgeComment.textContent = comment;
      judgeComment.style.opacity = 1;
    }, 300);

    // 色の変化（優勢劣勢で色味を変える演出などを入れても良いが今回はシンプルに）
  }

  async function sendMessage() {
    const text = messageInput.value.trim();
    if (!text || isProcessing) return;

    isProcessing = true;
    messageInput.disabled = true;
    sendBtn.disabled = true;

    // ユーザーのメッセージ表示
    appendMessage("user", text);
    messageInput.value = "";

    try {
      const response = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: text }),
      });

      const data = await response.json();

      if (data.error) {
        alert("エラーが発生しました");
        return;
      }

      // AIの返信表示
      appendMessage("opponent", data.response);

      // 判定更新
      updateGauge(data.judge.score, data.judge.comment);
    } catch (e) {
      console.error(e);
      alert("通信エラー");
    } finally {
      isProcessing = false;
      messageInput.disabled = false;
      sendBtn.disabled = false;
      messageInput.focus();
    }
  }

  sendBtn.addEventListener("click", sendMessage);
  messageInput.addEventListener("keypress", (e) => {
    if (e.key === "Enter") sendMessage();
  });

  // 初期フォーカス
  messageInput.focus();
});
