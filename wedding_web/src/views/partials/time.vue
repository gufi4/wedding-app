<script setup lang="ts">
import { computed } from 'vue'
import { WEDDING_DATE } from '@/stores/wedding-config'
import { useCountdown } from '@/composables/useCountdown'
import { pluralize } from '@/utils/pluralization'

const { countdown } = useCountdown(WEDDING_DATE)

// Computed properties for pluralized labels
const monthLabel = computed(() =>
  pluralize(countdown.value.months, ['месяц', 'месяца', 'месяцев'])
)

const dayLabel = computed(() =>
  pluralize(countdown.value.days, ['день', 'дня', 'дней'])
)

const hourLabel = computed(() =>
  pluralize(countdown.value.hours, ['час', 'часа', 'часов'])
)

const minuteLabel = computed(() =>
  pluralize(countdown.value.minutes, ['минута', 'минуты', 'минут'])
)

const titleText = computed(() =>
  countdown.value.isComplete
    ? 'Мы уже семья!'
    : 'Мы станем семьей через:'
)
</script>

<template>
  <section class="time section">
    <div class="time__title">
      <p>{{ titleText }}</p>
    </div>

    <div class="time__content">
      <div class="time__item">
        <div class="time-item__circle">
          {{ countdown.months }}
        </div>
        <div class="time-item__text">
          {{ monthLabel }}
        </div>
      </div>

      <div class="time__item">
        <div class="time-item__circle">
          {{ countdown.days }}
        </div>
        <div class="time-item__text">
          {{ dayLabel }}
        </div>
      </div>

      <div class="time__item">
        <div class="time-item__circle">
          {{ countdown.hours }}
        </div>
        <div class="time-item__text">
          {{ hourLabel }}
        </div>
      </div>

      <div class="time__item">
        <div class="time-item__circle">
          {{ countdown.minutes }}
        </div>
        <div class="time-item__text">
          {{ minuteLabel }}
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped lang="scss">
@use "../../styles/helpers/media";
@use "../../styles/helpers/functions";

.time {
  display: flex;
  flex-direction: column;
  gap: 20px;
  align-items: center;
}

.time__title {
  color: var(--c-primary);
  font-size: functions.rfs(28, 40);
  letter-spacing: -2px;
}

.time__content {
  display: flex;
  gap: 20px;
}

.time__item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 5px;
}

.time-item__circle {
  border: 1px solid var(--c-primary);
  border-radius: 50%;
  padding: 15px;
  font-size: functions.rfs(24, 32);
  width: 60px;
  height: 60px;
  text-align: center;
}

.time-item__text {
  text-align: center;
  font-size: functions.rfs(12, 16);
}
</style>
