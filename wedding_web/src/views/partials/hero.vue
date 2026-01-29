<template>
  <div class="hero">
    <div class="hero__data">
      <span>25</span>
      <span>04</span>
      <span>26</span>
    </div>

    <div class="hero__text">
      <span>Герман</span>
      <span>+</span>
      <span>Анна</span>
    </div>
  </div>
</template>

<script setup lang="ts">

</script>

<style scoped lang="scss">
@use "../../styles/helpers/media";
@use "../../styles/helpers/functions";

.hero {
  background-image: url("../../assets/bg-hero1.jpg") ;
  background-repeat: no-repeat;
  background-position: left;
  background-size: cover;
  height: 100vh;
  width: 100%;
  display: flex;
  flex-direction: row;
  gap: 40px;
  overflow: hidden;

  @include media.md-up {
    height: 70vh;
    gap: 320px;
  }

  @include media.xl-up {
    height: 100vh;
  }
}

.hero__data {
  margin-left: -30px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  margin-top: -20px;

  @include media.xl-up {
    margin-left: -40px;
    margin-top: -40px;
  }

  span {
    font-size: functions.rfs(220, 320);
    line-height: 1;
    font-weight: 100;
    font-family: var(--f-barlowCondensed);
    color: var(--c-white);
  }
}

.hero__text {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: center;
  align-self: flex-end;
  margin-bottom: 40px;

  span {
    font-size: functions.rfs(76, 120);
    line-height: 0.8;
    font-family: var(--f-headings);
    color: var(--c-white);

    @include media.lg-up {
      font-size: functions.rfs(76, 150);
    }

    @include media.xl-up {
      font-size: functions.rfs(76, 120);
    }
  }
}
</style>
