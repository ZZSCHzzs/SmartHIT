<template>

  <div class="container col">
    <div class="row no-gutters mt-4">
      <div class="d-flex justify-content-between align-items-center mb-2 col-sm-12">
        <h2 class="mb-0">通知中心</h2>
        <router-link class="btn btn-primary" to="/notice/launch">发布通知</router-link>
      </div>
    </div>

    <div class="row g-0">
      <div v-for="type in types" :key="type.id" class="col-sm-6">
        <div class="card m-3 min-height">
          <div class="card-header bg-theme-light text-white h4">{{ type.name }}</div>
          <div class="card-body d-flex flex-column">
            <div v-for="notification in type.notifications"
                 v-if="type.notifications && type.notifications.length > 0"
                 :key="notification.id"
                 class="notification-item py-2 border-bottom border-primary d-flex justify-content-between align-items-center"
                 @mouseleave="hideTooltip(notification.id)" @mouseover="showTooltip(notification.id)">
              <div>
                <router-link :to="'/n/' + notification.id" class="card-title h5 mb-0 text-decoration-none">
                  {{ $truncate(notification.title, 20) }}
                </router-link>
              </div>
              <div class="text-muted">
                <small>{{ $formatDate(notification.launch_time) }}</small>
              </div>
              <div v-if="tooltipVisible[notification.id]" class="tooltip-box">
                <div v-if="notificationsMap[notification.id].loading">
                  <p>正在AI概括中...</p>
                </div>
                <div v-else>
                  <h6>{{ notificationsMap[notification.id].title }}</h6>
                  <p><strong>发布者:</strong> {{ notification.launcher }}</p>
                  <p><strong>AI概括:</strong> {{ notificationsMap[notification.id].abstract }}</p>
                  <p><strong>关键词:</strong> {{ notificationsMap[notification.id].keywords.join(' ') }}</p>
                </div>
              </div>
            </div>
            <p v-else class="card-text">暂无通知</p>
          </div>
        </div>
      </div>

      <div class="col-sm-6">
        <div class="card m-3 min-height">
          <div class="card-header bg-theme-light text-white h4">
            <div class="d-flex justify-content-between align-items-center">
              <a>最新通知</a>
              <a class="text-white" href="/notice/list">更多</a>
            </div>
          </div>
          <div class="card-body d-flex flex-column">
            <div v-if="latestNotifications && latestNotifications.length > 0">
              <div v-for="notification in latestNotifications"
                   :key="notification.id"
                   class="notification-item py-2 border-bottom border-primary d-flex justify-content-between align-items-center"
                   @mouseleave="hideLatestTooltip(notification.id)" @mouseover="showLatestTooltip(notification.id)">
                <div>
                  <router-link :to="'/n/' + notification.id" class="card-title h5 mb-0 text-decoration-none">
                    {{ $truncate(notification.title, 20) }}
                  </router-link>
                </div>
                <div class="text-muted">
                  <small>{{ $formatDate(notification.launch_time) }}</small>
                </div>
                <div v-if="latestTooltipVisible[notification.id]" class="tooltip-box">
                  <div v-if="notificationsMap[notification.id].loading">
                    <p>正在AI概括中...</p>
                  </div>
                  <div v-else>
                    <h6>{{ notificationsMap[notification.id].title }}</h6>
                    <p><strong>发布者:</strong> {{ notification.launcher }}</p>
                    <p><strong>AI概括:</strong> {{ notificationsMap[notification.id].abstract }}</p>
                    <p><strong>关键词:</strong> {{ notificationsMap[notification.id].keywords.join(' ') }}</p>
                  </div>
                </div>
              </div>
            </div>
            <p v-else class="card-text">暂无最新通知</p>
          </div>
        </div>
      </div>
    </div>

    <div class="row no-gutters">
      <div class="col-sm-12">
        <div class="card m-3">
          <div class="card-header bg-theme text-white h4">
            本科生院
          </div>
          <div class="card-body todayHIT" v-html="todayHITContent" style="font-size: 20px"></div>
        </div>
      </div>
      <div class="col-sm-12">
        <div class="card m-3">
          <div class="card-header bg-theme text-white h4">
            电信学院
          </div>
          <div class="card-body todayHIT" v-html="todayHITContent2" style="font-size: 20px"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "@/axios";

export default {
  name: 'NoticeCenter',

  data() {
    return {
      isAllowed: false,
      isAuthed: false,
      types: [],
      latestNotifications: [],
      todayHITContent: '',
      tooltipVisible: {}, // { [notificationId]: boolean }
      latestTooltipVisible: {}, // { [notificationId]: boolean }
      notificationsMap: {} // { [notificationId]: { loading: boolean, abstract: string, keywords: string[] } }
    };
  },
  methods: {
    fetchNoticeCenter() {
      axios.get('/notifications/notice_center/')
          .then(response => {
            this.latestNotifications = response.data.latest_notifications;
            this.types = response.data.types;
            this.isAuthed = response.data.is_authed;
            this.todayHITContent = response.data.content;
            this.todayHITContent2 = response.data.content2;
            this.isAllowed = response.data.is_allowed;
                this.types.forEach(type => {
                  type.notifications.forEach(notification => {
                    // 初始化 notificationsMap
                    this.notificationsMap[notification.id] = {
                      ...notification,
                      loading: !notification.abstract || !notification.keywords || notification.keywords.length === 0,
                      keywords: notification.keywords || [],
                      abstract: notification.abstract || '',
                    };

                  });
          });
          })
          .catch(error => {
            console.error('Error fetching notice center data:', error);
          });

    },

    showTooltip(notificationId) {
      this.tooltipVisible[notificationId] = true;
      if (!this.notificationsMap[notificationId].abstract) {
        this.loadAbstractAndKeywords(notificationId);
      }
    },
    hideTooltip(notificationId) {
      this.tooltipVisible[notificationId] = false;
    },
    showLatestTooltip(notificationId) {
      this.latestTooltipVisible[notificationId] = true;
      if (!this.notificationsMap[notificationId].abstract) {
        this.loadAbstractAndKeywords(notificationId);
      }
    },
    hideLatestTooltip(notificationId) {
      this.latestTooltipVisible[notificationId] = false;
    },
    loadAbstractAndKeywords(notificationId) {
      const notification = this.notificationsMap[notificationId];
      if (notification) {
        notification.loading = true;
        axios.get(`/notifications/${notificationId}/abstract/`,{ timeout: 60000 })
            .then(response => {
              const { abstract, keywords } = response.data;
              this.notificationsMap[notificationId].abstract = abstract;
              this.notificationsMap[notificationId].keywords = keywords;
            })
            .catch(error => {
              console.error(`Error fetching abstract and keywords for notification ${notificationId}:`, error);
              this.$set(notification, 'loading', false);
            });
      }
      this.notificationsMap[notificationId].loading = false;
    }
  },
  mounted() {
    this.fetchNoticeCenter();
  },
};
</script>
<style scoped>
.notification-item {
  position: relative;
}

.tooltip-box {
  position: absolute;
  background: #fff;
  border: 1px solid #ccc;
  padding: 10px;
  box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
  z-index: 1000;
  top: 100%;
  left: 0;
  transform: translateY(10px);
  display: none;
}

.notification-item:hover .tooltip-box,
.tooltip-box {
  display: block;
}

.tooltip-box p {
  margin: 0;
}
.todayHIT ul{
  list-style-type: none;
}
.todayHIT span{
  margin-right: 5px !important;
}
.todayHIT a{
  font-size: 20px !important;
  text-decoration: none !important;
}
</style>
