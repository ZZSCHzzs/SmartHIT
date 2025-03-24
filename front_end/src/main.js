import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import store from './store';

// 引入 jQuery
import 'jquery/dist/jquery.js';
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap/dist/js/bootstrap.js';
import 'bootstrap-icons/font/bootstrap-icons.css';
import './assets/main.css';

import { format } from 'date-fns';

// 创建 Vue 应用实例
const app = createApp(App);

// 定义全局日期格式化方法
app.config.globalProperties.$formatDate = function(value) {
    if (!value) return '';
    return format(new Date(value), 'yyyy.MM.dd');
};

// 定义全局日期时间格式化方法
app.config.globalProperties.$formatDateTime = function(value) {
    if (!value) return '';
    return format(new Date(value), 'yyyy.MM.dd HH:mm');
};

// 定义全局文本截取方法
app.config.globalProperties.$truncate = function(value, length) {
    if (!value) return '';
    if (value.length <= length) return value;
    return value.substring(0, length) + '...';
};

// 使用路由
app.use(router);
app.use(store);

// 在应用启动时恢复用户信息
store.dispatch('fetchUser').then(() => {
    // 挂载应用
    app.mount('#app');
}).catch(error => {
    console.error('初始化时获取用户信息失败:', error);
    // 即使获取用户信息失败，也要挂载应用
    app.mount('#app');
});
