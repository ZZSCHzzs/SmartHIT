<template>
  <div class="row">
    <div class="col-md-12">
      <div class="card border-0 bg-white">
        <div class="card-header border-0">
          <h5 class="card-title">账号信息</h5>
        </div>
        <div class="card-body">
          <p><strong>用户名：</strong> {{ account.username }}</p>
          <p><strong>UID：</strong> {{ account.uid }}</p>
          <p><strong>注册日期：</strong> {{ $formatDate(account.regis_time) }}</p>
          <p><strong>权限组：</strong> {{ account.permission_group?.name }}</p>
          <p><strong>账号状态：</strong> {{ account.state?.name }}</p>
        </div>
      </div>
      <div class="card border-0 bg-white">
        <div class="card-header border-0">
          <h5 class="card-title">个人信息</h5>
        </div>
        <div class="card-body">
          <p><strong>昵称：</strong> {{ account.nickname }}</p>
          <p><strong>QQ：</strong> {{ account.qq }}</p>
          <p><strong>微信号：</strong> {{ account.wechat }}</p>
          <p><strong>姓名：</strong> {{ account.name }}</p>
          <p><strong>学工号：</strong> {{ account.stu_id }}</p>
          <p><strong>院系：</strong> {{ account.department?.name }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from '@/axios';

export default {
  name: 'view_info',
  data() {
    return {
      account: {},
    };
  },
  methods: {
    fetchUserInfo() {
      axios.get('auth/me/')
          .then((response) => {
            this.account = response.data;
          })
          .catch((error) => {
            console.error('初始化时获取用户信息失败:', error);
          });
    },
  },
  mounted() {
    this.fetchUserInfo();
  },
};
</script>

<style scoped>
</style>
