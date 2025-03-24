<template>
  <div>
    <!-- 悬浮气泡 -->
    <div
        class="floating-bubble rounded-circle bg-primary text-white d-flex justify-content-center align-items-center shadow"
        :style="{ top: `${position.top}px`, left: `${position.left}px`, position: 'fixed' }"
        @mousedown="startDrag"
        @mouseup="stopDrag"
        @click="toggleChatBox"
    >
      <div class="bubble">💬</div>
    </div>

    <!-- 对话框 -->
    <div
        v-if="showChatBox"
        class="chat-box border shadow bg-white"
        :style="{ top: `${chatBoxPosition.top}px`, left: `${chatBoxPosition.left}px`, position: 'fixed' }"
    >
      <div
          class="chat-header p-2 border-bottom bg-light"
          @mousedown="startChatBoxDrag"
          @mouseup="stopChatBoxDrag"
          @mousemove="onChatBoxDrag"
      >
        <div>
          <span>AI 对话</span>
          <select class="form-select form-select-sm d-inline-block w-auto ms-2" v-model="mode" @change="onModeChange">
            <option value="study">学习助手</option>
            <option value="life">生活助手</option>
          </select>
        </div>
        <button @click="toggleChatBox" class="btn btn-sm btn-danger">✕</button>
      </div>

      <div class="chat-content p-3">
        <div v-for="(msg, index) in messages" :key="index" class="message">
          <span class="message-role fw-bold">{{ msg.role }}:</span>
          <span v-html="formatMessage(msg.text)"></span>
          <hr v-if="index < messages.length - 1" />
        </div>
        <div v-if="isWaiting" class="waiting text-center text-muted">请耐心等待...</div>
      </div>

      <div class="input-group p-2">
        <input
            type="text"
            class="form-control"
            v-model="userMessage"
            @keyup.enter="sendMessage"
            placeholder="请输入内容"
        />
        <button @click="sendMessage" class="btn btn-primary">发送</button>
      </div>
    </div>
  </div>
</template>


<script>
import axios from '@/axios';

export default {
  data() {
    return {
      showChatBox: false,
      messages: [],
      userMessage: "",
      mode: "study",
      position: { top: window.innerHeight - 100, left: window.innerWidth - 100 },
      chatBoxPosition: { top: 0, left: 0 },
      isDragging: false,
      isChatBoxDragging: false,
      dragOffset: { x: 0, y: 0 },
      chatBoxDragOffset: { x: 0, y: 0 },
      isWaiting: false,  // AI响应等待状态
    };
  },
  methods: {
    scrollToBottom() {
      this.$nextTick(() => {
        const chatContent = this.$el.querySelector(".chat-content");
        chatContent.scrollTop = chatContent.scrollHeight;
      });
    },

    toggleChatBox() {
      if (!this.isDragging && !this.isChatBoxDragging) {
        this.showChatBox = !this.showChatBox;
        if (this.showChatBox) {
          this.adjustChatBoxPosition();
          this.scrollToBottom();
        }
      }
    },
    adjustChatBoxPosition() {
      const chatBoxWidth = 400;
      const chatBoxHeight = 600;
      let top = this.position.top - chatBoxHeight;
      let left = this.position.left;

      if (top < 0) {
        top = this.position.top + 50;
      }
      if (left + chatBoxWidth > window.innerWidth) {
        left = window.innerWidth - chatBoxWidth;
      }
      if (left < 0) {
        left = 0;
      }

      this.chatBoxPosition = {top, left};
    },
    sendMessage() {
      if (!this.userMessage.trim()) return;

      const userMsg = {role: '用户', text: this.userMessage};
      this.messages.push(userMsg);
      this.userMessage = "";
      this.isWaiting = true;  // 设置等待状态

      axios
          .post(this.mode === "study" ? "/assistants/study/" : "/assistants/live/", {
            message: userMsg.text,
          },{timeout: 60000})
          .then((response) => {
            this.messages.push({role: "AI", text: response.data.answer});
            this.scrollToBottom();
          })
          .catch(() => {
            this.messages.push({role: "系统", text: "AI响应失败，请重试。"});
            this.scrollToBottom();
          })
          .finally(() => {
            this.isWaiting = false;  // 请求完成后取消等待状态
          });
    },

    // 悬浮气泡的拖拽功能
    startDrag(event) {
      this.isDragging = true;
      this.dragOffset.x = event.clientX - this.position.left;
      this.dragOffset.y = event.clientY - this.position.top;

      document.addEventListener("mousemove", this.onDrag);
      document.addEventListener("mouseup", this.stopDrag);
    },
    onDrag(event) {
      if (this.isDragging) {
        this.position.left = event.clientX - this.dragOffset.x;
        this.position.top = event.clientY - this.dragOffset.y;
      }
    },
    stopDrag() {
      this.isDragging = false;
      document.removeEventListener("mousemove", this.onDrag);
      document.removeEventListener("mouseup", this.stopDrag);
    },

    // 对话框拖拽功能
    startChatBoxDrag(event) {
      this.isChatBoxDragging = true;
      this.chatBoxDragOffset.x = event.clientX - this.chatBoxPosition.left;
      this.chatBoxDragOffset.y = event.clientY - this.chatBoxPosition.top;

      document.addEventListener("mousemove", this.onChatBoxDrag);
      document.addEventListener("mouseup", this.stopChatBoxDrag);
    },
    onChatBoxDrag(event) {
      if (this.isChatBoxDragging) {
        this.chatBoxPosition.left = event.clientX - this.chatBoxDragOffset.x;
        this.chatBoxPosition.top = event.clientY - this.chatBoxDragOffset.y;
      }
    },
    stopChatBoxDrag() {
      this.isChatBoxDragging = false;
      document.removeEventListener("mousemove", this.onChatBoxDrag);
      document.removeEventListener("mouseup", this.stopChatBoxDrag);
    },

    onModeChange() {
      this.messages.push({role: "系统", text: `已切换到${this.mode === "study" ? "学习" : "生活"}助手模式`});
    },

    // 格式化消息文本，保留换行符
    formatMessage(text) {
      return text.replace(/\n/g, "<br>");
    },
  },
  mounted() {
    window.addEventListener("resize", () => {
      if (this.position.top > window.innerHeight - 100) {
        this.position.top = window.innerHeight - 100;
      }
      if (this.position.left > window.innerWidth - 100) {
        this.position.left = window.innerWidth - 100;
      }
    });
  },
};
</script>

<style scoped>
.floating-bubble {
  position: fixed;
  cursor: pointer;
  z-index: 1000;
}

.bubble {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background-color: #007bff;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 24px;
  color: white;
}

.chat-box {
  position: fixed;
  width: 400px;
  height: 600px;
  background-color: white;
  border: 1px solid #ddd;
  padding: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  z-index: 1000;
}

.chat-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
  cursor: move;
  user-select: none;
}

.chat-content {
  height: 470px;
  overflow-y: auto;
}

.message {
  margin: 5px 0;
}

.waiting {
  font-style: italic;
  color: #999;
  text-align: center;
  margin: 10px 0;
}

hr {
  border: none;
  border-top: 1px solid #ddd;
  margin: 10px 0;
}
</style>
