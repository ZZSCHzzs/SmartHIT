<template>



    <div class="container mt-4">
        <div class="row no-gutters">
            <div class="d-flex justify-content-between align-items-center mb-4 col-sm-12">
                <h2 class="mb-0">新贴列表</h2>
                <div v-if="isAuthenticated">
                    <router-link :to="{ path: `/post/launch` }" class="btn btn-primary text-white">发表主题帖</router-link>
                </div>
            </div>
        </div>
        <div v-if="posts.length > 0" >
          <div v-for="post in posts">
            <div class="row mb-4">
                <div class="col-md-12">
                    <div class="card shadow">
                        <div style="display: flex">
                            <div class="card-header text-center" style="display: flex; align-items: center; justify-content: center;">
                                {{ post.category }}
                            </div>

                            <div class="card-body pl-3 pr-3 pb-4 pt-4">
                                <h5 class="card-title mb-0"><router-link :to="{ path: `/p/${post.id}` }" >{{ post.title }}</router-link></h5>
                                <div class="d-flex justify-content-between align-items-center" style="height: 100%;">
                                    <div>
                                        <p class="card-text mb-0 text-muted">{{ post.author }}</p>
                                                                        <div v-if="post.last_comment_user">
                                    <div class="align-items-center"
                                         style="height: 100%;">
                                        <div>
                                            <p class="card-text mb-0 text-muted">
                                                最后回复：{{ post.last_comment_user }}
                                                {{ post.formatted_last_comment_time }}
                                            </p>
                                        </div>
                                    </div>
                                </div>
                                    </div>
                                    <div>
                                        <p class="card-text mb-0 text-muted">
                                            {{ post.formatted_launch_time }}</p>
                                    </div>
                                </div>

                            </div>


                        </div>
                    </div>
                </div>
            </div>
        </div></div>

        <!-- 分页组件 -->
        <ul class="pagination justify-content-center">
            <Pagination current-page="1" total-pages="10"></Pagination>
        </ul>
    </div>


</template>
<script>
import Pagination from "@/components/pagination.vue";
import axios from "@/axios.js";
import {mapGetters} from "vuex";
export default {
  name: 'post_list',
  components: {Pagination},
  data(){
    return{
      posts: [],
    }
  },
  computed: {
    ...mapGetters(['isAuthenticated', 'user'])
  },
  methods:{
    fetchPostList(){
      axios.get("posts/listall/").then(res=>{
        this.posts = res.data;
      })
    },
  },
  mounted() {
    this.fetchPostList();

  }
};
</script>
<style scoped>
</style>
