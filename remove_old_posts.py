import pytz
import base64
import requests
from datetime import datetime, timedelta
from config import WP_CONFIG, OLD_POSTS_DAY_THRESHOLD, DELETE_DAYS_COUNT


class WordPressMediaPostsRemoval():
    def __init__(self, site_domain, app_username, app_password):
        self.app_username = app_username
        self.app_password = app_password
        self.wp_url = f'https://{site_domain}/wp-json/wp/v2'
        self.auth_headers = self.generate_authorization_headers()

    def generate_authorization_headers(self):
        """Generate the basic authorization headers in dictionary form

        Returns:
            [dictionary]: Authorization as key and its corresponding encoded basic auth value
        """
        concatenate_str = f'{self.app_username}:{self.app_password}'
        token = base64.b64encode(concatenate_str.encode('utf-8'))
        headers = {'Authorization': f"Basic {token.decode('utf-8')}"}
        return headers

    def fetch_posts(self, published_from_date, published_to_date):
        """Return the list of detailed posts information between the from date and to date

        Args:
            published_from_date ([string]): To filter the articles since this date
            published_to_date ([string]): To filter the articles before this date

        Returns:
            [list]: List of posts
        """
        url = f'{self.wp_url}/posts?status=publish&per_page=100&after={published_from_date}&before={published_to_date}'

        all_posts = []
        print(f'Getting posts from {published_from_date} to {published_to_date}..')
        req = requests.get(url, headers=self.auth_headers)
        total_pages = int(req.headers['X-WP-TotalPages'])
        print(f'Total pages: {total_pages}')
        all_posts = req.json()

        for page in range(2, total_pages + 1):
            print(f'Getting posts, page: {page}')
            req = requests.get(f'{url}&page={page}', headers=self.auth_headers)
            all_posts.extend(req.json())

        print(f'Total number of posts: {len(all_posts)}')

        return all_posts

    def delete_media(self, media_id):
        """Delete the media from WordPress site given the media ID

        Args:
            media_id ([int]): Media ID
        """
        try:
            print(f'Deleting media ID: {media_id}')
            url = f'{self.wp_url}/media/{media_id}?force=true'
            del_req = requests.delete(url, headers=self.auth_headers)
            if del_req.status_code != 200:
                raise Exception(del_req.status_code)

            print(f'Deleted media ID: {media_id}')
        except Exception as e:
            print(f'Error deleting media {media_id}, error code: {str(e)}')

    
    def delete_posts(self):
        """Delete the media and posts between a specified start and end date

        Returns:
            [int, int]: Number of deleted posts and error posts
        """
        deleted_posts_count, error_posts_count = 0, 0
        published_from_date = (datetime.now() - timedelta(days=OLD_POSTS_DAY_THRESHOLD + DELETE_DAYS_COUNT)).astimezone(pytz.utc).strftime('%Y-%m-%dT%H:%M:%S')
        published_to_date = (datetime.now() - timedelta(days=OLD_POSTS_DAY_THRESHOLD)).astimezone(pytz.utc).strftime('%Y-%m-%dT%H:%M:%S')
        posts = self.fetch_posts(published_from_date, published_to_date)

        for index, post in enumerate(posts):
            post_id = post['id']
            try:
                print(f'======= Processing post {index}, post ID: {post_id} =======')
                print(f'Deleting post ID: {post_id}')
                # Remove featured media associated to the post
                media_id = post.get('featured_media')
                if media_id:
                    self.delete_media(media_id)

                url = f'{self.wp_url}/posts/{post_id}?force=true'
                del_req = requests.delete(url, headers=self.auth_headers)
                if del_req.status_code != 200:
                    raise Exception(del_req.status_code)

                print(f'Deleted post ID: {post_id}')
                deleted_posts_count += 1

            except Exception as e:
                print(f'Error deleting post {post_id}, error code: {str(e)}')
                error_posts_count += 1

        return deleted_posts_count, error_posts_count



if __name__ == '__main__':
    for site, site_value in WP_CONFIG.items():
        print(f'======= Processing {site} =======')
        wp_removal_instance = WordPressMediaPostsRemoval(site_value['domain'], site_value['app_username'], site_value['app_password'])
        deleted_posts_count, error_posts_count = wp_removal_instance.delete_posts()
        print(f'Site: {site} - Removed a total of {deleted_posts_count} posts. {error_posts_count} posts having issue removing.')
