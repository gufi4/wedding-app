interface PlanItem {
  icon: string
  title: string
  time?: string
  desc?: string
}

export const planItems: PlanItem[] = [
  {
    icon: '/assets/wedding.svg',
    title: 'Выкуп',
    time: '10:30',
    desc: 'Встречаемся у невесты'
  },
  {
    icon: '/assets/wedding-rings.svg',
    title: 'Бракосочетание',
    time: '12:00',
    desc: 'Встречаемся у ЗАГСА'
  },
  {
    icon: '/assets/dinner.svg',
    title: 'Кафе',
    time: '15:00',
    desc: 'Встречаемся в кафе'
  },
  {
    icon: '/assets/wedding-cake.svg',
    title: 'Торт',
    time: '19:30',
  },
]
