To run the script:
1. First setup an application password for a user in WP Admin Panel.
2. Install the dependencies in `requirements.txt`
3. Update `config.py` with the WP Site info (domain, username and app password). You can specify multiple sites here to be processed.
    
    NOTE: Specifying the app password directly in the config file is NOT RECOMMENDED. You can use environment variable to pass the value into the script or if you are using AWS/GCP you are advised to use Parameter Store or Secret Manager instead.
4. Run the script `python remove_old_posts.py`