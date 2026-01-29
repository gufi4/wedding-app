import { ref, computed, onUnmounted } from 'vue'
import { calculateCountdown, type CountdownTime } from '@/utils/countdown'

export function useCountdown(targetDate: Date) {
  const trigger = ref(Date.now())
  const updateInterval = 60 * 1000 // Update every minute

  // Calculate countdown
  const countdown = computed<CountdownTime>(() => {
    trigger.value // Establish reactive dependency
    return calculateCountdown(targetDate)
  })

  // Update timer
  let timer: ReturnType<typeof setInterval> | null = null

  const startTimer = () => {
    timer = setInterval(() => {
      trigger.value = Date.now()
    }, updateInterval)
  }

  const stopTimer = () => {
    if (timer) {
      clearInterval(timer)
      timer = null
    }
  }

  // Auto-start
  startTimer()

  // Auto-cleanup on unmount
  onUnmounted(() => {
    stopTimer()
  })

  return {
    countdown,
    startTimer,
    stopTimer
  }
}
