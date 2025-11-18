# Звіт з лабораторної роботи 3

## Розробка базового вебпроєкту

### Інформація про команду
- Назва команди: Немає

- Учасники:
  - Кравчук Владислав Вікторович

## Завдання
3 лабораторна, створити свій вебзастосунок

### Обрана предметна область

Онлайн магазин побутової техніки.

### Реалізовані вимоги

Вкажіть, які рівні завдань було виконано:

- [Виконано] Рівень 1: Створено сторінки "Головна" та "Про нас"
- [Виконано] Рівень 2: Додано мінімум дві додаткові статичні сторінки з меню та адаптивною версткою

## Хід виконання роботи
Виконував завдання в рівнях
Якщо не знав щось то питав в ШІ

### Підготовка середовища розробки

Опишіть процес встановлення та налаштування:

- Python 3.14
- pip instal Flask
- git 2.51.2
### Структура проєкту

Наведіть структуру файлів та директорій вашого проєкту:

```
d:\OneDrive\site
├── temples
├── app.py
```

### Опис реалізованих сторінок
Головна-все про сайт
Про нас-про команду яка робила цей сайт(я один)
Магазин-вкладка де можна бьуде купувати техніку
Зворотній звязок-вкладка де є гмайл розробнрика
#### Головна сторінка

Головна-опис сфери сайту

#### Сторінка "Про нас"

Про нас-про команду яка робила цей сайт

#### Додаткові сторінки (якщо реалізовано)

Магазин- вкладка де можна купувати техніку
Зворотній звязок-вкладка де є гмайл розробника 

## Ключові фрагменти коду

### Маршрутизація в Flask

Наведіть приклад налаштування маршрутів у файлі `app.py`:

"/" — endpoint: home
"/about" — endpoint: about
"/services" — endpoint: services
"/contact" — endpoint: contact

```python
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')
```

### Базовий шаблон

Наведіть фрагмент базового шаблону `base.html`:

<!DOCTYPE html>
<html lang="uk" class="h-full">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Побутова техніка{% endblock %}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        .bar {
            transition: all 0.3s ease-in-out;
        }
    </style>
</head>
<body class="flex flex-col min-h-screen bg-gray-100 font-sans leading-normal tracking-normal">
    <header class="bg-gradient-to-r from-blue-600 to-indigo-700 text-white shadow-lg">
        <nav class="container mx-auto px-4 py-4">
            <div class="flex flex-wrap justify-between items-center">
                <a href="{{ url_for('home') }}" class="text-2xl font-bold hover:text-yellow-200 transition duration-400">Побутова техніка</a>
                
                <button id="menu-toggle" class="lg:hidden focus:outline-none" aria-label="Відкрити меню">
                    <div class="w-6 h-6 relative">
                        <span class="bar absolute h-0.5 w-6 bg-white transform transition duration-300 ease-in-out"></span>
                        <span class="bar absolute h-0.5 w-6 bg-white transform transition duration-300 ease-in-out mt-2"></span>
                        <span class="bar absolute h-0.5 w-6 bg-white transform transition duration-300 ease-in-out mt-4"></span>
                    </div>
                </button>
                
                <ul id="menu" class="hidden w-full lg:flex lg:w-auto lg:space-x-6 flex-col lg:flex-row mt-4 lg:mt-0">
                    <li><a href="{{ url_for('home') }}" class="block py-2 lg:py-0 hover:text-yellow-200 transition duration-300">Головна</a></li>
                    <li><a href="{{ url_for('shop.shop') }}" class="block py-2 lg:py-0 hover:text-blue-300 transition duration-300">Магазин</a></li>
                    <li><a href="{{ url_for('shop.cart') }}" class="block py-2 lg:py-0 hover:text-blue-300 transition duration-300">Кошик</a></li>
                    <li><a href="{{ url_for('about') }}" class="block py-2 lg:py-0 hover:text-blue-300 transition duration-300">Про нас</a></li>
                    <li><a href="{{ url_for('feedback.feedback') }}" class="block py-2 lg:py-0 hover:text-blue-300 transition duration-300">Зворотній зв'язок</a></li>
                    <li><a href="{{ url_for('accounts.accounts') }}" class="block py-2 lg:py-0 hover:text-blue-300 transition duration-300">Аккаунт</a></li>
                </ul>
            </div>
        </nav>
    </header>

    <main class="flex-grow container mx-auto px-4 py-8">
        <div class="bg-white shadow-md rounded-lg p-6">
            {% block content %}{% endblock %}
        </div>
    </main>

    <footer class="bg-gray-800 text-white py-4 mt-auto">
        <div class="container mx-auto px-4 text-center">
            <p>&copy; 2025 Онлайн магазин побутової техніки. Всі права захищені.</p>
        </div>
    </footer>

    <script>
        document.addEventListener('DOMContentLoaded', function() {
            const menuToggle = document.getElementById('menu-toggle');
            const menu = document.getElementById('menu');
            const bars = menuToggle.querySelectorAll('.bar');

            menuToggle.addEventListener('click', function() {
                menu.classList.toggle('hidden');
                menu.classList.toggle('lg:flex');
                bars[0].classList.toggle('rotate-45');
                bars[0].classList.toggle('translate-y-2');
                bars[1].classList.toggle('opacity-0');
                bars[2].classList.toggle('-rotate-45');
                bars[2].classList.toggle('-translate-y-2');
                
                if (menu.classList.contains('hidden')) {
                    menuToggle.setAttribute('aria-expanded', 'false');
                    menuToggle.setAttribute('aria-label', 'Відкрити меню');
                } else {
                    menuToggle.setAttribute('aria-expanded', 'true');
                    menuToggle.setAttribute('aria-label', 'Закрити меню');
                }
            });

            // Закриваємо меню при кліку поза ним на мобільних пристроях
            document.addEventListener('click', function(event) {
                if (window.innerWidth < 1024) { // lg breakpoint
                    const isClickInside = menu.contains(event.target) || menuToggle.contains(event.target);
                    if (!isClickInside && !menu.classList.contains('hidden')) {
                        menu.classList.add('hidden');
                        menu.classList.remove('lg:flex');
                        bars[0].classList.remove('rotate-45', 'translate-y-2');
                        bars[1].classList.remove('opacity-0');
                        bars[2].classList.remove('-rotate-45', '-translate-y-2');
                        menuToggle.setAttribute('aria-expanded', 'false');
                        menuToggle.setAttribute('aria-label', 'Відкрити меню');
                    }
                }
            });

            // Перевіряємо розмір вікна при завантаженні та зміні розміру
            function checkWindowSize() {
                if (window.innerWidth >= 1024) {
                    menu.classList.remove('hidden');
                    menu.classList.add('lg:flex');
                } else {
                    menu.classList.add('hidden');
                    menu.classList.remove('lg:flex');
                }
            }

            window.addEventListener('resize', checkWindowSize);
            checkWindowSize(); // Викликаємо функцію при завантаженні сторінки
        });
    </script>
</body>
</html>

## Розподіл обов'язків у команді

Опишіть внесок кожного учасника команди:

- Кравчук Владислав Вікторович - Зробив все

## Скріншоти

Додайте скріншоти основних сторінок вашого вебзастосунку:
(https://gruzavto.lviv.ua/wp-content/uploads/2020/08/100.png)
(https://images.mentoday.ru/upload/img_cache/6b1/6b176f2c459f8339dc71dd4b34f08011_ce_2000x1110x0x84_cropped_1200x628.jpg)
### Головна сторінка

{% extends "base.html" %} {% block title %}Головна{% endblock %} {% block
content %}
<h1 class="text-3xl font-bold mb-4">Ласкаво просимо на головну сторінку сайту "Побутова техніка"</h1>
<div class="grid grid-cols-1 md:grid-cols-2 gap-4">
    <div>
        <img
            src="https://gruzavto.lviv.ua/wp-content/uploads/2020/08/100.png"
            alt="Placeholder"
            class="w-full rounded-lg shadow-md"
        />
    </div>
    <div>
        <p class="text-lg">
            Тут ви знайдете широкий вибір побутової техніки для вашого дому. Від холодильників до пральних машин - в нас є все, що вам потрібно, щоб зробити ваше життя комфортнішим.
        </p>
    </div>
</div>
{% endblock %}

### Сторінка "Про нас"

{% extends "base.html" %} {% block title %}Про нас{% endblock %} {% block
content %}
<h1 class="text-3xl font-bold mb-4">Про нас</h1>
<div class="grid grid-cols-1 md:grid-cols-2 gap-4">
    <div>
        <p class="text-lg">
            Ми продаємо найкращу побутову техніку для вашого дому. Наша команда прагне забезпечити вас якісними продуктами та відмінним сервісом.
        </p>
    </div>

    <div>
        <img
            src="https://images.mentoday.ru/upload/img_cache/6b1/6b176f2c459f8339dc71dd4b34f08011_ce_2000x1110x0x84_cropped_1200x628.jpg"
            alt="Placeholder"
            class="w-full rounded-lg shadow-md"
        />
    </div>
</div>
{% endblock %}


### Додаткові сторінки



### Висновки

Опишіть:

- Що вдалося реалізувати успішно:Більшість
- З якими труднощами зіткнулися:
- Які навички та знання отримали:Навчився створювати сайт на базі хтмл та пайтон
- Які можливості для вдосконалення проєкту бачите:Збільшення директорії проекту

Очікувана оцінка: [8 балів]

Обґрунтування: [Написав більшість коду за допомогою штучного інтелекту]
