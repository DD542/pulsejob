<template>
  <div class="chart-wrapper">
    <div
      v-for="(item, index) in data"
      :key="index"
      class="bar-row"
    >
      <div class="bar-label">{{ item[labelKey] }}</div>
      <div class="bar-track">
        <div
          class="bar-fill"
          :style="{
            width: (item[valueKey] / maxValue * 100) + '%',
            background: color
          }"
        ></div>
      </div>
      <div class="bar-value">{{ item[valueKey] }}</div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  data: Array,
  labelKey: String,
  valueKey: String,
  color: {
    type: String,
    default: 'linear-gradient(90deg, #2a2a2a, #e8e8e8)'
  }
})

const maxValue = computed(() => {
  if (!props.data || props.data.length === 0) return 1
  return Math.max(...props.data.map(item => item[props.valueKey]))
})
</script>

<style scoped>
.chart-wrapper {
  display: flex;
  flex-direction: column;
  gap: 10px;
  width: 100%;
}

.bar-row {
  display: grid;
  grid-template-columns: 140px 1fr 40px;
  align-items: center;
  gap: 12px;
}

.bar-label {
  font-family: 'DM Mono', monospace;
  font-size: 11px;
  color: #888;
  text-align: right;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.bar-track {
  height: 8px;
  background: #222;
  border-radius: 0;
  overflow: hidden;
}

.bar-fill {
  height: 100%;
  transition: width 0.8s cubic-bezier(0.4, 0, 0.2, 1);
  border-radius: 0;
  min-width: 4px;
}

.bar-value {
  font-family: 'DM Mono', monospace;
  font-size: 11px;
  color: #444;
  text-align: left;
}
</style>