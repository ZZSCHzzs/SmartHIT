<template>
  <div class="container">
    <div class="row justify-content-center">
      <div class="col-md-12">
        <div class="card shadow mt-4">
          <div class="card-body">
            <h2 class="mb-3 font-weight-bold">{{ post.title }}</h2>
            <div class="d-flex justify-content-between">
              <p class="mb-0 text-muted">{{ post.author }}</p>
              <p class="mb-0 text-muted">{{ post.formatted_launch_time }}</p>
            </div>
            <hr>
            <div class="post-content" v-html="post.text"></div>
            <div v-if="post.additional_information">
              <hr>
              <p class="font-weight-bold">附加信息:</p>
              <p>{{ post.additional_information }}</p>
            </div>
            <div v-if="post.additional_graphics">
              <hr>
              <p class="font-weight-bold">附加图片:</p>
              <img :src="post.additional_graphics" class="img-fluid rounded" alt="附加图片">
            </div>
            <hr>
            <div class="d-flex justify-content-between">
              <p class="mb-0 text-muted">点赞: {{ post.likes }}</p>
              <div>
                <div v-if="isAuthenticated">
                  <div v-if="user.uid === post.launcher_uid">
                    <a class="text-danger delete-post col-4 text-decoration-none" @click.prevent="deletePost(post.id)">删除主题帖</a>
                  </div>
                </div>
                <p class="mb-0 text-muted">浏览次数: {{ post.view_times }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="mt-4">
      <div class="card mt-4 shadow mb-3">
        <div class="card-body">
          <h4 class="mb-3">写评论</h4>
          <form @submit.prevent="submitComment">
            <div class="form-group">
              <label for="comment" class="sr-only">评论</label>
              <textarea v-model="newComment" class="form-control" id="comment" rows="3"></textarea>
            </div>
            <button type="submit" class="btn btn-primary">提交评论</button>
          </form>
        </div>
      </div>
      <h3 class="mb-3">评论</h3>
      <div v-if="comments.length > 0">
        <div v-for="comment in comments" :key="comment.id">
          <div class="card mb-2 shadow">
            <div class="card-body">
              <p class="mb-2 mt-2">
                <h6 class="font-bold">#{{ comment.index }}</h6>
                <a>{{ comment.content }}</a>
              </p>
              <hr>
              <div class="d-flex justify-content-between mt-1">
                <div>
                  <p class="mb-0 text-muted">{{ comment.author }}</p>
                </div>
                <div>
                  <div v-if="isAuthenticated">
                    <div v-if="user.uid === comment.author_id || user === post.launcher_uid">
                      <a class="text-danger delete-comment text-decoration-none" @click.prevent="deleteComment(comment.id)">删除评论</a>
                    </div>
                  </div>
                  <p class="mb-0 text-muted ml-3">{{ comment.formatted_time }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div v-else>
        <div class="card mb-2 shadow">
          <div class="card-body">
            <p>目前还没有评论。</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from '@/axios.js';
import {mapGetters} from "vuex";

export default {
  data() {
    return {
      post: {},
      comments: [],
      comment: '',
      newComment: '',
      is_authed: true,  // 假设用户已经通过认证
      user: {},  // 假设用户信息已经加载
    };
  },
  computed: {
    ...mapGetters(['isAuthenticated', 'user'])
  },
  mounted() {
    this.fetchPostDetail();
  },
  methods: {
    fetchPostDetail() {
      const postId = this.$route.params.pid;
      axios.get(`posts/${postId}/view/`)
          .then(response => {
            this.post = response.data.post;
            this.comments = response.data.comments;
          })
          .catch(error => {
            console.error('Error fetching post detail:', error);
          });
    },
    submitComment() {
      const postId = this.$route.params.pid;
      axios.post(`posts/${postId}/add_comment/`, { comment: this.newComment })
          .then(response => {
            this.comments.push(response.data);
            this.newComment = '';
          })
          .catch(error => {
            console.error('Error submitting comment:', error);
          });
    },
    deleteComment(commentId) {
      axios.post(`posts/${commentId}/delete_comment/`)
          .then(response => {
            this.comments = this.comments.filter(comment => comment.id !== commentId);
          })
          .catch(error => {
            console.error('Error deleting comment:', error);
          });
    },
    deletePost(postId) {
      axios.post(`posts/${postId}/delete/`)
          .then(response => {
            this.$router.push('/');
          })
          .catch(error => {
            console.error('Error deleting post:', error);
          });
    },
    formatMessage(text) {
      return text.replace(/\n/g, "<br>");
    },
  }
};
</script>

<style scoped>
/* 根据需要添加样式 */
</style>
