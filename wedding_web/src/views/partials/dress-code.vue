<script setup lang="ts">
  import { dressCodeColors } from '@/stores/dress-code.ts'
</script>

<template>
  <section class="dress-code section container container--text">
    <div class="dress-code__title">
      Дресс-код
    </div>

    <div class="dress-code__text">
      <p>Пожалуйста, приходите в красивой одежде, которая соответствует торжественному настроению.</p>
      <p>Мы будем рады, если вы поддержите цветовую палитру нашей свадьбы:</p>
    </div>

    <div class="dress-code__list container container--md-up">
      <div v-for="(color, index) in dressCodeColors"
           :key="index"
           class="dress-code__item"
           :style="{ backgroundColor: color.color }"
      >
      </div>
    </div>

    <div class="dress-code__list dress-code__list--addition container container--md-up">
      <div class="dress-code__item--addition">
        <div class="dress-code__item">
          <img src="../../assets/silver.png">
        </div>

        <p>серебро</p>
      </div>

      <div class="dress-code__item--addition">
        <div class="dress-code__item">
          <img src="../../assets/gold.jpg">
        </div>

        <p>золото</p>
      </div>

    </div>
  </section>
</template>

<style scoped lang="scss">
@use "../../styles/helpers/media";
@use "../../styles/helpers/functions";

.dress-code {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
}

.dress-code__title {
  color: var(--c-primary);
  font-size: functions.rfs(40, 70);
  text-transform: uppercase;
}

.dress-code__text {
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  font-size: functions.rfs(16,24);

  p:nth-child(2) {
    width: 80%;
  }
}

.dress-code__list {
  display: flex;
  gap: 10px;

  &--addition {
    width: 100%;
    justify-content: space-evenly;
  }
}

.dress-code__item {
  border: 1px solid var(--c-secondary);
  width: 50px;
  height: 50px;
  border-radius: 50%;
  overflow: hidden;
}

.dress-code__item--addition {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 5px;
}
</style>
