export interface CountdownTime {
  months: number
  days: number
  hours: number
  minutes: number
  isComplete: boolean
}

/**
 * Calculate time remaining until target date
 * @param targetDate - The wedding date
 * @returns Object with months, days, hours, minutes remaining
 */
export function calculateCountdown(targetDate: Date): CountdownTime {
  const now = new Date()
  const diff = targetDate.getTime() - now.getTime()

  if (diff <= 0) {
    return {
      months: 0,
      days: 0,
      hours: 0,
      minutes: 0,
      isComplete: true
    }
  }

  // Calculate months (approximate)
  let months = 0
  let tempDate = new Date(now)

  while (tempDate < targetDate) {
    const nextMonth = new Date(tempDate)
    nextMonth.setMonth(tempDate.getMonth() + 1)
    if (nextMonth <= targetDate) {
      months++
      tempDate = nextMonth
    } else {
      break
    }
  }

  // Calculate remaining time after months
  const remainingDiff = targetDate.getTime() - tempDate.getTime()

  // Convert remaining milliseconds to days, hours, minutes
  const days = Math.floor(remainingDiff / (1000 * 60 * 60 * 24))
  const hours = Math.floor((remainingDiff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60))
  const minutes = Math.floor((remainingDiff % (1000 * 60 * 60)) / (1000 * 60))

  return {
    months,
    days,
    hours,
    minutes,
    isComplete: false
  }
}
