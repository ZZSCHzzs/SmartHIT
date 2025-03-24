<template>
  <div class="regis-page">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-md-6">
          <div class="card mt-5">
            <div class="card-body regis-card shadow">
              <h2 class="text-center mb-4 regis-title">注册您的账号</h2>
              <form @submit.prevent="register">
                <div class="form-group mb-4">
                  <label class="regis-label" for="username">用户名</label>
                  <input type="text" v-model="username" class="form-control" id="username" required>
                </div>
                <div class="form-group mb-4">
                  <label class="regis-label" for="password">密码</label>
                  <input type="password" v-model="password" class="form-control" id="password" required>
                </div>
                <div class="form-group mb-4">
                  <label class="regis-label" for="password_confirm">确认密码</label>
                  <input type="password" v-model="password_confirm" class="form-control" id="password_confirm" required>
                </div>
                <div class="form-group mb-4">
                  <label class="regis-label" for="nickname">昵称</label>
                  <input type="text" v-model="nickname" class="form-control" id="nickname" required>
                </div>
                <div class="form-group mb-4">
                  <label class="regis-label" for="stu_id">学工号</label>
                  <input type="text" v-model="stu_id" class="form-control" id="stu_id" required>
                </div>
                <div class="form-group mb-4">
                  <label class="regis-label" for="department">院系</label>
                  <select v-model="department" class="form-control" id="department">
                    <option v-for="dept in departments" :key="dept.id" :value="dept.id">{{ dept.name }}</option>
                  </select>
                </div>
                <button type="submit" class="btn btn-primary btn-block col-sm-12">注册</button>
              </form>
              <router-link to="/login">已有账号?立即登录</router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "@/axios";

export default {
  name: 'Regis',
  data() {
    return {
      username: '',
      password: '',
      password_confirm: '',
      nickname: '',
      stu_id: '',
      department: '',
      departments: []
    };
  },
  created() {
    this.fetchDepartments();
  },
  methods: {
    async fetchDepartments() {
      try {
        const response = await axios.get('/departments/');
        this.departments = response.data;
      } catch (error) {
        console.error(error);
        alert('获取院系信息失败');
      }
    },
    async register() {
      try {
        await axios.post('/auth/register/', {
          username: this.username,
          password: this.password,
          password_confirm: this.password_confirm,
          nickname: this.nickname,
          stu_id: this.stu_id,
          department: this.department
        });
        this.$router.push('/login');
      } catch (error) {
        console.error(error);
        alert('注册失败，请检查输入');
      }
    }
  }
};
</script>

<style scoped>

</style>
