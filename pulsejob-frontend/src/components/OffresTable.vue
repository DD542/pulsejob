<template>
  <div class="table-wrapper">
    <div class="search-bar">
      <input
        v-model="recherche"
        type="text"
        placeholder="Filtrer par titre, entreprise, ville..."
        class="search-input"
      />
    </div>

    <div class="table-container">
      <table class="table">
        <thead>
          <tr>
            <th>Titre</th>
            <th>Entreprise</th>
            <th>Localisation</th>
            <th>Contrat</th>
            <th>Expérience</th>
            <th>Publication</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="(offre, index) in offresFiltrees"
            :key="index"
            class="table-row"
          >
            <td class="td-title">{{ offre.titre }}</td>
            <td>{{ offre.entreprise }}</td>
            <td>{{ offre.localisation }}</td>
            <td>
              <span class="badge" :class="getBadgeClass(offre.type_contrat)">
                {{ offre.type_contrat }}
              </span>
            </td>
            <td>{{ offre.experience }}</td>
            <td class="td-date">{{ formatDate(offre.date_publication) }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="table-footer">
      {{ offresFiltrees.length }} offres affichées
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  offres: Array
})

const recherche = ref('')

const offresFiltrees = computed(() => {
  if (!props.offres) return []
  if (!recherche.value) return props.offres
  const q = recherche.value.toLowerCase()
  return props.offres.filter(o =>
    Object.values(o).some(v => String(v).toLowerCase().includes(q))
  )
})

const formatDate = (date) => {
  if (!date) return ''
  return new Date(date).toLocaleDateString('fr-FR', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric'
  })
}

const getBadgeClass = (type) => {
  const map = {
    'CDI': 'badge-cdi',
    'CDD': 'badge-cdd',
    'MIS': 'badge-mis',
    'LIB': 'badge-lib'
  }
  return map[type] || 'badge-default'
}
</script>

<style scoped>
.table-wrapper {
  width: 100%;
}

.search-bar {
  margin-bottom: 16px;
}

.search-input {
  width: 100%;
  background: #141414;
  border: 1px solid #1a1a1a;
  color: #e8e8e8;
  padding: 12px 16px;
  font-family: 'DM Mono', monospace;
  font-size: 12px;
  outline: none;
  transition: border-color 0.2s;
}

.search-input::placeholder {
  color: #333;
}

.search-input:focus {
  border-color: #333;
}

.table-container {
  overflow-x: auto;
  border: 1px solid #1a1a1a;
}

.table {
  width: 100%;
  border-collapse: collapse;
}

thead tr {
  border-bottom: 1px solid #1a1a1a;
}

th {
  font-family: 'DM Mono', monospace;
  font-size: 10px;
  letter-spacing: 2px;
  color: #444;
  text-transform: uppercase;
  padding: 14px 16px;
  text-align: left;
  font-weight: 400;
  white-space: nowrap;
}

.table-row {
  border-bottom: 1px solid #141414;
  transition: background 0.15s;
}

.table-row:hover {
  background: #141414;
}

.table-row:last-child {
  border-bottom: none;
}

td {
  padding: 14px 16px;
  font-size: 13px;
  color: #888;
  vertical-align: middle;
}

.td-title {
  color: #e8e8e8;
  font-weight: 400;
  max-width: 300px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.td-date {
  font-family: 'DM Mono', monospace;
  font-size: 11px;
  white-space: nowrap;
}

.badge {
  font-family: 'DM Mono', monospace;
  font-size: 10px;
  letter-spacing: 1px;
  padding: 3px 8px;
  border: 1px solid;
}

.badge-cdi { color: #a8c4a2; border-color: #a8c4a2; }
.badge-cdd { color: #c8b89a; border-color: #c8b89a; }
.badge-mis { color: #888; border-color: #333; }
.badge-lib { color: #666; border-color: #222; }
.badge-default { color: #555; border-color: #222; }

.table-footer {
  margin-top: 12px;
  font-family: 'DM Mono', monospace;
  font-size: 11px;
  color: #333;
  text-align: right;
}
</style>