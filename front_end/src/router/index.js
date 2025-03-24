import { createRouter, createWebHistory } from 'vue-router';
import Index from '../views/index.vue';
// 导入其他视图组件
import Regis from '@/views/auth/regis.vue';
import Login from '@/views/auth/login.vue';

import notice_list from '@/views/notice/notice_list.vue';
import notice_center from '@/views/notice/notice_center.vue';
import notice_launch from "@/views/notice/notice_launch.vue";
import notice_detail from "@/views/notice/notice_detail.vue";

import post_list from "@/views/post/post_list.vue";
import post_launch from "@/views/post/post_launch.vue";
import post_detail from "@/views/post/post_detail.vue";
import categories from "@/views/post/categories.vue";
import category_detail from "@/views/post/category_detail.vue";

import user_center from "@/views/user/user_center.vue";
import view_info from "@/views/user/view_info.vue";
import edit_info from "@/views/user/edit_info.vue";
import my_posts from "@/views/user/my_posts.vue";
import my_comments from "@/views/user/my_comments.vue";
import my_subscription from "@/views/user/my_subscription.vue";

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', redirect: '/index'},
    { path: '/index', name: 'index', component: Index },
    // 添加其他路由配置
    { path: '/regis', name: 'regis', component: Regis },
    { path: '/login', name: 'login', component: Login },
    // { path: '/logout', name: 'logout', component: Logout },

    { path: '/notice', redirect: '/notice/center'},
    { path: '/notice/list', name: 'notice_list', component: notice_list },
    { path: '/notice/launch', name: 'notice_launch', component: notice_launch },
    { path: '/n/:nid', name: 'notice_detail', component: notice_detail },
    { path: '/notice/center', name: 'notice_center', component: notice_center },

    { path: '/post/launch', name: 'post_launch', component: post_launch },
    { path: '/post/list', name: 'post_list', component:post_list },
    { path: '/p/:pid', name: 'post_detail', component: post_detail },
    { path: '/categories', name: 'categories', component: categories },
    { path: '/c/:cid', name: 'category_detail', component: category_detail },
    {
      path: '/account',
      name: 'account',
      component: user_center,
      redirect: '/account/info',
      children: [
        { path: 'info', name: 'view_info', component: view_info },
        { path: 'edit', name: 'editInfo', component: edit_info },
        { path: 'posts', name: 'myPosts', component: my_posts },
        { path: 'comments', name: 'myComments', component: my_comments },
        { path: 'subscription', name: 'subscription', component: my_subscription },
      ]
    },
  ]
});

export default router;
