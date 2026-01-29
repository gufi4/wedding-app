<script setup lang="ts">
import { ref } from 'vue'

const formData = ref({
  name: '',
  guest_count: '',
  comment: ''
})

const isSubmitting = ref(false)
const submitStatus = ref<{ type: 'success' | 'error', message: string } | null>(null)

async function submitForm() {
  submitStatus.value = null

  // Валидация
  if (!formData.value.name.trim()) {
    submitStatus.value = { type: 'error', message: 'Пожалуйста, укажите имя и фамилию' }
    return
  }

  const guestCount = Number(formData.value.guest_count)
  if (!formData.value.guest_count || isNaN(guestCount) || guestCount <= 0) {
    submitStatus.value = { type: 'error', message: 'Пожалуйста, укажите корректное количество гостей' }
    return
  }

  isSubmitting.value = true

  try {
    const guestData = {
      name: formData.value.name.trim(),
      guest_count: guestCount,
      comment: formData.value.comment.trim()
    }

    const response = await fetch(`${import.meta.env.VITE_API_URL}/api/v1/guests/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(guestData)
    })

    const result = await response.json()

    if (result.success) {
      submitStatus.value = { type: 'success', message: 'Спасибо! Ждем Вас на нашей свадьбе!' }
      // Очистить форму
      formData.value = { name: '', guest_count: '', comment: '' }
    } else {
      submitStatus.value = { type: 'error', message: 'Ошибка в отправке. Попробуйте позже' }
    }
  } catch {
    submitStatus.value = { type: 'error', message: 'Ошибка в отправке. Попробуйте позже' }
  } finally {
    isSubmitting.value = false
  }
}
</script>

<template>
  <section class="presence-form section container container--text">
    <div class="presence-form__title">
      Присутствие
    </div>

    <div class="presence-form__text">
      <p>Пожалуйста, подтвердите ваше присутствие на нашем празднике до 1 апреля 2026 года
        любым удобным для вас способом или заполните форму ниже:
      </p>
    </div>

    <form class="presence-form__form" @submit.prevent="submitForm">
      <input
        v-model="formData.name"
        name="name"
        type="text"
        class="presence-form__input"
        placeholder="Имя и фамилия"
      >

      <input
        v-model="formData.guest_count"
        name="guest_count"
        type="number"
        class="presence-form__input"
        placeholder="Кол-во персон"
      >

      <textarea
        v-model="formData.comment"
        name="comment"
        class="presence-form__textarea"
        placeholder="Оставь свой комментарий"
      >
      </textarea>

      <p class="presence-form__text">Если еще остались вопросы напишите их в наш
        <a href="https://t.me/weddingGA2026_bot" target="_blank">телеграмм</a>
      </p>

      <div v-if="submitStatus" class="presence-form__status" :class="`presence-form__status--${submitStatus.type}`">
        {{ submitStatus.message }}
      </div>

      <button class="presence-form__btn-submit" type="submit" :disabled="isSubmitting">
        {{ isSubmitting ? 'Отправка...' : 'Отправить' }}
      </button>
    </form>

  </section>
</template>

<style scoped lang="scss">
@use "../../styles/helpers/media";
@use "../../styles/helpers/functions";

.presence-form {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
}

.presence-form__title {
  color: var(--c-primary);
  font-size: functions.rfs(40, 70);
  text-transform: uppercase;
}

.presence-form__text {
  padding-inline: 20px;
  text-align: center;
  font-size: functions.rfs(16, 24);

  a {
    color: var(--c-primary);
    font-weight: 600;
  }
}

.presence-form__form {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding-inline: 15px;
  gap: 15px;
}

.presence-form__input {
  border: 1px solid var(--c-primary);
  border-radius: var(--b-radius-sm);
  padding: 5px 15px;
}

.presence-form__textarea {
  width: 100%;
  height: 100px;
  border: 1px solid var(--c-primary);
  border-radius: var(--b-radius-sm);
  padding: 8px;
}

.presence-form__btn-submit {
  background: none;
  border: 2px solid var(--c-primary);
  border-radius: var(--b-radius-sm);
  width: max-content;
  font-size: functions.rfs(20, 30);
  text-transform: uppercase;
  color: var(--c-primary);
  padding: 10px 60px;
  cursor: pointer;
  transition: opacity 0.2s;

  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
}

.presence-form__status {
  padding: 10px 15px;
  border-radius: var(--b-radius-sm);
  text-align: center;

  &--success {
    background: #d4edda;
    color: #155724;
  }

  &--error {
    background: #f8d7da;
    color: #721c24;
  }
}

</style>
