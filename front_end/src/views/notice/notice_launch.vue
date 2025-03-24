<template>
  <div class="launch-page">
    <div class="container mt-4">
      <div class="row justify-content-center">
        <div class="col-sm-8  shadow bg-white">
          <div class="card-body login-card">
            <h2 class="mb-4 regis-title">发布新通知</h2>
            <form @submit.prevent="submitForm" id="launch-form" enctype="multipart/form-data" novalidate>
              <div class="row g-5 mb-4">
                <div class="form-group left col-sm-6">
                  <label class="form-label" for="launcher">发布人</label>
                  <input type="text" id="launcher" v-model="form.launcher" class="form-control">
                </div>
                <div class="form-group right col-sm-6">
                  <label class="form-label" for="type">类型</label>
                  <select id="type" v-model="form.type" class="form-control">
                    <option v-for="type in types" :key="type.id" :value="type.id">{{ type.name }}</option>
                  </select>
                </div>
              </div>
              <div class="form-group col-sm-12 mb-4">
                <label class="form-label" for="title">标题</label>
                <input type="text" id="title" v-model="form.title" class="form-control">
              </div>
              <div class="form-group col-sm-12 mb-4">
                <label class="form-label" for="text">内容</label>
                <textarea id="text" v-model="form.text" class="form-control fixed-height-textarea"></textarea>
              </div>
              <div class="form-group col-sm-12 mb-4">
                <label class="form-label" for="additional_graphics">附加图片</label>
                <br>
                <input class="form-control" accept="image/*" type="file" id="additional_graphics" @change="handleFileUpload">
              </div>
              <div class="col-sm-12 mb-4">
                <button type="submit" class="btn btn-primary">发布</button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>

    <!-- 模态框 -->
    <div v-if="showModal" class="modal" id="launch-success-modal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">发布成功</h5>
            <button type="button" class="close" @click="hideModal" aria-label="Close">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body">
            <p>发布成功!是否继续发布通知</p>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-primary" @click="continuePublishing">继续</button>
            <button type="button" class="btn btn-secondary">
              <router-link class="text-decoration-none text-white" to="/notice">回到通知中心</router-link>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "@/axios";

export default {
  name: 'LaunchNotice',
  data() {
    return {
      form: {
        launcher: '',
        type: '',
        title: '',
        text: '',
        additional_graphics: null,
      },
      types: [],
      showModal: false,
    };
  },
  methods: {
    handleFileUpload(event) {
      this.form.additional_graphics = event.target.files[0];
    },
    submitForm() {
      const formData = new FormData();
      formData.append('launcher', this.form.launcher);
      formData.append('type', this.form.type);
      formData.append('title', this.form.title);
      formData.append('text', this.form.text);
      if (this.form.additional_graphics) {
        formData.append('additional_graphics', this.form.additional_graphics);
      }

      axios.post('/notifications/launch/', formData, {
        headers: {
          'X-CSRFToken': this.getCsrfToken(),
          'Content-Type': 'multipart/form-data',
        },
      })
          .then(response => {
            if (response.data.success) {
              this.form = {
                launcher: '',
                type: '',
                title: '',
                text: '',
                additional_graphics: null,
              };
              this.showModal = true;
            } else {
              // 处理错误
              console.error(response.data.errors);
            }
          })
          .catch(error => {
            console.error('Error:', error);
          });
    },
    getCsrfToken() {
      let cookieValue = null;
      if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; cookies.length; i++) {
          const cookie = cookies[i].trim();
          if (cookie.substring(0, 10) === 'csrftoken=') {
            cookieValue = decodeURIComponent(cookie.substring(10));
            break;
          }
        }
      }
      return cookieValue;
    },
    hideModal() {
      this.showModal = false;
    },
    continuePublishing() {
      this.hideModal();
      this.$router.push('/notice/launch');
    },
    fetchTypes() {
      axios.get('/notifications/types/')
          .then(response => {
            this.types = response.data;
          })
          .catch(error => {
            console.error('There was an error fetching the notification types!', error);
          });
    },
  },
  mounted() {
    this.fetchTypes();
  },
};
</script>

<style scoped>
/* Add your custom styles here */
</style>
