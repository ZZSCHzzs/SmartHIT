<template>
  <div class="card border-0">
    <div class="card-header border-0">
      <h5 class="card-title">我的评论</h5>
    </div>
    <div class="card-body p-0">
      <div class="row">
        <div class="col-md-12">
          <div class="table-responsive">
            <table class="table">
              <thead>
              <tr>
                <th scope="col">评论内容</th>
                <th scope="col">发布时间</th>
                <th scope="col">所属主题帖</th>
                <th scope="col">操作</th>
              </tr>
              </thead>
              <tbody>
              <template v-if="comments.length > 0">
                <tr v-for="comment in comments" :key="comment.id">
                  <td>
                    {{ $truncate(comment.content, 20) }}
                  </td>
                  <td>{{ $formatDateTime(comment.created_at) }}</td>
                  <td>
                    <router-link :to="{ path: `/p/${comment.post_id}` }">
                      {{ $truncate(comment.post_title, 20) }}
                    </router-link>
                  </td>
                  <td>
                    <button @click="deleteComment(comment.id)" class="btn btn-sm btn-danger">
                      删除
                    </button>
                  </td>
                </tr>
              </template>
              <template v-else>
                <tr>
                  <td colspan="4">暂无评论</td>
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
  name: 'my_comments',
  data() {
    return {
      comments: [],
    };
  },
  methods: {
    fetchMyComments() {
      axios.get('account/comments/')
          .then((response) => {
            this.comments = response.data;
          })
          .catch((error) => {
            console.error('初始化时获取我的评论失败:', error);
          });
    },
    deleteComment(commentId) {
      axios.delete(`posts/${commentId}/delete_comment/`)
          .then(() => {
            // 删除成功后更新评论列表
            this.fetchMyComments();
          })
          .catch((error) => {
            console.error('删除评论失败:', error);
          });
    },
  },
  mounted() {
    this.fetchMyComments();
  },
};
</script>

<style scoped>
</style>
