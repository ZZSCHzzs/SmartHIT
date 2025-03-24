<template>
  <div class="container mt-4">
    <div class="card mt-5">
      <div class="card-header bg-theme-light text-white text-center">
        <h3 class="m-0 p-2">{{ category_object.name }}</h3>

      </div>
      <div class="card-body">
        <div v-if="category_object.description">
          <p class="card-text">{{ category_object.description }}</p>
        </div>
        <div v-else>
          <p class="card-text">暂无描述</p>
        </div>
        <div v-if="category_object.top_pic">
          <img :src="category_object.top_pic" class="img-fluid" alt="图片">
        </div>
      </div>
    </div>
    <div class="row no-gutters mt-3">
      <div class="d-flex justify-content-between align-items-center mb-4 col-sm-12">
        <h2 class="mb-0">帖子列表</h2>

        <div class="d-flex align-items-center">
          <subscription class="m-3" :category="category_object" /> <!-- 调整订阅按钮位置 -->

          <!-- 使用 Bootstrap 网格系统控制按钮的显示 -->
          <div class="d-flex justify-content-end align-items-center">
            <div v-if="is_authed" class="ml-3">
              <router-link :to="{ path: `/post/launch`, query: { cid: category_object.cid } }" class="btn btn-primary text-white">发表主题帖</router-link>
            </div>
          </div>
        </div>
      </div>

    </div>
    <div v-if="posts.length > 0">
      <div v-for="post in posts" :key="post.id" class="row mb-4">
        <div class="col-md-12">
          <div class="card shadow">
            <div style="display: flex">
              <div class="card-header text-center" style="display: flex; align-items: center; justify-content: center;">
                {{ post.category }}
              </div>
              <div class="card-body pl-3 pr-3 pb-4 pt-4">
                <h5 class="card-title mb-0">
                  <router-link :to="{ path: `/p/${post.id}` }">{{ post.title }}</router-link>
                </h5>
                <div class="d-flex justify-content-between align-items-center" style="height: 100%;">
                  <div>
                    <p class="card-text mb-0 text-muted">{{ post.author }}</p>
                    <div v-if="post.comments && post.comments.length > 0">
                      <p class="card-text mb-0 text-muted">
                        最后回复：{{ post.last_comment_user }}
                        {{ post.formatted_last_comment_time }}
                      </p>
                    </div>
                  </div>
                  <div>
                    <p class="card-text mb-0 text-muted">{{ post.formatted_launch_time }}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div v-else>
      <p class="text-center">暂无帖子</p>
    </div>
    <!-- 分页组件 -->
    <ul class="pagination justify-content-center">
      <li class="page-item" v-if="page > 1">
        <a class="page-link" @click.prevent="fetchPosts(page - 1)">上一页</a>
      </li>
      <li class="page-item" v-if="hasMore">
        <a class="page-link" @click.prevent="fetchPosts(page + 1)">下一页</a>
      </li>
    </ul>
  </div>
</template>

<script>
import axios from '@/axios';
import subscription from '@/components/subscription.vue';

export default {
  name: 'CategoryDetail',
  components: {
    subscription,
  },
  data() {
    return {
      category_object: {},
      posts: [],
      page: 1,
      hasMore: false,
      is_authed: true,  // 假设用户已通过认证
    };
  },
  mounted() {
    this.fetchCategoryDetail();
    this.fetchPosts();
  },
  methods: {
    fetchCategoryDetail() {
      const cid = this.$route.params.cid;
      axios.get(`categories/${cid}/view/`)
          .then(response => {
            this.category_object = response.data;
          })
          .catch(error => {
            console.error('Error fetching category detail:', error);
          });
    },
    fetchPosts(page = 1) {
      const cid = this.$route.params.cid;
      axios.get(`categories/${cid}/posts/`)
          .then(response => {
            this.posts = response.data;
            this.page = page;
            this.hasMore = !!response.data.next;
          })
          .catch(error => {
            console.error('Error fetching posts:', error);
          });
    }
  }
};
</script>

<style scoped>
/* 根据需要添加样式 */
</style>
