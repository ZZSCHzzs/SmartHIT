<template>
  <div class="card border-0">
    <div class="card-header border-0">
      <h5 class="card-title">我的关注</h5>
    </div>
    <div class="card-body p-0">
      <div class="row">
        <div class="col-md-12">
          <div class="table-responsive">
            <table class="table">
              <thead>
              <tr>
                <th scope="col">关注的主题</th>
                <th scope="col">操作</th>
              </tr>
              </thead>
              <tbody>
              <template v-if="subscriptions.length > 0">
                <tr v-for="subscription in subscriptions" :key="subscription.category.cid">
                  <td>
                    <router-link :to="{ path: `/c/${subscription.category.cid}` }">
                      {{ subscription.category.name }}
                    </router-link>
                  </td>
                  <td>
                    <button @click="deleteSubscription(subscription.id)" class="btn btn-sm btn-danger">
                      删除
                    </button>
                  </td>
                </tr>
              </template>
              <template v-else>
                <tr>
                  <td colspan="4">暂无关注</td>
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
import subscription from "@/components/subscription.vue";
import axios from "@/axios";

export default {
  name: 'subscription',
  computed: {
    subscription() {
      return subscription
    }
  },
  data() {
    return {
      subscriptions: [],
    };
  },
  methods: {
    fetchSubscriptions() {
      axios.get('account/subscriptions/')
        .then((response) => {
          this.subscriptions = response.data;
        })
        .catch((error) => {
          console.error(error);
        });
    },
    deleteSubscription(subscriptionId) {
      axios.delete(`subscriptions/${subscriptionId}/`)
        .then((response) => {
          this.subscriptions = this.subscriptions.filter(subscription => subscription.id !== subscriptionId);
        })
        .catch((error) => {
          console.error('失败:', error);
        });
    },
  },
  mounted() {
    this.fetchSubscriptions();
  },
};
</script>
<style scoped>
</style>
