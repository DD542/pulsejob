<template>
  <div class="donut-wrapper">
    <svg :width="size" :height="size" :viewBox="`0 0 ${size} ${size}`">
      <g :transform="`translate(${size/2}, ${size/2})`">
        <circle :r="innerRadius" fill="#0f0f0f" />
        <path
          v-for="(slice, index) in slices"
          :key="index"
          :d="slice.path"
          fill="none"
          :stroke="colors[index % colors.length]"
          :stroke-width="strokeWidth"
          stroke-linecap="butt"
          class="slice"
          @mouseenter="hoveredIndex = index"
          @mouseleave="hoveredIndex = null"
        />
        <text
          v-if="hoveredIndex !== null"
          text-anchor="middle"
          dominant-baseline="middle"
          class="center-text"
          y="-8"
        >{{ getPercent(contrats[hoveredIndex]?.[valueKey]) }}%</text>
        <text
          v-if="hoveredIndex !== null"
          text-anchor="middle"
          dominant-baseline="middle"
          class="center-label"
          y="10"
        >{{ contrats[hoveredIndex]?.[labelKey] }}</text>
      </g>
    </svg>

    <div class="legend">
      <div
        v-for="(item, index) in data"
        :key="index"
        class="legend-item"
        :class="{ active: hoveredIndex === index }"
        @mouseenter="hoveredIndex = index"
        @mouseleave="hoveredIndex = null"
      >
        <div class="legend-bar" :style="{ background: colors[index % colors.length] }"></div>
        <div class="legend-info">
          <span class="legend-label">{{ item[labelKey] }}</span>
          <span class="legend-value">{{ getPercent(item[valueKey]) }}%</span>
        </div>
        <span class="legend-count">{{ item[valueKey] }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'

const props = defineProps({
  data: Array,
  labelKey: String,
  valueKey: String,
  size: { type: Number, default: 200 }
})

const hoveredIndex = ref(null)
const contrats = computed(() => props.data || [])

const outerRadius = computed(() => props.size / 2 - 8)
const innerRadius = computed(() => outerRadius.value * 0.58)
const strokeWidth = computed(() => outerRadius.value - innerRadius.value)

const colors = ['#ffffff', '#7ec87a', '#e8b86d', '#6ab0e8', '#e87a7a', '#aaa']

const total = computed(() => {
  if (!props.data) return 0
  return props.data.reduce((sum, item) => sum + item[props.valueKey], 0)
})

const getPercent = (value) => {
  if (!value || !total.value) return '0.0'
  return ((value / total.value) * 100).toFixed(1)
}

const slices = computed(() => {
  if (!props.data) return []
  let currentAngle = -Math.PI / 2
  return props.data.map(item => {
    const angle = (item[props.valueKey] / total.value) * 2 * Math.PI
    const gap = 0.03
    const startAngle = currentAngle + gap / 2
    const endAngle = currentAngle + angle - gap / 2
    currentAngle = currentAngle + angle

    const r = (outerRadius.value + innerRadius.value) / 2
    const x1 = r * Math.cos(startAngle)
    const y1 = r * Math.sin(startAngle)
    const x2 = r * Math.cos(endAngle)
    const y2 = r * Math.sin(endAngle)
    const largeArc = angle > Math.PI ? 1 : 0

    return {
      path: `M ${x1} ${y1} A ${r} ${r} 0 ${largeArc} 1 ${x2} ${y2}`
    }
  })
})
</script>

<style scoped>
.donut-wrapper {
  display: flex;
  align-items: center;
  gap: 40px;
}

.slice {
  transition: opacity 0.2s, stroke-width 0.2s;
  cursor: pointer;
}

.slice:hover {
  opacity: 0.85;
}

.center-text {
  font-family: 'DM Sans', sans-serif;
  font-size: 18px;
  font-weight: 600;
  fill: #e8e8e8;
}

.center-label {
  font-family: 'DM Mono', monospace;
  font-size: 9px;
  fill: #555;
  letter-spacing: 1px;
  text-transform: uppercase;
}

.legend {
  display: flex;
  flex-direction: column;
  gap: 12px;
  flex: 1;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
  opacity: 0.5;
  transition: opacity 0.2s;
}

.legend-item:hover,
.legend-item.active {
  opacity: 1;
}

.legend-bar {
  width: 3px;
  height: 28px;
  flex-shrink: 0;
  border-radius: 0;
}

.legend-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
  flex: 1;
}

.legend-label {
  font-family: 'DM Mono', monospace;
  font-size: 11px;
  color: #888;
  letter-spacing: 1px;
}

.legend-value {
  font-family: 'DM Mono', monospace;
  font-size: 14px;
  color: #e8e8e8;
  font-weight: 500;
}

.legend-count {
  font-family: 'DM Mono', monospace;
  font-size: 10px;
  color: #333;
}
</style>