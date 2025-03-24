<template>
  <nav class="navbar shadow navbar-expand-lg navbar-light bg-light" :class="{ 'fixed-top': isFixed }" ref="navbar">
    <div class="container">
      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          <li class="nav-item">
            <router-link class="nav-link" to="/index">首页</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/notice/center">通知中心</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/categories">板块分区</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/post/list">新帖列表</router-link>
          </li>
        </ul>
        <div class="d-flex align-items-center">
          <form class="form-inline mr-2">
            <input class="form-control" type="search" placeholder="请输入" aria-label="Search">
          </form>
          <button class="btn btn-primary" type="submit">搜索</button>
        </div>
        <ul class="navbar-nav ml-auto">
          <li v-if="isAuthenticated" class="nav-item dropdown">
            <a class="nav-link dropdown-toggle" id="navbarDropdown" role="button" data-bs-toggle="dropdown"
               aria-expanded="false">
              {{ user.nickname }}
            </a>
            <ul class="dropdown-menu" aria-labelledby="navbarDropdown">
              <li><router-link class="dropdown-item" to="/account/info">个人信息</router-link></li>
              <li><router-link class="dropdown-item" to="/account/edit">修改信息</router-link></li>
              <li><router-link class="dropdown-item" to="/account/posts">我的帖子</router-link></li>
              <li><router-link class="dropdown-item" to="/account/comments">我的评论</router-link></li>
              <li><hr class="dropdown-divider"></li>
              <li><a class="dropdown-item" href="#" @click.prevent="logout">注销</a></li>
            </ul>
          </li>
          <li v-else class="nav-item">
            <router-link class="nav-link" to="/regis">注册</router-link>
            <router-link class="nav-link" to="/login">登录</router-link>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script>
import { mapGetters, mapActions } from 'vuex';

export default {
  name: 'Navbar',
  data() {
    return {
      isFixed: false, // 导航栏是否固定
      initialOffset: 0 // 导航栏的初始偏移量
    };
  },
  computed: {
    ...mapGetters(['isAuthenticated', 'user'])
  },
  mounted() {
    this.setInitialOffset();
    window.addEventListener('scroll', this.handleScroll);
    window.addEventListener('resize', this.setInitialOffset);
  },
  beforeUnmount() {
    window.removeEventListener('scroll', this.handleScroll);
    window.removeEventListener('resize', this.setInitialOffset);
  },
  methods: {
    ...mapActions(['logout']),
    setInitialOffset() {
      this.$nextTick(() => {
        const navbar = this.$refs.navbar;
        this.initialOffset = navbar.offsetTop;
      });
    },
    handleScroll() {
      const scrollPosition = window.scrollY;
      if (scrollPosition >= this.initialOffset) {
        this.isFixed = true;
        document.body.style.paddingTop = `${this.$refs.navbar.offsetHeight}px`;
      } else {
        this.isFixed = false;
        document.body.style.paddingTop = '';
      }
    }
  }
};
</script>

<style scoped>
.fixed-top {
  position: fixed;
  top: 0;
  width: 100%;
  z-index: 1030;
}
</style>
