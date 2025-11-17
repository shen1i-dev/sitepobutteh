from flask import Flask, render_template_string, url_for, request, redirect, jsonify
from markupsafe import Markup
import models

# Імпортуємо адмін-блюпринт з папки routes
from routes.admin import admin_bp

app = Flask(__name__)
app.register_blueprint(admin_bp, url_prefix="/admin")

# Базовий шаблон з Tailwind CDN та простим адаптивним меню
base_template = """
<!doctype html>
<html lang="uk">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <script src="https://cdn.tailwindcss.com"></script>
    <title>{{ title }} — Проєкт</title>
</head>
<body class="min-h-screen bg-gray-50 text-gray-800">
    <header class="bg-white shadow">
        <div class="container mx-auto px-4 py-4 flex items-center justify-between">
            <a href="{{ url_for('home') }}" class="text-xl font-semibold">Онлайн послуги</a>
            <nav class="hidden md:flex space-x-4">
                <a href="{{ url_for('home') }}" class="px-3 py-2 rounded {{ 'bg-gray-200' if active=='home' else 'hover:bg-gray-100' }}">Головна</a>
                <a href="{{ url_for('about') }}" class="px-3 py-2 rounded {{ 'bg-gray-200' if active=='about' else 'hover:bg-gray-100' }}">Про нас</a>
                <a href="{{ url_for('services') }}" class="px-3 py-2 rounded {{ 'bg-gray-200' if active=='services' else 'hover:bg-gray-100' }}">Послуги</a>
                <a href="{{ url_for('contact') }}" class="px-3 py-2 rounded {{ 'bg-gray-200' if active=='contact' else 'hover:bg-gray-100' }}">Контакти</a>
            </nav>
            <div class="md:hidden">
                <button id="menuBtn" class="p-2 rounded bg-gray-100">Меню</button>
            </div>
        </div>
        <div id="mobileMenu" class="md:hidden hidden bg-white border-t">
            <div class="px-4 py-2 flex flex-col">
                <a href="{{ url_for('home') }}" class="py-2 {{ 'font-semibold' if active=='home' else '' }}">Головна</a>
                <a href="{{ url_for('about') }}" class="py-2 {{ 'font-semibold' if active=='about' else '' }}">Про нас</a>
                <a href="{{ url_for('services') }}" class="py-2 {{ 'font-semibold' if active=='services' else '' }}">Послуги</a>
                <a href="{{ url_for('contact') }}" class="py-2 {{ 'font-semibold' if active=='contact' else '' }}">Контакти</a>
            </div>
        </div>
    </header>

    <main class="container mx-auto px-4 py-8">
        {{ content|safe }}
    </main>

    <footer class="bg-white border-t mt-12">
        <div class="container mx-auto px-4 py-6 text-sm text-gray-600">
            © 2025 Онлайн послуги — навчальний вебзастосунок. Репозиторій із кодом додається до звіту.
        </div>
    </footer>

    <script>
        // Простий мобільний toggle меню
        document.getElementById('menuBtn')?.addEventListener('click', function(){
            const m = document.getElementById('mobileMenu');
            if (m) m.classList.toggle('hidden');
        });
    </script>
</body>
</html>
"""

# Утиліта для швидкого рендерингу сторінки
def render_page(title, active, content_html):
        return render_template_string(base_template, title=title, active=active, content=Markup(content_html))

@app.route("/")
def home():
        content = """
        <section class="grid gap-6 md:grid-cols-2 items-center">
            <div>
                <h1 class="text-3xl font-bold mb-3">Вітання на Головній сторінці</h1>
                <p class="text-gray-700 mb-4">Цей навчальний проєкт демонструє просту структуру Flask-застосунку з адаптивним інтерфейсом.
                Область: освітні онлайн-послуги.</p>
                <ul class="list-disc pl-5 text-gray-700">
                    <li>Курси програмування</li>
                    <li>Індивідуальні консультації</li>
                    <li>Матеріали для самостійного вивчення</li>
                </ul>
            </div>
            <div class="bg-gradient-to-br from-blue-50 to-white p-6 rounded shadow">
                <img src="https://lviv1256.com/wp-content/uploads/2018/02/3c99a63cf81c3449bf7199e7af36599a.jpg" alt="learning" class="w-full rounded">
            </div>
        </section>
        """
        return render_page("Головна", "home", content)

@app.route("/about")
def about():
        content = """
        <article class="prose lg:prose-xl">
            <h1>Про нас</h1>
            <p>Ми — команда студентів, яка створює навчальні ресурси з програмування. Мета — доступно пояснювати складні речі і надихати на практику.</p>
            <h2>Наша місія</h2>
            <p>Підвищити рівень цифрової грамотності та допомогти освоїти сучасні інструменти веб-розробки.</p>
        </article>
        """
        return render_page("Про нас", "about", content)

@app.route("/services")
def services():
        content = """
        <section>
            <h1 class="text-2xl font-semibold mb-4">Послуги</h1>
            <div class="grid gap-4 md:grid-cols-3">
                <div class="p-4 bg-white rounded shadow">
                    <h3 class="font-medium">Курси</h3>
                    <p class="text-sm text-gray-600">Структуровані курси з Python, Flask та фронтенду.</p>
                </div>
                <div class="p-4 bg-white rounded shadow">
                    <h3 class="font-medium">Менторство</h3>
                    <p class="text-sm text-gray-600">Індивідуальні сесії з розбором проєктів та код-ревью.</p>
                </div>
                <div class="p-4 bg-white rounded shadow">
                    <h3 class="font-medium">Ресурси</h3>
                    <p class="text-sm text-gray-600">Збірки матеріалів, шаблони проєктів та практичні завдання.</p>
                </div>
            </div>
        </section>
        """
        return render_page("Послуги", "services", content)

@app.route("/contact")
def contact():
        content = """
        <section class="max-w-lg">
            <h1 class="text-2xl font-semibold mb-3">Контакти</h1>
            <p class="mb-4 text-gray-700">Зв'яжіться з командою за електронною поштою або через репозиторій.</p>
            <ul class="text-gray-700">
                <li><strong>Email:</strong> vladkravchuk1303@gmail.com</li>
                <li><strong>GitHub:</strong> <a class="text-blue-600" href="https://github.com/shen1i-dev" target="_blank">Github розробника сайту</a></li>
            </ul>

            <h2 class="text-xl mt-6">Залишити відгук</h2>
            <form action="/feedback" method="post" class="mt-3">
                <input name="name" placeholder="Ім'я" class="border p-2 w-full mb-2" required>
                <input name="email" placeholder="Email" class="border p-2 w-full mb-2" required>
                <textarea name="message" placeholder="Ваш відгук" class="border p-2 w-full mb-2" required></textarea>
                <button class="px-3 py-2 bg-blue-600 text-white rounded">Надіслати</button>
            </form>
        </section>
        """
        return render_page("Контакти", "contact", content)

# Новий маршрут для обробки форми відгуків
@app.route("/feedback", methods=["POST"])
def feedback_submit():
    name = request.form.get("name")
    email = request.form.get("email")
    message = request.form.get("message")
    models.create_feedback(name, email, message)
    return render_page("Дякуємо", "contact", "<p class='text-green-700'>Дякуємо за відгук — він надійшов.</p>")

@app.route('/services', methods=['GET'])
def services_list():
    services = models.get_services()
    return jsonify([{"id": s[0], "name": s[1], "description": s[2], "price": s[3]} for s in services])

@app.route('/services/order', methods=['POST'])
def services_order():
    data = request.form or request.get_json() or {}
    service_id = int(data.get('service_id') or 0)
    quantity = int(data.get('quantity') or 1)
    name = data.get('name')
    email = data.get('email')
    try:
        order_id = models.create_service_order(service_id, quantity, None, name, email)
        return jsonify({"order_id": order_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
        # Ініціалізація БД (створить db.sqlite)
        models.init_db()
        # Режим розробки, порт можна змінити
        app.run(debug=True, host="0.0.0.0", port=8000)