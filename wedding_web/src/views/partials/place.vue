<script setup lang="ts">
const openMap = () => {
  window.open('https://yandex.ru/maps/-/CLhaZHYd', '_blank');
}
</script>

<template>
  <section class="place">
    <div class="h1">
      Место
    </div>

    <div class="place__description">
      <p>Кафе "Аксинья"</p>
      <p class="place__description--address">ул. Гагарина, 32Д, станица Кумылженская</p>
    </div>

    <button class="place__btn" @click="openMap">Открыть карту</button>
  </section>
</template>

<style scoped lang="scss">
@use "../../styles/helpers/media";
@use "../../styles/helpers/functions";

.place {
  padding-top: 60px;
  display: flex;
  flex-direction: column;
  gap: 20px;
  align-items: center;
}

.place__description {
  text-align: center;
  font-size: functions.rfs(20, 26);

  &--address {
    margin-top: 10px;
    padding-inline: 10px;
    font-size: functions.rfs(16, 24);
  }
}

.place__btn {
  margin-top: 5px;
  text-transform: lowercase;
  width: max-content;
  background: none;
  border: 1px solid var(--c-black);
  border-radius: var(--b-radius-lg);
  padding: 10px 20px;
  color: var(--c-black);
}

</style>
