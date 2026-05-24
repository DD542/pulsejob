<template>
  <div class="section-title">{{ title }}</div>
</template>

<script setup>
defineProps({ title: String })
</script>

<style scoped>
.section-title {
  font-family: 'DM Mono', monospace;
  font-size: 10px;
  letter-spacing: 3px;
  color: #444;
  text-transform: uppercase;
  margin-bottom: 20px;
  padding-bottom: 12px;
  border-bottom: 1px solid #1a1a1a;
}
</style>