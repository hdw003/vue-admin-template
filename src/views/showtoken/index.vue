<template>
  <div class="app-container">
    <el-card>{{ token }}</el-card>
    <el-button type="primary" size="middle" @click="toGetToken()">
      刷新
    </el-button>
  </div>
</template>

<script>
import { getToken } from '@/api/article'
export default {

  data() {
    return {
      token: ''
    }
  },
  watch: {
    filterText(val) {
      this.$refs.tree2.filter(val)
    }
  },
  created() {
    this.toGetToken()
  },

  methods: {
    filterNode(value, data) {
      if (!value) return true
      return data.label.indexOf(value) !== -1
    },
    toGetToken() {
      getToken().then(response => {
        this.token = response.data.token
      })
    }
  }
}
</script>

