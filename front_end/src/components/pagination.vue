<template>
  <nav aria-label="Page navigation">
    <ul class="pagination">
      <li class="page-item" :class="{ disabled: currentPage === 1 }">
        <a class="page-link" href="#" @click.prevent="changePage(1)">首页</a>
      </li>
      <li class="page-item" :class="{ disabled: currentPage === 1 }">
        <a class="page-link" href="#" @click.prevent="changePage(currentPage - 1)">上一页</a>
      </li>
      <li class="page-item" v-for="page in pages" :key="page" :class="{ active: currentPage === page }">
        <a class="page-link" href="#" @click.prevent="changePage(page)">{{ page }}</a>
      </li>
      <li class="page-item" :class="{ disabled: currentPage === totalPages }">
        <a class="page-link" href="#" @click.prevent="changePage(currentPage + 1)">下一页</a>
      </li>
      <li class="page-item" :class="{ disabled: currentPage === totalPages }">
        <a class="page-link" href="#" @click.prevent="changePage(totalPages)">末页</a>
      </li>
      <li class="page-item">
        <form @submit.prevent="jumpToPage">
          <input v-model="jumpPage" type="text" class="form-control" placeholder="页码" style="display: inline-block; width: auto; margin-left: 10px;">
          <button class="btn btn-primary" type="submit" style="margin-left: 5px;">跳转</button>
        </form>
      </li>
    </ul>
  </nav>
</template>

<script>
export default {
  props: {
    totalPages: {
      type: Number,
      required: true
    },
    currentPage: {
      type: Number,
      required: true
    },
    pageRange: {
      type: Number,
      default: 5
    }
  },
  data() {
    return {
      jumpPage: ''
    }
  },
  computed: {
    pages() {
      let startPage = Math.max(1, this.currentPage - this.pageRange)
      let endPage = Math.min(this.totalPages, this.currentPage + this.pageRange)
      let pages = []
      for (let i = startPage; i <= endPage; i++) {
        pages.push(i)
      }
      return pages
    }
  },
  methods: {
    changePage(page) {
      if (page !== this.currentPage && page > 0 && page <= this.totalPages) {
        this.$emit('page-changed', page)
      }
    },
    jumpToPage() {
      let page = parseInt(this.jumpPage)
      if (page > 0 && page <= this.totalPages) {
        this.$emit('page-changed', page)
        this.jumpPage = ''
      }
    }
  }
}
</script>

<style scoped>
.pagination {
  display: flex;
  justify-content: center;
}
.page-item.disabled .page-link {
  pointer-events: none;
  cursor: default;
}
</style>
