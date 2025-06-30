import { MessageType, ChatType, RoadmapType } from './types'

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
    messages: [
      { text: 'Доброго времени суток! Что вы хотели бы освоить?', isUser: false },
      { text: 'Хочу узнать про курсы по маркетингу.', isUser: true },
      { text: 'Какие конкретные навыки вы хотите освоить?', isUser: false },
    ],
  },
  {
    id: 2,
    name: 'Программирование',
    roadmapId: 2,
    messages: [
      { text: 'Доброго времени суток! Что вы хотели бы освоить?', isUser: false },
      { text: 'Python и JavaScript.', isUser: true },
      { text: 'Какие конкретные навыки вы хотите освоить?', isUser: false },
    ],
  },
  {
    id: 3,
    name: 'Дизайн',
    roadmapId: 3,
    messages: [
      { text: 'Доброго времени суток! Что вы хотели бы освоить?', isUser: false },
      { text: 'Расскажите про UX/UI.', isUser: true },
      { text: 'Какие конкретные навыки вы хотите освоить?', isUser: false },
    ],
  },
]

export const roadmaps: RoadmapType[] = [
    {
      id: 1,
      status: 'done',
      name: 'Roadmap 1',
      courses: [
        {
          id: 1,
          cover_url: '/assets/courseImage.png',
          title: 'Телеграм-боты на Python: продвинутый уровень',
          duration: 9,
          difficulty: 'hard',
          price: 3600,
          pupils_num: 1200,
          authors: 'Александр Данилов',
          rating: 4,
          url: '#course-1',
          progress: 1,
        },
        {
          id: 2,
          cover_url: '/assets/courseImage.png',
          title: 'Телеграм-боты на Python: продвинутый уровень',
          duration: 9,
          difficulty: 'hard',
          price: 3600,
          pupils_num: 1200,
          authors: 'Александр Данилов',
          rating: 4,
          url: '#course-1',
          progress: 0.5,
        },
      ],
    },
    {
      id: 2,
      status: 'current',
      name: 'Roadmap 2',
      courses: [
        {
          id: 1,
          cover_url: '/assets/courseImage.png',
          title: 'Телеграм-боты на Python: продвинутый уровень',
          duration: 9,
          difficulty: 'hard',
          price: 3600,
          pupils_num: 1200,
          authors: 'Александр Данилов',
          rating: 4,
          url: '#course-2',
          progress: 1,
        },
        {
          id: 2,
          cover_url: '/assets/courseImage.png',
          title: 'Телеграм-боты на Python: продвинутый уровень',
          duration: 9,
          difficulty: 'hard',
          price: 3600,
          pupils_num: 1200,
          authors: 'Александр Данилов',
          rating: 4,
          url: '#course-2',
          progress: 0.7,
        },
        {
          id: 3,
          cover_url: '/assets/courseImage.png',
          title: 'Телеграм-боты на Python: продвинутый уровень',
          duration: 9,
          difficulty: 'hard',
          price: 3600,
          pupils_num: 1200,
          authors: 'Александр Данилов',
          rating: 4,
          url: '#course-2',
          progress: 0,
        },
      ],
    },
    {
      id: 3,
      status: 'notNow',
      name: 'Роадмап 3',
      courses: [
        {
          id: 3,
          cover_url: '/assets/courseImage.png',
          title: 'Телеграм-боты на Python: продвинутый уровень',
          duration: 9,
          difficulty: 'hard',
          price: 3600,
          pupils_num: 1200,
          authors: 'Александр Данилов',
          rating: 4,
          url: '#course-3',
          progress: 0,
        },
      ],
    },
  ]
