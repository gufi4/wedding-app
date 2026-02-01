<script setup lang="ts">
import { ref, onMounted } from 'vue'

const formData = ref({
  name: '',
  guest_count: '',
  comment: ''
})

const isSubmitting = ref(false)
const submitStatus = ref<{ type: 'success' | 'error', message: string } | null>(null)
const hasSubmitted = ref(false)
const submittedData = ref<{ name: string; guest_count: number } | null>(null)

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
    // Обрезаем имя до первых 2 слов (имя + фамилия)
    const nameParts = formData.value.name.trim().split(/\s+/)
    const shortName = nameParts.slice(0, 2).join(' ')

    const guestData = {
      name: shortName,
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
      // Сохранить в localStorage сразу (чтобы не потерять данные)
      localStorage.setItem('wedding-form-submitted', JSON.stringify({
        name: guestData.name,
        guest_count: guestData.guest_count
      }))

      // Сразу сохраняем данные для отображения после задержки
      submittedData.value = { name: guestData.name, guest_count: guestData.guest_count }

      submitStatus.value = { type: 'success', message: 'Спасибо! Переходите в наш телеграмм бот, чтобы ничего не пропустить! Ждем Вас на нашей свадьбе!' }
      // Очистить форму
      formData.value = { name: '', guest_count: '', comment: '' }

      // Задержка перед скрытием формы (15 секунд)
      setTimeout(() => {
        hasSubmitted.value = true
      }, 5000)
    } else {
      submitStatus.value = { type: 'error', message: 'Ошибка в отправке. Попробуйте позже' }
    }
  } catch {
    submitStatus.value = { type: 'error', message: 'Ошибка в отправке. Попробуйте позже' }
  } finally {
    isSubmitting.value = false
  }
}

function getGuestWord(count: number | undefined): string {
  if (!count) return '0 персон'

  if (count === 1) {
    return 'одни'
  }

  // Словарь числительных
  const numberWords: Record<number, string> = {
    2: 'двух', 3: 'трех', 4: 'четырех', 5: 'пяти',
    6: 'шести', 7: 'семи', 8: 'восьми', 9: 'девяти', 10: 'десяти',
    11: 'одиннадцати', 12: 'двенадцати', 13: 'тринадцати', 14: 'четырнадцати',
    15: 'пятнадцати', 16: 'шестнадцати', 17: 'семнадцати', 18: 'восемнадцати',
    19: 'девятнадцати', 20: 'двадцати'
  }

  if (count <= 20) {
    return `${numberWords[count]} персон`
  }

  // Для чисел больше 20
  return `${count} персон`
}

onMounted(() => {
  const saved = localStorage.getItem('wedding-form-submitted')
  if (saved) {
    try {
      const data = JSON.parse(saved)
      hasSubmitted.value = true
      submittedData.value = data
    } catch {
      localStorage.removeItem('wedding-form-submitted')
    }
  }
})
</script>

<template>
  <section class="presence-form section container container--text">
    <div class="presence-form__title">
      Присутствие
    </div>

    <!-- Если уже отправлял - показываем текст подтверждения -->
    <div  class="presence-form__confirmed">
      <p class="presence-form__text presence-form__text--confirmed">
        Вы уже подтвердили свое присутствие <strong>{{ submittedData?.name }}</strong>
        <br/>
        <br/>
        <template v-if="submittedData?.guest_count === 1">Вы сказали что придете, <strong>{{ getGuestWord(submittedData?.guest_count) }}.</strong></template>
        <template v-else>Вы сказали что придете, в количестве <strong>{{ getGuestWord(submittedData?.guest_count) }}.</strong></template>
      </p>
      <br/>
      <p class="presence-form__text">
        Если остались вопросы, пишите в наш
        <a href="https://t.me/weddingGA2026_bot" target="_blank">телеграмм бот</a>
      </p>
    </div>

    <!-- Если нет - показываем форму с приглашением -->
<!--    <template v-else>-->
<!--      <div class="presence-form__text presence-form__text&#45;&#45;padding">-->
<!--        <p>Пожалуйста, подтвердите ваше присутствие на нашем празднике до 1 апреля 2026 года-->
<!--          любым удобным для вас способом или заполните форму ниже:-->
<!--        </p>-->
<!--      </div>-->

<!--      <form class="presence-form__form" @submit.prevent="submitForm">-->
<!--      <input-->
<!--        v-model="formData.name"-->
<!--        name="name"-->
<!--        type="text"-->
<!--        class="presence-form__input"-->
<!--        placeholder="Имя и фамилия"-->
<!--      >-->

<!--      <input-->
<!--        v-model="formData.guest_count"-->
<!--        name="guest_count"-->
<!--        type="number"-->
<!--        class="presence-form__input"-->
<!--        placeholder="Кол-во персон"-->
<!--      >-->

<!--      <textarea-->
<!--        v-model="formData.comment"-->
<!--        name="comment"-->
<!--        class="presence-form__textarea"-->
<!--        placeholder="Оставь свой комментарий"-->
<!--      >-->
<!--      </textarea>-->

<!--      <p class="presence-form__text">Если еще остались вопросы напишите их в наш-->
<!--        <a href="https://t.me/weddingGA2026_bot" target="_blank">телеграмм</a>-->
<!--      </p>-->

<!--      <div v-if="submitStatus" class="presence-form__status" :class="`presence-form__status&#45;&#45;${submitStatus.type}`">-->
<!--        {{ submitStatus.message }}-->
<!--      </div>-->

<!--      <button class="presence-form__btn-submit" type="submit" :disabled="isSubmitting">-->
<!--        {{ isSubmitting ? 'Отправка...' : 'Отправить' }}-->
<!--      </button>-->
<!--    </form>-->
<!--    </template>-->

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

  &--padding {
    @include media.lg-up {
      padding-inline: 50px;
    }
  }

  a, strong {
    color: var(--c-primary);
    font-weight: 600;
  }
}

.presence-form__text--confirmed {
  border: 2px solid var(--c-primary);
  margin-inline: 10px;
  border-radius: 10px;

  @include media.lg-up {
    padding: 15px;
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

  @include media.lg-up {
    padding: 10px 30px 10px 10px;
  }
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
