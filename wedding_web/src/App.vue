<script setup lang="ts">
  import Hero from './views/partials/hero.vue';
  import TextData from '@/views/partials/text-data.vue'
  import Place from '@/views/partials/place.vue'
  import PlanDay from '@/views/partials/plan-day.vue'
  import DressCode from '@/views/partials/dress-code.vue'
  import Form from '@/views/partials/form.vue'
  import Time from '@/views/partials/time.vue'
  import Footer from '@/views/partials/footer.vue'
</script>

<template>
  <section class="main container">
    <Hero/>
    <TextData/>
    <Place/>
    <PlanDay/>
    <DressCode/>
    <Form/>
    <Time/>
    <Footer/>
  </section>



</template>

<style scoped>
</style>
