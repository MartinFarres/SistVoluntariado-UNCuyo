<template>
  <div class="card card-stats mb-4 mb-xl-0">
    <div class="card-body">
      <div class="row">
        <div class="col">
          <h5 class="card-title text-uppercase text-muted mb-0">{{ title }}</h5>
          <span class="h2 font-weight-bold mb-0">{{ value }}</span>
        </div>
        <div class="col-auto">
          <div class="icon icon-shape text-white rounded-circle shadow" :class="iconColor">
            <i class="bi" :class="icon"></i>
          </div>
        </div>
      </div>
      <p class="mt-3 mb-0 text-muted text-sm">
        <span class="me-2" :class="percentageColor">
          <i class="bi" :class="percentage.startsWith('+') ? 'bi-arrow-up' : 'bi-arrow-down'"></i>
          {{ percentage }}
        </span>
        <span class="text-nowrap">{{ description }}</span>
      </p>
    </div>
  </div>
</template>

<script lang="ts">
export default {
  name: 'StatsCard',
  props: {
    title: {
      type: String,
      required: true
    },
    value: {
      type: [String, Number],
      required: true
    },
    icon: {
      type: String,
      required: true
    },
    iconColor: {
      type: String,
      default: 'bg-primary'
    },
    percentage: {
      type: String,
      default: '0%'
    },
    percentageColor: {
      type: String,
      default: 'text-success'
    },
    description: {
      type: String,
      default: ''
    }
  }
}
</script>

<style scoped>
.card-stats {
  border: 0;
  box-shadow: 0 0 2rem 0 rgba(136, 152, 170, 0.15);
}

.card-stats .card-body {
  padding: 1.5rem;
}

.card-title {
  font-size: 0.625rem;
  font-weight: 600;
  letter-spacing: 0.04em;
  color: #8898aa;
}

.icon-shape {
  width: 48px;
  height: 48px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-size: 1.25rem;
}

.text-sm {
  font-size: 0.875rem;
}

.bg-danger {
  background: linear-gradient(87deg, #f5365c 0, #f56036 100%);
}

.bg-warning {
  background: linear-gradient(87deg, #fb6340 0, #fbb140 100%);
}

.bg-info {
  background: linear-gradient(87deg, #11cdef 0, #1171ef 100%);
}

.bg-success {
  background: linear-gradient(87deg, #2dce89 0, #2dcecc 100%);
}
</style>