<template>
  <!-- templates/user/my_posts.html -->
  <div class="card border-0">
    <div class="card-header border-0">
      <h5 class="card-title">我的帖子</h5>
    </div>
    <div class="card-body p-0 ">
      <div class="row">
        <div class="col-md-12">
          <div class="table-responsive">
            <table class="table">
              <thead>
              <tr>
                <th scope="col">标题</th>
                <th scope="col">发布时间</th>
                <th scope="col">浏览次数</th>
                <th scope="col">评论数</th>
                <th scope="col">操作</th>
              </tr>
              </thead>
              <tbody>
              <template v-if="posts.length > 0">
                <tr v-for="post in posts" :key="post.id">
                  <td>
                    <router-link :to="{ path: `/p/${post.id}` }">{{ $truncate(post.title, 20) }}</router-link>
                  </td>
                  <td>{{ $formatDateTime(post.launch_time) }}</td>
                  <td>{{ post.view_times }}</td>
                  <td>{{ post.comments_count }}</td>
                  <td>
                    <button @click="deletePost(post.id)" class="btn btn-sm btn-danger">删除</button>
                  </td>
                </tr>
              </template>
              <template v-else>
                <tr>
                  <td colspan="5">暂无帖子</td>
                </tr>
              </template>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "@/axios.js";

export default {
  name: 'my_posts',
  data() {
    return {
      posts: [],
    };
  },
  methods: {
    fetchMyPosts() {
      axios.get('account/posts/')
          .then((response) => {
            this.posts = response.data;
          })
          .catch((error) => {
            console.error('初始化时获取我的帖子失败:', error);
          });
    },
    deletePost(postId) {
      axios.delete(`posts/${postId}/`)
          .then(() => {
            // 删除成功后更新列表
            this.posts = this.posts.filter(post => post.id !== postId);
            console.log('帖子删除成功');
          })
          .catch((error) => {
            console.error('删除帖子失败:', error);
          });
    },
  },
  mounted() {
    this.fetchMyPosts();
  },
};
</script>

<style scoped>
</style>
