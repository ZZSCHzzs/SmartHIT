<template>
  <!-- user_center -->
  <div class="container mt-4">
    <div class="row">
      <div class="col-md-3">
        <div class="text-center mb-4">
          <h5 class="mb-3 mt-3">{{ user.nickname }}</h5>
        </div>
        <div class="list-group">
          <router-link to="/account/info" class="list-group-item list-group-item-action" :class="{ active: isActive('/account/info') }">查看信息</router-link>
          <router-link to="/account/edit" class="list-group-item list-group-item-action" :class="{ active: isActive('/account/edit') }">修改信息</router-link>
          <router-link to="/account/posts" class="list-group-item list-group-item-action" :class="{ active: isActive('/account/posts') }">我的帖子</router-link>
          <router-link to="/account/comments" class="list-group-item list-group-item-action" :class="{ active: isActive('/account/comments') }">我的评论</router-link>
          <router-link to="/account/subscription" class="list-group-item list-group-item-action" :class="{ active: isActive('/account/subscription') }">关注版面</router-link>
        </div>
      </div>
      <div class="col-md-9">
        <div class="card">
          <div class="card-body">
            <router-view></router-view>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex';

export default {
  name: 'user_center',
  computed: {
    ...mapGetters(['isAuthenticated', 'user'])
  },
  methods: {
    isActive(path) {
      // 获取当前路由路径
      let currentPath = this.$route.path;
      // 判断当前路由路径是否与给定的路径匹配
      return currentPath === path;
    }
  }
};
</script>

<style scoped>
.list-group .list-group-item.active {
  background-color: #007bff;
  color: #fff;
}
</style>
