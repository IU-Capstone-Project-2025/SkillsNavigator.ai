# 🌐 Frontend (Vite + React + TypeScript)

Этот проект использует [Vite](https://vitejs.dev/) как сборщик, [pnpm](https://pnpm.io/) как пакетный менеджер, и настроен для разработки с TypeScript, ESLint, Prettier, Stylelint и Husky.

---

## 📁 Структура

```
frontend/
├── public/                    # Статические ресурсы (favicon, иконки и т.д.)
├── src/                       # Исходный код приложения (React-компоненты, стили, утилиты)
├── .gitignore                 # Игнорируемые файлы Git
├── .lintstagedrc.yml          # Настройки для lint-staged
├── .prettierrc.yml            # Настройки Prettier
├── .stylelintrc.yml           # Настройки Stylelint
├── Dockerfile                 # Docker-инструкция для деплоя
├── eslint.config.js           # Конфигурация ESLint
├── index.html                 # Главный HTML-шаблон
├── package.json               # Скрипты, зависимости и метаданные проекта
├── pnpm-lock.yaml             # Лок-файл зависимостей pnpm
├── README.md                  # Документация (ты читаешь её сейчас)
├── tsconfig.app.json          # TypeScript-конфиг для приложения
├── tsconfig.json              # Базовый TS-конфиг
├── tsconfig.node.json         # TS-конфиг для Node-окружения (например, скриптов или конфига)
└── vite.config.ts             # Конфигурация Vite
```

---

## 🚀 Скрипты

Скрипты доступны через `pnpm run <script>` (или `pnpm <script>` для краткой формы):

| Скрипт         | Описание |
|----------------|----------|
| `dev`          | Запускает Vite Dev Server для разработки по адресу `http://localhost:5173`. Автоматически обновляется при изменении кода. |
| `build`        | Собирает TypeScript-проект и генерирует production-сборку через Vite. Результат сохраняется в `dist/`. |
| `preview`      | Локально запускает production-сборку (`dist/`) как бы она выглядела на сервере. Удобно для финального теста. |
| `lint`         | Запускает ESLint с кэшем, проверяя весь проект. |
| `types`        | Проверяет типы с помощью TypeScript для `tsconfig.json` и `tsconfig.node.json`. Ничего не компилирует. |
| `stylelint`    | Запускает Stylelint для проверки SCSS-стилей. |
| `stylecheck`   | Быстро обновляет кэш SCSS-файлов через `sass` (возможно используется для CI или предпросмотра). |
| `prettify`     | Применяет Prettier ко всему коду и сохраняет изменения в файлах. |

---

## 💻 Как запустить проект

### ▶️ Для разработки:
```bash
pnpm install     # Установить зависимости
pnpm dev         # Запуск dev-сервера (http://localhost:5173)
```

### 🏁 Для продакшена:
```bash
pnpm build       # Собирает проект в dist/
pnpm preview     # Предпросмотр продакшн-сборки (http://localhost:4173)
```

---

## 🧪 Проверка кода

Проверка качества и форматирования:
```bash
pnpm lint        # ESLint
pnpm stylelint   # Stylelint для стилей
pnpm types       # Проверка типов
pnpm prettify    # Автоформатирование кода
```

---

## Документация по инструментам:
> - [Vite](https://vitejs.dev/)
> - [React](https://react.dev/)
> - [TypeScript](https://www.typescriptlang.org/)
> - [pnpm](https://pnpm.io/)
> - [ESLint](https://eslint.org/)
> - [Prettier](https://prettier.io/)
> - [Stylelint](https://stylelint.io/)
> - [Husky](https://typicode.github.io/husky/)
