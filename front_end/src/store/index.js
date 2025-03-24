import { createStore } from 'vuex';
import axios from '../axios.js'; // 导入配置好的 axios 实例

export default createStore({
    state: {
        accessToken: localStorage.getItem('accessToken') || '',
        refreshToken: localStorage.getItem('refreshToken') || '',
        isAuthenticated: !!localStorage.getItem('accessToken'),
        user: {}
    },
    mutations: {
        setAuth(state, { accessToken, refreshToken }) {
            state.accessToken = accessToken;
            state.refreshToken = refreshToken;
            state.isAuthenticated = true;
            localStorage.setItem('accessToken', accessToken);
            localStorage.setItem('refreshToken', refreshToken);
        },
        logout(state) {
            state.accessToken = '';
            state.refreshToken = '';
            state.isAuthenticated = false;
            state.user = {};
            localStorage.removeItem('accessToken');
            localStorage.removeItem('refreshToken');
        },
        setUser(state, user) {
            state.user = user;
        }
    },
    actions: {
        async handleLogin({ commit }, credentials) {
            try {
                const response = await axios.post('auth/login/', credentials);
                commit('setAuth', {
                    accessToken: response.data.access,
                    refreshToken: response.data.refresh
                });
                await this.dispatch('fetchUser');
            } catch (error) {
                console.error('登录失败:', error);
                throw error;
            }
        },
        async fetchUser({ commit, state, dispatch }) {
            if (!state.accessToken) {
                console.error('未找到有效的访问令牌');
                return; // 没有有效的令牌，直接返回
            }
            try {
                const response = await axios.get('auth/me/');
                commit('setUser', response.data);

            } catch (error) {
                console.error('获取用户信息失败:', error);
                if (error.response && error.response.status === 401) {
                    dispatch('logout'); // 处理认证失败的情况
                }
                throw error;
            }
        },
        logout({ commit }) {
            commit('logout');
        }
    },
    getters: {
        isAuthenticated: state => state.isAuthenticated,
        accessToken: state => state.accessToken,
        refreshToken: state => state.refreshToken,
        user: state => state.user
    }
});
