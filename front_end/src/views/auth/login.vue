<template>
  <!-- login.vue -->
  <div class="login-page">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-md-5">
          <div class="card mt-5">
            <div class="card-body login-card shadow">
              <h2 class="text-center mb-4 login-title">登录</h2>
              <form @submit.prevent="Login">
                <div class="form-group mb-4">
                  <label class="font-bold">用户名</label>
                  <input v-model="username" class="form-control" required>
                </div>
                <div class="form-group mb-4">
                  <label class="font-bold">密码</label>
                  <input v-model="password" type="password" class="form-control" required>
                </div>
                <button type="submit" class="btn btn-primary col-sm-12 btn-block">登录</button>
              </form>
              <div class="mt-2" style="display: flex; justify-content: space-between;">
                <router-link :to="{ path: `/regis` }">未注册？请先注册</router-link>
                <router-link :to="{ path: `/forgot-password` }">忘记密码？</router-link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapActions } from 'vuex';

export default {
  name: 'Login',
  data() {
    return {
      username: '',
      password: ''
    };
  },
  methods: {
    ...mapActions(['handleLogin']), // 修改这里的映射名称为 handleLogin
    async Login() { // 修改方法名为 handleLogin
      try {
        await this.handleLogin({username: this.username, password: this.password}); // 调用 handleLogin 方法
        this.$router.push('/'); // 登录成功后跳转到主页
      } catch (error) {
        console.error('登录失败', error);
      }
    }
  }
};
</script>