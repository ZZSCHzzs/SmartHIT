<template>
  <div class="container">
    <div class="card mt-5">
      <div class="card-header bg-theme-light text-white justify-content-center">
        <h3 class="justify-content-center">{{ notification.title }}</h3>
      </div>
      <div class="card-body">
        <div class="d-flex justify-content-between align-items-center">
          <h6 class="card-title text-muted">发布者: {{ notification.launcher }}</h6>
          <p class="card-text text-muted">浏览次数: {{ notification.view_times }}</p>
        </div>
        <div class="mb-3"></div>
        <p class="card-text" v-html="formatMessage(notification.text)"></p>
        <div v-if="notification.additional_graphics">
          <img :src="notification.additional_graphics" alt="附加图片" class="img-fluid">
        </div>
      </div>
      <div class="card-footer text-muted">
        发布时间：{{ $formatDateTime(notification.launch_time) }}
      </div>
    </div>
  </div>
</template>

<script>
import axios from "@/axios";

export default {
  name: 'NotificationDetail',
  data() {
    return {
      notification: {}
    }
  },
  methods: {
    fetchNotification() {
      const nid = this.$route.params.nid; // 从路由参数获取通知ID
      axios.get(`/notifications/${nid}/view/`)
          .then(res => {
            this.notification = res.data;
          })
          .catch(error => {
            console.error('There was an error fetching the notification!', error);
          });
    }
    ,    formatMessage(text) {
      return text.replace(/\n/g, "<br>");
    },
  },
  created() {
    this.fetchNotification(); // 在组件创建时获取通知数据
  }
};
</script>

<style scoped>
/* 根据需要添加样式 */
</style>
