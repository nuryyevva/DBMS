import log
import users

if __name__ == "__main__":
    log.log_filter('log.csv', 'utf-8')
    users.users_filter('users.csv', 'koi8_r')