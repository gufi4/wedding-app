<script setup lang="ts">
interface Props {
  icon: string;
  time?: string;
  title: string;
  desc?: string;
  isLast?: boolean;
}

const props = defineProps<Props>()
</script>

<template>
  <div class="plan-item" :class="{ 'plan-item--last': props.isLast }">
    <div class="plan-item__icon">
      <img class="plan-item__img" :src=props.icon alt="Иконка {{ props.title }}">
    </div>
    <div class="plan-item__line-wrap">
      <div class="plan-item__line"></div>
      <div class="plan-item__heart"><img src="../../assets/icon-heart.svg" alt="Иконка сердца"></div>
    </div>
    <div class="plan-item__content">
      <div class="plan-item__heading">
        <p class="plan-item__time">
          {{ props.time }}
        </p>
        <p class="plan-item__title">
          {{ props.title}}
        </p>
      </div>
      <div class="plan-item__desc">
        {{ props.desc }}
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
@use "../../styles/helpers/media";
@use "../../styles/helpers/functions";

.plan-item__img {
  padding-top: 10px;
  width: 30px;

  @include media.lg-up {
    width: 45px;
  }

  @include media.xl-up {
    padding-top: 15px;
  }
}

.plan-item__line-wrap {
  position: relative;
  height: 100%;
  display: flex;
  justify-content: center;
}

.plan-item__line {
  position: absolute;
  top: -32px;
  bottom: -34px;
  width: 2px;
  background: #999;
}

.plan-item__heart {
  position: relative;
  background: white;
  padding: 10px 0;
  z-index: 2;
  color: red;
}

.plan-item {
  display: flex;
  align-items: center;
  gap: 10px;
  width: 100%;
}

.plan-item__icon {
  margin-right: 10px;
  font-size: functions.rfs(50, 70);
}

.plan-item__content {
  display: flex;
  flex-direction: column;
  gap: 5px;
  margin-left: 5px;
  flex: 1;
}

.plan-item__heading {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 20px;

  @include media.lg-up {
    gap: 60px;
  }
}

.plan-item__time {
  position: relative;
  top: 10px;
  font-weight: 600;
  font-size: functions.rfs(20, 26);
  line-height: 1;

  @include media.lg-up {
    top: 15px;
  }
}

.plan-item__title {
  display: flex;
  justify-content: center;
  text-align: center;
  font-weight: 600;
  font-size: functions.rfs(20, 26);
  line-height: 1;
  width: 100%;
}

.plan-item__desc {
  font-size: functions.rfs(14, 20);
  color: var(--c-grey-70);
  text-align: right;
}

.plan-item--last {
  .plan-item__time {
    top: 2px;
  }
}
</style>
