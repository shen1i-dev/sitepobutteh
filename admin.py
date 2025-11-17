from flask import Blueprint, render_template, render_template_string, request, redirect, url_for, flash
import models

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

base_admin = """
<!doctype html><html lang="uk"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Admin</title>
<link href="https://cdn.tailwindcss.com" rel="stylesheet">
</head><body class="bg-gray-50 min-h-screen">
<div class="container mx-auto p-6">
<a class="text-blue-600" href="/">Назад на сайт</a>
<h1 class="text-2xl font-bold mt-4">Адмін-панель</h1>
<div class="mt-4">
{{ body|safe }}
</div>
</div></body></html>
"""

@admin_bp.route("/")
def admin_index():
    body = """
    <ul class="list-disc pl-5">
        <li><a href="/admin/feedbacks" class="text-blue-600">Відгуки</a></li>
        <li><a href="/admin/clients" class="text-blue-600">Клієнти</a></li>
        <li><a href="/admin/services" class="text-blue-600">Послуги</a></li>
        <li><a href="/admin/service_orders" class="text-blue-600">Замовлення послуг</a></li>
    </ul>
    """
    return render_template_string(base_admin, body=body)

# Feedbacks
@admin_bp.route("/feedbacks")
def feedbacks():
    rows = models.get_feedbacks()
    items = "<h2 class='text-xl'>Відгуки</h2><ul class='mt-4'>"
    for r in rows:
        items += f"<li class='mb-3 p-3 bg-white rounded shadow'><b>{r[1]}</b> ({r[2]})<div class='text-sm text-gray-700'>{r[3]}</div><form method='post' action='/admin/feedbacks/delete/{r[0]}' class='mt-2'><button class='px-2 py-1 bg-red-500 text-white rounded'>Видалити</button></form></li>"
    items += "</ul>"
    return render_template_string(base_admin, body=items)

@admin_bp.route("/feedbacks/delete/<int:fid>", methods=["POST"])
def feedback_delete(fid):
    models.delete_feedback(fid)
    return redirect(url_for("admin.feedbacks"))


# Clients
@admin_bp.route("/clients", methods=["GET","POST"])
def clients():
    msg = ""
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        models.create_client(name, email, phone)
        msg = "<div class='text-green-600'>Клієнта додано</div>"
    rows = models.get_clients()
    body = "<h2 class='text-xl'>Клієнти</h2>" + msg
    body += "<form method='post' class='mt-3 mb-4 bg-white p-4 rounded shadow'><input name='name' placeholder='Імʼя' class='border p-2 w-full mb-2'><input name='email' placeholder='Email' class='border p-2 w-full mb-2'><input name='phone' placeholder='Телефон' class='border p-2 w-full mb-2'><button class='px-3 py-1 bg-blue-600 text-white rounded'>Додати клієнта</button></form>"
    for r in rows:
        body += f"<div class='p-3 bg-white rounded shadow mb-2'><b>{r[1]}</b> — {r[2]} — {r[3]}</div>"
    return render_template_string(base_admin, body=body)

# Services - HTML admin page
@admin_bp.route('/services', methods=['GET'])
def admin_services():
    services = models.get_services()
    body = "<h2 class='text-xl'>Послуги</h2>"
    body += "<form method='post' action='/admin/services/add' class='mt-3 mb-4 bg-white p-4 rounded shadow'><input name='name' placeholder='Назва послуги' class='border p-2 w-full mb-2' required><textarea name='description' placeholder='Опис' class='border p-2 w-full mb-2'></textarea><div class='flex gap-2'><input name='price' placeholder='Ціна' class='border p-2' required></div><button class='mt-2 px-3 py-1 bg-blue-600 text-white rounded'>Додати послугу</button></form>"
    for s in services:
        body += f"<div class='p-3 bg-white rounded shadow mb-2'><b>{s[1]}</b> — {s[3]} грн <div class='text-sm text-gray-600'>{s[2]}</div><form method='post' action='/admin/services/delete/{s[0]}' class='mt-2'><button class='px-2 py-1 bg-red-500 text-white rounded'>Видалити</button></form></div>"
    return render_template_string(base_admin, body=body)

@admin_bp.route('/services/add', methods=['POST'])
def admin_add_service():
    name = request.form.get('name')
    description = request.form.get('description')
    price = request.form.get('price', 0)
    try:
        sid = models.create_service(name, description, float(price))
        return redirect(url_for('admin.admin_services'))
    except Exception as e:
        return render_template_string(base_admin, body=f"<div class='text-red-600'>Помилка: {e}</div>")

@admin_bp.route('/services/delete/<int:service_id>', methods=['POST'])
def admin_delete_service(service_id):
    models.delete_service(service_id)
    return redirect(url_for('admin.admin_services'))

# Service orders - HTML admin page
@admin_bp.route('/service_orders', methods=['GET'])
def admin_service_orders():
    orders = models.get_service_orders()
    body = "<h2 class='text-xl'>Замовлення послуг</h2>"
    for o in orders:
        body += f"<div class='p-3 bg-white rounded shadow mb-3'><b>#{o[0]}</b> — Послуга: {o[2]} — К-сть: {o[3]} — Сума: {o[5]} грн — Статус: {o[8]}<div class='text-sm text-gray-600'>Замовник: {o[6] or '-'} {('('+o[7]+')') if o[7] else ''} — {o[9]}</div><form method='post' action='/admin/service_orders/{o[0]}/status' class='mt-2'><select name='status' class='border p-1'><option>new</option><option>processing</option><option>completed</option><option>cancelled</option></select><button class='ml-2 px-2 py-1 bg-green-600 text-white rounded'>Оновити</button></form></div>"
    return render_template_string(base_admin, body=body)

@admin_bp.route('/service_orders/<int:order_id>/status', methods=['POST'])
def admin_update_service_order_status(order_id):
    status = request.form.get('status', 'processing')
    models.update_service_order_status(order_id, status)
    return redirect(url_for('admin.admin_service_orders'))