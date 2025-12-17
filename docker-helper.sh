RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

print_msg() {
    echo -e "${GREEN}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $1"
}

print_error() {
    echo -e "${RED}[$(date '+%Y-%m-%d %H:%M:%S')] ERROR:${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[$(date '+%Y-%m-%d %H:%M:%S')] WARNING:${NC} $1"
}

start() {
    print_msg "Запуск контейнерів..."
    docker-compose up -d
    print_msg "Контейнери запущені!"
    docker-compose ps
}

stop() {
    print_msg "Зупинка контейнерів..."
    docker-compose down
    print_msg "Контейнери зупинені!"
}

restart() {
    print_msg "Перезапуск контейнерів..."
    docker-compose restart
    print_msg "Контейнери перезапущені!"
}

logs() {
    docker-compose logs -f web
}

backup() {
    BACKUP_DIR="./backups"
    mkdir -p $BACKUP_DIR
    
    TIMESTAMP=$(date '+%Y%m%d_%H%M%S')
    BACKUP_FILE="$BACKUP_DIR/database_${TIMESTAMP}.db"
    
    print_msg "Створення backup бази даних..."
    docker-compose exec web cp /app/data/database.db /app/data/database_backup_${TIMESTAMP}.db
    docker cp flask_app:/app/data/database.db $BACKUP_FILE
    
    if [ -f "$BACKUP_FILE" ]; then
        print_msg "Backup успішно створено: $BACKUP_FILE"
        ls -lh $BACKUP_FILE
    else
        print_error "Помилка при створенні backup!"
        exit 1
    fi
}

restore() {
    if [ -z "$1" ]; then
        print_error "Необхідно вказати шлях до файлу backup!"
        echo "Використання: ./docker-helper.sh restore <путь_до_backup_файлу>"
        exit 1
    fi
    
    if [ ! -f "$1" ]; then
        print_error "Файл $1 не знайдено!"
        exit 1
    fi
    
    print_warning "Ви збираєтеся відновити базу даних з $1"
    read -p "Ви впевнені? (yes/no): " -r
    if [[ $REPLY =~ ^[Yy][Ee][Ss]$ ]]; then
        print_msg "Зупинка контейнеру..."
        docker-compose stop web
        
        print_msg "Копіювання backup файлу..."
        docker cp "$1" flask_app:/app/data/database.db
        
        print_msg "Запуск контейнеру..."
        docker-compose start web
        
        print_msg "База даних успішно відновлена!"
    else
        print_msg "Відновлення скасовано"
    fi
}

clean() {
    print_msg "Очищення невикористовуваних Docker ресурсів..."
    docker system prune -f
    print_msg "Очищення завершено!"
}

health() {
    print_msg "Статус контейнера:"
    docker ps --filter "name=flask_app" --format "table {{.Names}}\t{{.Status}}"
    
    print_msg "\nДеталі health check:"
    docker inspect flask_app | grep -A 10 "\"Health\""
}

exec_cmd() {
    if [ -z "$1" ]; then
        print_error "Необхідно вказати команду!"
        echo "Використання: ./docker-helper.sh exec <команда>"
        exit 1
    fi
    
    docker-compose exec web sh -c "$1"
}

stats() {
    print_msg "Статистика використання ресурсів контейнерів:"
    docker stats flask_app
}

help() {
    echo "Docker Helper скрипт для управління контейнерами"
    echo ""
    echo "Использование: ./docker-helper.sh <команда>"
    echo ""
    echo "Доступні команди:"
    echo "  start          - Запустити контейнери"
    echo "  stop           - Зупинити контейнери"
    echo "  restart        - Перезапустити контейнери"
    echo "  logs           - Переглянути логи в реальному часі"
    echo "  backup         - Створити backup бази даних"
    echo "  restore <file> - Відновити базу даних з backup"
    echo "  health         - Переглянути статус health check"
    echo "  stats          - Переглянути статистику ресурсів"
    echo "  clean          - Очистити невикористовувані ресурси"
    echo "  exec <cmd>     - Виконати команду в контейнері"
    echo "  help           - Вивести цю справку"
    echo ""
}

case "$1" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    restart)
        restart
        ;;
    logs)
        logs
        ;;
    backup)
        backup
        ;;
    restore)
        restore "$2"
        ;;
    health)
        health
        ;;
    stats)
        stats
        ;;
    clean)
        clean
        ;;
    exec)
        exec_cmd "$2"
        ;;
    help|--help|-h)
        help
        ;;
    *)
        print_error "Невідома команда: $1"
        echo ""
        help
        exit 1
        ;;
esac
