<template>
  <div class="kpi-card">
    <div class="kpi-label">{{ label }}</div>
    <div class="kpi-value">{{ formattedValue }}</div>
    <div class="kpi-unit">{{ unit }}</div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  label: String,
  value: [Number, String],
  unit: String
})

const formattedValue = computed(() => {
  if (typeof props.value === 'number') {
    return props.value.toLocaleString('fr-FR')
  }
  return props.value
})
</script>

<style scoped>
.kpi-card {
  background: #0f0f0f;
  padding: 28px 24px;
  border-right: 1px solid #1a1a1a;
}

.kpi-card:last-child {
  border-right: none;
}

.kpi-label {
  font-family: 'DM Mono', monospace;
  font-size: 10px;
  letter-spacing: 2px;
  color: #444;
  text-transform: uppercase;
  margin-bottom: 12px;
}

.kpi-value {
  font-size: 40px;
  font-weight: 600;
  color: #e8e8e8;
  letter-spacing: -1px;
  line-height: 1;
  margin-bottom: 8px;
}

.kpi-unit {
  font-size: 13px;
  color: #444;
  font-weight: 300;
}
</style>