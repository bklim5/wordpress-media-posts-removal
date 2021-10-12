# you can add more WP sites to be processed here as well
WP_CONFIG = {
    'site1': {
        'app_username': '## YOUR USERNAME HERE ##',
        'app_password': '## YOUR APP PASSWORD HERE ##',
        'domain': '## WP SITE DOMAIN HERE, eg: site1.com ##'
    },
    # 'site2': {
    #     'app_username': '## USERNAME HERE ##',
    #     'app_password': '## USER APP PASSWORD HERE ##',
    #     'app_url': 'https://site2.com/wp-json/wp/v2'
    # }
}

# eg: in each execution, we process/delete the posts between 97 days old to 90 days old
OLD_POSTS_DAY_THRESHOLD = 90
DELETE_DAYS_COUNT = 7