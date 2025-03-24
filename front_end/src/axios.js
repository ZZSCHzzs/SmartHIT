import axios from 'axios';
import store from './store'; // 导入 Vuex store
import router from './router'; // 导入 Vue Router

const instance = axios.create({
    baseURL: 'http://192.168.1.100:8000/', // Django 后端的基本 URL
    timeout: 1000,
    headers: {
        'Content-Type': 'application/json'
    }
});

// 请求拦截器
instance.interceptors.request.use(config => {
    const token = store.getters.accessToken;
    if (token) {
        config.headers['Authorization'] = `Bearer ${token}`;
    }
    console.log('请求头:', config.headers);
    return config;
}, error => {
    return Promise.reject(error);
});

// 响应拦截器
instance.interceptors.response.use(response => {
    return response;
}, async error => {
    const originalRequest = error.config;
    if (error.response && error.response.status === 401 && !originalRequest._retry) {
        originalRequest._retry = true;
        try {
            await store.dispatch('logout'); // 尝试注销用户
            router.push('/login');
        } catch (logoutError) {
            console.error('注销用户失败:', logoutError);
        }
    }
    return Promise.reject(error);
});

export default instance;
