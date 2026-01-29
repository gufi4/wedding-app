<script setup lang="ts">
</script>

<template>
  <section class="footer section">
    <div class="footer__title">
      Контакты
    </div>
    <div class="footer__subtitle container container--text">
      <p>Герман — <a href="tel:89375673390">+7 (937) 567-33-90</a></p>
      <p>Адресс: <a href="https://yandex.ru/maps/-/CLhcrNPK" target="_blank">улица Межколхозстроя, 13, станица Кумылженская</a></p>
      <br/>
      <p>Анна — <a href="tel:89044280710">+7 (904) 428-07-10</a></p>
      <p>Адресс: <a href="https://yandex.ru/maps/-/CLhcnXMe" target="_blank">улица Шолохова, 16, станица Кумылженская</a></p>
    </div>

    <div class="footer__title section">
      До скорой встречи <img class="footer__title--icon" src="../../assets/icon-heart.svg">
    </div>
  </section>
</template>

<style scoped lang="scss">
@use "../../styles/helpers/media";
@use "../../styles/helpers/functions";

.footer {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 10px;
}

.footer__subtitle {
  display: flex;
  flex-direction: column;
  justify-content: center;
  text-align: center;
  gap: 5px;
  font-size: functions.rfs(16, 22);

  p {
    a {
      color: var(--c-grey-70);
    }
  }
}

.footer__title {
  font-size: functions.rfs(40, 66);
  text-transform: uppercase;
  color: var(--c-primary);
}

.footer__title--icon {
  padding-top: 8px;
  width: 30px;

  @include media.xl-up {
    width: 40px;
    padding-top: 20px;
  }
}
</style>
