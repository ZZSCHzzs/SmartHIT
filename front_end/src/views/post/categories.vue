<template>
  <div class="container">
    <h2 class="h2 mt-4 mb-3">版面列表</h2>
    <div v-if="category_types.length > 0">
      <div v-for="category_type in category_types" :key="category_type.id">
        <div class="row mt-3 mb-5">
          <div class="col">
            <div class="card">
              <div class="bg-theme-light card-title p-2 text-white text-center">
                <h3 class="m-1">{{ category_type.name }}</h3>
              </div>
              <div class="card-body">
                <div class="row">
                  <div v-if="category_type.categories.length > 0" class="d-flex flex-wrap">
                    <div v-for="category in category_type.categories" :key="category.id" class="col-md-4 mb-3">
                      <div class="card border-0">
                        <div class="card-body text-center">
                          <img :src="getCategoryIconPath(category.cid)" alt="" class="card-img mb-2">
                          <h4 class="card-title" style="font-size: 1.7rem; font-weight: bold;">
                            <router-link :to="{ path: `/c/${category.cid}` }" class="text-dark text-decoration-none">{{ category.name }}</router-link>
                          </h4>
                        </div>
                      </div>
                    </div>
                  </div>
                  <div v-else>
                    <p>No categories available.</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div v-else>
      <p>Loading...</p>
    </div>
  </div>
</template>

<script>
import axios from "@/axios";

export default {
  name: "Category",
  data() {
    return {
      category_types: [],
      loading: true,
      error: null
    };
  },
  methods: {
    async fetchCategoryList() {
        axios.get("categories/type/")
            .then(response => {
              this.category_types = response.data;
            })
            .catch(error => {
          console.error('Error fetching data:', error);
          })
      },
    getCategoryIconPath(cid) {
      return `/img/category_icons/${cid}.jpg`;
    }
    },
  mounted() {
    this.fetchCategoryList();
  }
};
</script>

<style scoped>
.h3 {
  font-size: 1.5rem;
}

.card-header {
  background-color: #f8f9fa;
  color: #495057;
}

.card-img {
  height: 100px;
  width: 100px;
}
</style>
