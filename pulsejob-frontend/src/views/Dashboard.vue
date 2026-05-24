<template>
  <div class="dashboard">

    <!-- Header -->
    <header class="header">
      <div class="header-inner">
        <div class="header-label">France Travail API — Données temps réel</div>
        <h1 class="header-title">PulseJob</h1>
        <p class="header-sub">Observatoire du marché Data & Intelligence Artificielle en France</p>
      </div>
    </header>

    <!-- Loading -->
    <div v-if="loading" class="loading">
      <div class="loading-text">Chargement des données...</div>
    </div>

    <div v-else class="container">

      <!-- KPIs -->
      <div class="kpi-grid">
        <KpiCard label="Offres analysées" :value="stats.total_offres" unit="offres collectées" />
        <KpiCard label="Villes couvertes" :value="stats.total_villes" unit="zones géographiques" />
        <KpiCard label="Entreprises" :value="stats.total_entreprises" unit="recruteurs identifiés" />
        <KpiCard label="Compétences" :value="competences.length" unit="technologies détectées" />
      </div>

      <!-- Ligne 1 -->
      <div class="grid-2">
        <div class="card">
          <SectionTitle title="Compétences les plus demandées" />
          <BarChart
            :data="competences"
            labelKey="competence"
            valueKey="occurences"
            color="linear-gradient(90deg, #2a2a2a, #ffffff)"
          />
        </div>
        <div class="card">
          <SectionTitle title="Concentration géographique" />
          <BarChart
            :data="villes"
            labelKey="ville"
            valueKey="nombre_offres"
            color="linear-gradient(90deg, #3a2a1a, #e8b86d)"
          />
        </div>
      </div>

      <div class="divider"></div>

      <!-- Ligne 2 -->
      <div class="grid-2">
        <div class="card">
          <SectionTitle title="Top recruteurs" />
          <BarChart
            :data="entreprises"
            labelKey="entreprise"
            valueKey="nombre_offres"
            color="linear-gradient(90deg, #1a2a1a, #7ec87a)"
          />
        </div>
        <div class="card">
          <SectionTitle title="Types de contrats" />
          <DonutChart
            :data="contrats"
            labelKey="type_contrat"
            valueKey="nombre"
            :size="220"
          />
        </div>
      </div>

      <div class="divider"></div>

      <!-- Table -->
      <div class="card">
        <SectionTitle title="Explorer les offres" />
        <OffresTable :offres="offres" />
      </div>

      <!-- Footer -->
      <footer class="footer">
        <span>PulseJob — Dylan Menga Wanda — ECE Paris B3 Data & IA</span>
        <span>{{ stats.total_offres }} offres — Source France Travail API</span>
      </footer>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import KpiCard from '../components/KpiCard.vue'
import SectionTitle from '../components/SectionTitle.vue'
import BarChart from '../components/BarChart.vue'
import DonutChart from '../components/DonutChart.vue'
import OffresTable from '../components/OffresTable.vue'

const API = 'http://localhost:5001'

const loading = ref(true)
const stats = ref({})
const competences = ref([])
const villes = ref([])
const entreprises = ref([])
const contrats = ref([])
const offres = ref([])

onMounted(async () => {
  try {
    const [s, c, v, e, co, o] = await Promise.all([
      axios.get(`${API}/api/stats`),
      axios.get(`${API}/api/competences`),
      axios.get(`${API}/api/villes`),
      axios.get(`${API}/api/entreprises`),
      axios.get(`${API}/api/contrats`),
      axios.get(`${API}/api/offres`)
    ])
    stats.value = s.data
    competences.value = c.data
    villes.value = v.data
    entreprises.value = e.data
    contrats.value = co.data
    offres.value = o.data
  } catch (err) {
    console.error('Erreur chargement API', err)
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.dashboard {
  min-height: 100vh;
  background: #0f0f0f;
}

.container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 40px;
}

.header {
  border-bottom: 1px solid #1a1a1a;
  margin-bottom: 40px;
}

.header-inner {
  max-width: 1400px;
  margin: 0 auto;
  padding: 48px 40px 32px;
}

.header-label {
  font-family: 'DM Mono', monospace;
  font-size: 11px;
  letter-spacing: 3px;
  color: #555;
  text-transform: uppercase;
  margin-bottom: 12px;
}

.header-title {
  font-size: 36px;
  font-weight: 600;
  color: #f0f0f0;
  letter-spacing: -0.5px;
  margin-bottom: 8px;
}

.header-sub {
  font-size: 14px;
  color: #555;
  font-weight: 300;
}

.loading {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 60vh;
}

.loading-text {
  font-family: 'DM Mono', monospace;
  font-size: 12px;
  color: #333;
  letter-spacing: 2px;
}

.kpi-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  border: 1px solid #1a1a1a;
  margin-bottom: 40px;
}

.grid-2 {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1px;
  background: #1a1a1a;
  margin-bottom: 1px;
}

.card {
  background: #0f0f0f;
  padding: 32px;
}

.divider {
  height: 1px;
  background: #1a1a1a;
  margin: 40px 0;
}

.footer {
  margin-top: 60px;
  padding: 24px 0 40px;
  border-top: 1px solid #1a1a1a;
  font-family: 'DM Mono', monospace;
  font-size: 11px;
  color: #333;
  display: flex;
  justify-content: space-between;
}

@media (max-width: 1024px) {
  .kpi-grid { grid-template-columns: repeat(2, 1fr); }
  .grid-2 { grid-template-columns: 1fr; }
  .container { padding: 0 20px; }
  .header-inner { padding: 32px 20px 24px; }
}

@media (max-width: 640px) {
  .kpi-grid { grid-template-columns: 1fr 1fr; }
  .header-title { font-size: 28px; }
  .card { padding: 20px; }
}
</style>