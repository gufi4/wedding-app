<script setup lang="ts">
import Data from '@/views/components/data.vue'
</script>

<template>
  <section class="text-data section">
    <div class="text-data__heading">
      <div class="text-data__title">
        Дорогие гости!
      </div>
      <div class="text-data__subtitle">
        Дорогие гости!
      </div>
    </div>

    <div class="text-data__text container container--text">
      <p>Совсем скоро в нашей жизни произойдет очень важное событие — <strong>наша свадьба!</strong></p>
        <p>Мы верим и надеемся что этот день станет красивым началом долгой и счастливой жизни!
      </p>
      <p>Приглашаем Вас разделить с нами радость этого дня.</p>
    </div>

    <div class="text-data__data">
      <p>Апрель, 2026</p>
      <Data/>
    </div>
  </section>
</template>

<style scoped lang="scss">
@use "../../styles/helpers/media";
@use "../../styles/helpers/functions";

.text-data {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.text-data__heading {
  position: relative;
  height: 120px;
}

.text-data__title {
  position: relative;
  color: var(--c-primary);
  font-family: var(--f-base);
  font-size: functions.rfs(40, 70);
  z-index: var(--z-bottom);
  text-transform: uppercase;
}

.text-data__subtitle {
  color: var(--c-secondary);
  font-family: var(--f-headings);
  font-size: functions.rfs(70, 120);
  position: absolute;
  top: 4px;
  z-index: 1;
}

.text-data__text {
  margin-top: -15px;
  padding: 0 10px;
  text-align: center;
  display: flex;
  flex-direction: column;
  gap: 10px;
  font-size: functions.rfs(18,26);

  @include media.md-up {
    margin-top: 20px;
  }

  @include media.xl-up {
    margin-top: 55px;
  }

  p {
    strong {
      color: var(--c-primary);
    }
  }
}

.text-data__data {
  padding-top: 20px;
  text-align: center;

  p {
    color: var(--c-primary);
    font-family: var(--f-headings);
    font-size: functions.rfs(70, 70);
  }
}
</style>
