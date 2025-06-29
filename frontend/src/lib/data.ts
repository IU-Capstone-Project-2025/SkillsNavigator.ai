import { MessageType, ChatType } from './types'

export const questions: MessageType[] = [
  { text: 'Доброго времени суток! Что вы хотели бы освоить?', isUser: false },
  { text: 'Какой у вас уже уровень?', isUser: false },
  { text: 'Какие конкретные навыки вы хотите освоить?', isUser: false },
]

export let chats: ChatType[] = [
  {
    id: 1,
    name: 'Маркетология',
    roadmapId: 1,
    chat: [
      { text: 'Доброго времени суток! Что вы хотели бы освоить?', isUser: false },
      { text: 'Хочу узнать про курсы по маркетингу.', isUser: true },
      { text: 'Какие конкретные навыки вы хотите освоить?', isUser: false },
    ],
  },
  {
    id: 2,
    name: 'Программирование',
    roadmapId: 2,
    chat: [
      { text: 'Доброго времени суток! Что вы хотели бы освоить?', isUser: false },
      { text: 'Python и JavaScript.', isUser: true },
      { text: 'Какие конкретные навыки вы хотите освоить?', isUser: false },
    ],
  },
  {
    id: 3,
    name: 'Дизайн',
    roadmapId: 3,
    chat: [
      { text: 'Доброго времени суток! Что вы хотели бы освоить?', isUser: false },
      { text: 'Расскажите про UX/UI.', isUser: true },
      { text: 'Какие конкретные навыки вы хотите освоить?', isUser: false },
    ],
  },
]
