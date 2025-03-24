<!-- CategoryItem.vue -->
<template>
  <div>
    <button v-if="!isFollowing" class="btn btn-primary" @click="followCategory">关注</button>
    <button v-else class="btn btn-success" @click="unfollowCategory">取消关注</button>
  </div>
</template>

<script>
import axios from '@/axios';

export default {
  props: ['category'],
  data() {
    return {
      isFollowing: false,
      subscription: {},
    };
  },
  methods: {
    followCategory() {
      axios.post('subscriptions/', { cid: this.category.cid })
          .then(response => {
            this.isFollowing = true;
            console.log(response.data);
          })
          .catch(error => {
            console.error('关注分类帖子失败:', error);
          });
    },
    unfollowCategory() {
      axios.delete(`subscription/${this.subscription.id}/`)
          .then(response => {
            this.isFollowing = false;
            console.log(response.data);
          })
          .catch(error => {
            console.error('取消关注分类帖子失败:', error);
          });
    },
    checkIfFollowing() {
      axios.post(`subscriptions/check/`, { cid: this.category.cid })
          .then(response => {
            this.isFollowing = response.data.is_following;
            this.subscription = response.data.subscription;
          })
          .catch(error => {
            console.error('检查关注状态失败:', error);
          });
    },
  },
  mounted() {
    this.checkIfFollowing();
  },
};
</script>
