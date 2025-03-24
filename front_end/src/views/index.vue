<template>
  <div>
    <div class="index_root">
      <div class="container bg-white pt-4">
        <div id="carouselExampleCaptions" class="carousel slide">
          <div class="carousel-indicators">
            <button type="button" data-bs-target="#carouselExampleCaptions" data-bs-slide-to="0" class="active"
              aria-current="true" aria-label="Slide 1"></button>
            <button type="button" data-bs-target="#carouselExampleCaptions" data-bs-slide-to="1"
              aria-label="Slide 2"></button>
            <button type="button" data-bs-target="#carouselExampleCaptions" data-bs-slide-to="2"
              aria-label="Slide 3"></button>
          </div>
          <div class="carousel-inner">
            <div class="carousel-item active">
              <img class="bd-placeholder-img bd-placeholder-img-lg d-block w-100" width="800" height="300"
                src="/img/hit11.jpg" alt>
              <div class="carousel-caption d-none d-md-block">
                <h5>欢迎来到校园智能信息发布平台</h5>
                <p>平台实现通知信息+校园论坛的整合</p>
              </div>
            </div>
            <div class="carousel-item">
              <img class="bd-placeholder-img bd-placeholder-img-lg d-block w-100" width="800" height="300"
                src="/img/hit22.jpg" alt>
              <div class="carousel-caption d-none d-md-block">
                <h5>Welcome to SmartInfo!</h5>
                <p>The platform provides newest notification and forum service</p>
              </div>
            </div>
            <div class="carousel-item">
              <img class="bd-placeholder-img bd-placeholder-img-lg d-block w-100" width="800" height="300"
                src="/img/hit33.jpeg" alt>
              <div class="carousel-caption d-none d-md-block">
                <h5>公告</h5>
                <p>如果您想参与网站的建设与管理，请与我们联系</p>
              </div>
            </div>
          </div>
          <button class="carousel-control-prev" type="button" data-bs-target="#carouselExampleCaptions"
            data-bs-slide="prev">
            <span class="carousel-control-prev-icon" aria-hidden="true"></span>
            <span class="visually-hidden">Previous</span>
          </button>
          <button class="carousel-control-next" type="button" data-bs-target="#carouselExampleCaptions"
            data-bs-slide="next">
            <span class="carousel-control-next-icon" aria-hidden="true"></span>
            <span class="visually-hidden">Next</span>
          </button>
        </div>
        <div class="row">
          <div class="col-sm-8">
            <div class="announcement">
              <div class="boardTitle">📰全站公告</div>
              <div class="boardContent">
                <div v-for="top in tops" :key="top.id"
                  class="py-1 border-bottom d-flex justify-content-between align-items-center">
                  <div>
                    <router-link class="card-title mb-0 text-decoration-none" :to="'/n/' + top.id">{{ top.title}}</router-link>
                  </div>
                  <div class="text-muted">
                    <small>[{{ $formatDate(top.launch_time) }}]</small>
                  </div>
                </div>
                <p v-if="tops.length === 0" class="card-text">暂无</p>
              </div>
            </div>
            <div class="row">
              <div class="important col-sm-6">
                <div class="boardTitle">⚠️重要通知</div>
                <div class="boardContent">
                  <div v-for="notification in notifications" :key="notification.id"
                       @mouseleave="hideTooltip(notification.id)" @mouseover="showTooltip(notification.id)"
                    class="notification-item py-1 border-bottom d-flex justify-content-between align-items-center">
                    <div>
                      <router-link class="card-title mb-0 text-decoration-none" :to="'/n/' + notification.id">{{
                          $truncate(notification.title, 15) }}</router-link>
                    </div>
                    <div class="text-muted">
                      <small>[{{ $formatDate(notification.launch_time) }}]</small>
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
                  <p v-if="notifications.length === 0" class="card-text">暂无</p>
                </div>
              </div>
              <div class="hot col-sm-6">
                <div class="boardTitle">🔥近期热帖</div>
                <div class="boardContent">
                  <div v-for="post in posts1" :key="post.id"
                    class="py-1 border-bottom d-flex justify-content-between align-items-center">
                    <div>
                      <router-link class="card-title mb-0 text-decoration-none" :to="'/p/' + post.id">{{ $truncate(post.title, 15)
                        }}</router-link>
                    </div>
                    <div class="text-muted">
                      <small>[{{ $formatDate(post.launch_time) }}]</small>
                    </div>
                  </div>
                  <p v-if="posts1.length === 0" class="card-text">暂无</p>
                </div>
              </div>
              <div class="study col-sm-6">
                <div class="boardTitle">📖学习答疑</div>
                <div class="boardContent">
                  <div v-for="post in posts2" :key="post.id"
                    class="py-1 border-bottom d-flex justify-content-between align-items-center">
                    <div>
                      <router-link class="card-title mb-0 text-decoration-none" :to="'/p/' + post.id">{{ $truncate(post.title, 15)
                        }}</router-link>
                    </div>
                    <div class="text-muted">
                      <small>[{{ $formatDate(post.launch_time) }}]</small>
                    </div>
                  </div>
                  <p v-if="posts2.length === 0" class="card-text">暂无</p>
                </div>
              </div>
              <div class="activity col-sm-6">
                <div class="boardTitle">❤️情感与生活</div>
                <div class="boardContent">
                  <div v-for="post in posts3" :key="post.id"
                    class="py-1 border-bottom d-flex justify-content-between align-items-center">
                    <div>
                      <router-link class="card-title mb-0 text-decoration-none" :to="'/p/' + post.id">{{ $truncate(post.title, 15)
                        }}</router-link>
                    </div>
                    <div class="text-muted">
                      <small>[{{ $formatDate(post.launch_time) }}]</small>
                    </div>
                  </div>
                  <p v-if="posts3.length === 0" class="card-text">暂无</p>
                </div>
              </div>
              <div class="activity col-sm-6">
                <div class="boardTitle">🏸体育结伴</div>
                <div class="boardContent">
                  <div v-for="post in posts4" :key="post.id"
                    class="py-1 border-bottom d-flex justify-content-between align-items-center">
                    <div>
                      <router-link class="card-title mb-0 text-decoration-none" :to="'/p/' + post.id">{{ $truncate(post.title, 15)
                        }}</router-link>
                    </div>
                    <div class="text-muted">
                      <small>[{{ $formatDate(post.launch_time) }}]</small>
                    </div>
                  </div>
                  <p v-if="posts4.length === 0" class="card-text">暂无</p>
                </div>
              </div>
              <div class="activity col-sm-6">
                <div class="boardTitle">🏫校园活动</div>
                <div class="boardContent">
                  <div v-for="post in posts5" :key="post.id"
                    class="py-1 border-bottom d-flex justify-content-between align-items-center">
                    <div>
                      <router-link class="card-title mb-0 text-decoration-none" :to="'/p/' + post.id">{{ $truncate(post.title, 15)
                        }}</router-link>
                    </div>
                    <div class="text-muted">
                      <small>[{{ $formatDate(post.launch_time) }}]</small>
                    </div>
                  </div>
                  <p v-if="posts5.length === 0" class="card-text">暂无</p>
                </div>
              </div>
            </div>
          </div>
          <div class="col-sm-4">
            <div class="navigation">
              <div class="boardTitle">✈️快捷导航</div>
              <div class="navigationContent">
                <div class="navigationRow" v-for="(item, index) in navigationItems" :key="index">
                  <div class="navigationImage">
                    <img :src="item.imgSrc" style="height: 60px" alt="">
                  </div>
                  <div class="navigationTitle">
                    <a :href="item.link" target="_blank">{{ item.title }}</a>
                  </div>
                </div>
              </div>
            </div>
            <div class="count">
              <div class="boardTitle">🌐网站统计</div>
              <div class="informationCount p-3">
                <a class="text-white text-decoration-none">
                  通知总数：{{ notificationCount }}
                </a>
                <a class="text-white text-decoration-none">
                  主题帖总数：{{ postCount }}
                </a>
                <a class="text-white text-decoration-none">
                  今日新帖：{{ newPostCount }}
                </a>
                <a class="text-white text-decoration-none">
                  今日新通知：{{ newPostCount }}
                </a>
                <a class="text-white text-decoration-none">
                  用户总数：{{ userCount }}
                </a>

              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Header from '../components/header.vue';
import Navbar from '../components/navbar.vue';
import axios from 'axios';

export default {
  name: 'Index',
  components: {
    Header,
    Navbar
  },
  data() {
    return {
      isAuthed: false,
      tops: [],
      notifications: [],
      posts1: [],
      posts2: [],
      posts3: [],
      posts4: [],
      posts5: [],
      notificationCount: 0,
      postCount: 0,
      newPostCount: 0,
      newNoticeCount: 0,
      userCount: 0,
      navigationItems: [
        { imgSrc: '/img/category_icons/24.jpg', link: 'http://today.hit.edu.cn', title: '校内新闻' },
        { imgSrc: '/img/navigation_icons/jw.jpg', link: 'http://jwts.hit.edu.cn', title: '本科生教务系统' },
        { imgSrc: '/img/navigation_icons/yj.jpg', link: 'http://yjsgl.hit.edu.cn/', title: '研究生管理系统' },
        { imgSrc: '/img/navigation_icons/mh.jpg', link: 'http://i.hit.edu.cn', title: '门户平台' },
        { imgSrc: '/img/navigation_icons/ivpn.jpg', link: 'http://i-hit-edu-cn.ivpn.hit.edu.cn', title: 'IVPN(校外)' },
        { imgSrc: '/img/navigation_icons/xg.jpg', link: 'https://xg.hit.edu.cn/xs/mh', title: '学工系统' },
        { imgSrc: '/img/navigation_icons/xyk.jpg', link: 'http://xyk.hit.edu.cn', title: '校园卡' },
        { imgSrc: '/img/navigation_icons/yd.jpg', link: 'http://venue-book.hit.edu.cn:8080/', title: '运动场地预约' },
        { imgSrc: '/img/navigation_icons/tsg.jpg', link: 'http://ic.lib.hit.edu.cn/', title: '图书馆预约' }
      ],
      tooltipVisible: {}, // { [notificationId]: boolean }
      notificationsMap: {}
    };
  },
  methods: {
    fetchData() {
      axios.get('http://192.168.1.100:8000/index_api/')
          .then(response => {
            const data = response.data;
            this.isAuthed = data.is_authed;
            this.tops = data.tops;
            this.notifications = data.notifications;
            this.posts1 = data.posts1;
            this.posts2 = data.posts2;
            this.posts3 = data.posts3;
            this.posts4 = data.posts4;
            this.posts5 = data.posts5;
            this.notificationCount = data.notification_count;
            this.postCount = data.post_count;
            this.newPostCount = data.new_post_count;
            this.newNoticeCount = data.new_notice_count;
            this.userCount = data.user_count;
            this.notifications.forEach(notification => {
              this.notificationsMap[notification.id] = {
                ...notification,
                loading: !notification.abstract || !notification.keywords || notification.keywords.length === 0,
                keywords: notification.keywords || [],
                abstract: notification.abstract || '',
              };
            });
          })
          .catch(error => {
            console.error('There was an error fetching the data!', error);
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
  },
  created() {
    this.fetchData();
  },

}
</script>

<style scoped>
.container{
  background-color: #f2f4f8;
}
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
</style>