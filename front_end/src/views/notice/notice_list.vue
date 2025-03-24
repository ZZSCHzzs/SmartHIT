<template>
  <div class="container mt-4">
    <h2 class="mb-4">通知列表</h2>
    <div v-if="notifications.length > 0">
      <div v-for="notification in notifications" :key="notification.id">
        <div class="row mb-4">
          <div class="col-md-12">
            <div class="card shadow">
              <div style="display: flex">
                <div class="card-header text-center" style="display: flex; align-items: center; justify-content: center;">
                  {{ notification.type.name }}
                </div>
                <div class="card-body pl-3 pr-3 pb-4 pt-4">
                  <h5 class="card-title mb-0">
                    <router-link :to="{ path: `/n/${notification.id}` }">{{ notification.title }}</router-link>
                  </h5>
                  <div class="d-flex justify-content-between align-items-center" style="height: 100%;">
                    <div>
                      <p class="card-text mb-0 text-muted">发布者: {{ notification.launcher }}</p>
                    </div>
                    <div>
                      <p class="card-text mb-0 text-muted">发布时间: {{ $formatDateTime(notification.launch_time) }}</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <!-- 分页组件 -->
    <ul class="pagination justify-content-center">
      <Pagination current-page="1" total-pages="10"></Pagination>
    </ul>
  </div>
</template>

<script>
import Pagination from "@/components/pagination.vue";
import axios from "@/axios";

export default {
  name: 'notice_list',
  components: { Pagination },
  data() {
    return {
      notifications: [],
      types: {},
    };
  },
  methods: {
    fetchNotifications() {
      axios.get('/notifications/')
          .then(res => {
            this.notifications = res.data;
          })
          .catch(error => {
            console.error('There was an error fetching the notification!', error);
          });
    },
    fetchNotificationTypes() {
      axios.get('/notifications/types/')
          .then(res => {
            const typesArray = res.data;
            const typesObject = {};
            typesArray.forEach(type => {
              typesObject[type.id] = type;
            });
            this.types = typesObject;
          })
          .catch(error => {
            console.error('There was an error fetching the notification types!', error);
          });
    }
  },
  mounted() {
    this.fetchNotifications();
    this.fetchNotificationTypes();
  }
};
</script>

<style scoped>
</style>
