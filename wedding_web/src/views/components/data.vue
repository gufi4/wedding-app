<script setup lang="ts">
</script>

<template>
  <div class="data container container--md-up">
    <div class="data__item">
      23
    </div>
    <div class="data__item">
      24
    </div>
    <div class="data__item data__item--active">
      25
    </div>
    <div class="data__item">
      26
    </div>
    <div class="data__item">
      27
    </div>
  </div>
</template>

<style scoped lang="scss">
@use "../../styles/helpers/media";
@use "../../styles/helpers/functions";

.data {
  padding-top: 40px;
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  position: relative;
  width: 100vw;

  &::before {
    content: '';
    position: absolute;
    top: -10px;
    left: -90px;
    right: -90px;
    bottom: -90px;
    background-image: url("../../assets/heart.svg");
    background-size: 100% 100%;
    background-repeat: no-repeat;
    background-position: center;
    pointer-events: none;
  }
}

.data__item {
  font-size: functions.rfs(25, 40);
  border-radius: 10px;
  padding: 10px;

  &--active {
    position: relative;
    border: none;
  }
}

</style>
