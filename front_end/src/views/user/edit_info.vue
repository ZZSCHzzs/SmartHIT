<template>
  <div class="row">
    <div class="col-md-12">
      <div class="card border-0">
        <div class="card-header border-0">
          <h5 class="card-title">修改个人信息</h5>
        </div>
        <div class="card-body col-sm-6">
          <form @submit.prevent="submitForm" enctype="multipart/form-data" novalidate>
            <div class="form-group">
              <label class="regis-label">昵称</label>
              <input v-model="nickname" type="text" class="form-control" placeholder="请输入昵称" />
            </div>
            <div class="form-group">
              <label class="regis-label">QQ</label>
              <input v-model="qq" type="text" class="form-control" placeholder="请输入QQ号" />
            </div>
            <div class="form-group">
              <label class="regis-label">微信号</label>
              <input v-model="wechat" type="text" class="form-control" placeholder="请输入微信号" />
            </div>
            <div class="form-group">
              <label class="regis-label">姓名</label>
              <input v-model="name" type="text" class="form-control" placeholder="请输入姓名" />
            </div>
            <div class="form-group">
              <label class="regis-label">学工号</label>
              <input v-model="stu_id" type="text" class="form-control" placeholder="请输入学工号" />
            </div>
            <div class="form-group">
              <label class="regis-label">院系</label>
              <select v-model="department" class="form-control">
                <option v-for="dept in departments" :key="dept.id" :value="dept.id">{{ dept.name }}</option>
              </select>
            </div>
            <button type="submit" class="btn btn-primary">提交修改</button>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from '@/axios';

export default {
  name: 'edit_info',
  data() {
    return {
      nickname: '',
      qq: '',
      wechat: '',
      name: '',
      stu_id: '',
      department: '', // 初始化为空，等待选项加载
      departments: [], // 用来存储从后端获取的院系选项
    };
  },
  methods: {
    fetchUserInfo() {
      axios.get('auth/me/')
          .then(response => {
            const userData = response.data;
            this.nickname = userData.nickname;
            this.qq = userData.qq;
            this.wechat = userData.wechat;
            this.name = userData.name;
            this.stu_id = userData.stu_id;
            this.department = userData.department.id; // 假设后端返回的是院系的 ID
          })
          .catch(error => {
            console.error('获取用户信息失败:', error);
          });
    },
    fetchDepartments() {
      axios.get('departments/')
          .then(response => {
            this.departments = response.data;
          })
          .catch(error => {
            console.error('获取院系列表失败:', error);
          });
    },
    submitForm() {
      const formData = {
        nickname: this.nickname,
        qq: this.qq,
        wechat: this.wechat,
        name: this.name,
        stu_id: this.stu_id,
        department: this.department,
      };

      axios.post('account/edit/', formData)
          .then(response => {
            console.log('表单提交成功:', response.data);
            // 处理成功逻辑
          })
          .catch(error => {
            console.error('表单提交失败:', error);
          });
    },
  },
  mounted() {
    this.fetchUserInfo(); // 获取用户信息填充表单
    this.fetchDepartments(); // 获取院系选项列表
  },
};
</script>

<style scoped>
.form-control {
  margin-bottom: 10px;
}
</style>
