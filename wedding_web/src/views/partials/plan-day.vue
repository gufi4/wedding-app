<script setup lang="ts">
import PlanItem from '@/views/components/plan-item.vue'
import { planItems } from '@/stores/data-plan-day.ts'
</script>

<template>
  <section class="plan-day section">
    <p class="h1">План дня</p>
    <div class="plan-day__list">
      <PlanItem v-for="(item, index) in planItems"
                :key="index"
                :icon="item.icon"
                :title="item.title"
                :time="item.time"
                :desc="item.desc"
                :isLast="index === planItems.length - 1"
      />
    </div>
  </section>
</template>

<style scoped lang="scss">
@use "../../styles/helpers/media";
@use "../../styles/helpers/functions";

.plan-day {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 30px;
}

.plan-day__list {
  margin-top: 20px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}
</style>
