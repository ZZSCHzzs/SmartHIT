<template>
  <div class="launch-page">
    <div class="container mt-4">
      <div class="row justify-content-center">
        <div class="col-sm-8 shadow bg-white">
          <div class="card-body login-card">
            <div class="d-flex justify-content-between">
              <h2 class="mb-4 regis-title">发表主题帖</h2>
              <a class="text-decoration-none" @click="toggleCopilot">AI辅助撰写</a>
            </div>

            <form id="launch-form" enctype="multipart/form-data" novalidate @submit.prevent="submitForm">
              <div class="form-group mb-4">
                <label for="category">分类</label>
                <select id="category" v-model="form.category" class="form-control">
                  <option v-for="category in categories" :key="category.id" :value="category.id">
                    {{ category.name }}
                  </option>
                </select>
              </div>
              <div class="form-group mb-4">
                <label for="title">标题</label>
                <input id="title" v-model="form.title" class="form-control" type="text">
              </div>
              <div class="form-group mb-4">
                <label for="text">正文</label>
                <textarea id="text" v-model="form.text" class="form-control fixed-height-textarea"></textarea>
              </div>
              <div class="form-group mb-4">
                <label for="additionalInformation">附加信息</label>
                <input id="additionalInformation" v-model="form.additionalInformation" class="form-control" type="text">
              </div>
              <div class="form-group mb-2">
                <label for="additionalGraphics">附加图片</label>
                <input id="additionalGraphics" accept="image/*" class="form-control" type="file"
                       @change="handleFileUpload">
              </div>
              <button class="btn btn-primary" type="submit">发表</button>
            </form>
          </div>
        </div>
        <div v-if="showCopilot" class="col-sm-4">
          <div class="card shadow">
            <div class="card-body">
              <h5>AI 辅助撰写</h5>
              <div class="form-group mb-3">
                <label for="topic">输入主题</label>
                <input id="topic" v-model="topic" class="form-control" type="text">
                <button class="btn btn-secondary mt-2" @click="generateAIPost" :disabled="isLoading">
                  获取建议
                </button>
              </div>
              <!-- 显示加载提示 -->
              <div v-if="isLoading" class="alert alert-info">
                正在生成AI建议，请耐心等待...
              </div>
              <div v-if="aiTitle && aiContent">
                <h6>建议标题</h6>
                <p>{{ aiTitle }}</p>
                <h6>建议内容</h6>
                <p v-html="formatMessage(aiContent)"></p>
                <button class="btn btn-primary mt-2" @click="applyAIPost">应用建议</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from '@/axios.js';

export default {
  name: 'PostLaunch',
  data() {
    return {
      form: {
        category: '',
        title: '',
        text: '',
        additionalInformation: '',
        additionalGraphics: null,
      },
      categories: [],
      showCopilot: false,
      topic: '',           // 用户输入的主题
      aiTitle: '',         // AI 返回的标题
      aiContent: '',       // AI 返回的内容
      isLoading: false,    // AI生成时的加载状态
    };
  },
  methods: {
    handleFileUpload(event) {
      this.form.additionalGraphics = event.target.files[0];
    },
    submitForm() {
      const formData = new FormData();
      formData.append('category', this.form.category);
      formData.append('title', this.form.title);
      formData.append('text', this.form.text);
      formData.append('additionalInformation', this.form.additionalInformation);
      if (this.form.additionalGraphics) {
        formData.append('additionalGraphics', this.form.additionalGraphics);
      }
      axios.post('posts/launch/', formData)
          .then(response => {
            // Handle success
            console.log('Form submitted successfully:', response);
            this.$router.push('/p/' + response.data.post_id);
          })
          .catch(error => {
            // Handle error
            console.error('Error submitting form:', error);
          });
    },
    fetchCategories() {
      const params = this.$route.query; // Assuming you're using Vue Router
      axios.get('categories/', {params})
          .then(response => {
            this.categories = response.data;
          })
          .catch(error => {
            console.error('Error fetching categories:', error);
          });
    },
    toggleCopilot() {
      this.showCopilot = !this.showCopilot;
    },
    generateAIPost() {
      if (!this.topic.trim()) return;

      this.isLoading = true; // 开始加载
      axios.post('assistants/write/', { topic: this.topic }, {timeout: 60000})
          .then(response => {
            this.aiTitle = response.data.title;
            this.aiContent = response.data.content;
            this.isLoading = false; // 结束加载
          })
          .catch(error => {
            console.error('Error fetching AI suggestions:', error);
            this.isLoading = false; // 结束加载，即使有错误
          });
    },
    applyAIPost() {
      this.form.title = this.aiTitle;
      this.form.text = this.aiContent;
      this.toggleCopilot(); // Hide copilot area after applying suggestions
    },
    formatMessage(text) {
      return text.replace(/\n/g, "<br>");
    },
  },
  mounted() {
    this.fetchCategories();
  },
};
</script>

<style scoped>
/* Your styles here */
</style>
