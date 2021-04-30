# Novel Public Health
Novel Public Health website written in Django.

## Quick Start
To get this project up and running locally on your computer:
1. Download [Python 3.9](https://www.python.org/downloads/).
2. Download [Git](https://git-scm.com/downloads).
3. Download the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli).
4. Install the database: [Postgres](https://devcenter.heroku.com/articles/heroku-postgresql#local-setup).
5. To run the webpage on your local server, we have added two files to simplify the process:
   - [local-testing.sh](local-testing.sh)    (For Macs)
   - [local-testing.bat](local-testing.bat)  (For Windows)
   
   Comments have been placed in both of the above scripts in order to tell you which commands are required.
   
   To run the shell script, open your terminal and type:
   ```
   sh local-testing.sh
   ```
   
   To run the batch file, in your terminal:
   ```
   .\local-testing.bat
   ```
3. Open a browser to `http://127.0.0.1:8000/` to see the site.
4. Open a browser to `http://127.0.0.1:8000/admin/` to see the admin site.

## Deploying to Heroku
When you want to make a change from your local site to the production site, you run the following Github commands in your terminal:
```
$ git add .
$ git commit -m "my commit"
$ git push origin main
```

What does each command do?
1. You first add your changes for Github to see what changes you have "staged" locally. 
   - To see all of your staged changes, you can run ```git status```.
   - If you want to delete all of your local changes, you would run ```git stash``` (there's no going back from stashing so be careful)
2. Next, you commit your staged changes to history.
3. Finally, you push your committed changes to the Github repo! 
   - We have automatically configured Heroku to detect any new pushed changes and build the production site.

Also, here's a helpful analogy describing the above git add, commit, and push commands taken from [this blog](https://dev.to/erikaheidi/stage-commit-push-a-git-story-comic-a37):
> Work on your postcard (implement your changes).
> 
> Put it on the "staged" pocket when you're ready to commit (git add).
> 
> Stamp the postcard (git commit).
> 
> When you're ready, put the postcard in the mailbox (git push).

## Production
**IMPORTANT:** After you push your changes to Github AND after the Heroku build has finished (usually takes a few minutes), you must run one of the following scripts:
   - [production.sh](production.sh)    (For Macs)
   - [production.bat](production.bat)  (For Windows)
      
   To run the shell script, open your terminal and type:
   ```
   sh production.sh
   ```
   
   To run the batch file, in your terminal:
   ```
   .\production.bat
   ```
However, you **only** need to do this whenever you have pushed any new migrations. The production database is different from the local database, so we migrate any new changes on the live site with this script.

## External Services
- [Heroku Novel Public Health Dashboard](https://dashboard.heroku.com/apps/novel-public-health)
   - See current builds in progress after pushing to Github.
   - Set config variables in settings. They must be similar to the local environment variables as seen in [locallibrary/.env](locallibrary/.env).
   - See data metrics and dynos cost.
- [AWS Bucket](https://s3.console.aws.amazon.com/s3/buckets/novel-public-health-media?region=us-east-2&tab=objects)
   - Contains movie and image uploads.
   - Serves all of our static files (HTML/CSS/JS).
- [Stripe Dashboard](https://dashboard.stripe.com/test/dashboard) 
   - Subscription payment plans and managing customers.
- [Bright Data Proxy Manager](https://brightdata.com/cp/dashboard) 
   - Searches Google Scholar for relevant research articles about a movie.

## Average Cost Estimate
### Live Production Site
```
+ $7.00  => HEROKU SERVER. Needed for running the production site at all times.
+ $0.02  => AWS BUCKET. ($0.023 per GB for 50 TB / Month). Right now, we're at about 0.5 GB.
            Of course, this cost will be greater when adding larger movie files.
+ $0.00  => STRIPE. Stripe's fees are on a per-transaction basis (2.9% + $0.30) for purchases.
+ $0.00  => BRIGHT DATA. Bright Data offers (0.01 GBs @ 0.6 $/GB), but for our purpose, it's basically free.
            Our team's usage over a few months hadn't reached a penny.
            Also, there's $6.00 in the account, so it should last for a very long time.
--------
~ $7.02 / month
```
Not included above, but also important, is that most domains will cost an average of $10 per year.
 - e.g., setting the domain to novelpublichealth.com instead of [novel-public-health.herokuapp.com](https://novel-public-health.herokuapp.com/).

**IMPORTANT:** Note that these costs are **only** for a running production site. If you're okay with not running the production site just yet, the local development can be free. All you'd have to do is the following:
1. Navigate to the Heroku app's [Resources page](https://dashboard.heroku.com/apps/novel-public-health/resources).
2. Under Hobby Dynos, click the pencil icon, and turn the switch off.
3. Now, your production site will not be functional, but your total cost per month will be about $0.02.
4. Whenever you'd like to have the production site working again, just flip that same switch!

## Further Documentation
For more information about using Python on Heroku, see these Dev Center articles:
- [Python on Heroku](https://devcenter.heroku.com/categories/python)
