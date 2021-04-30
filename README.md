# Novel Public Health
Novel Public Health website written in Django.

## Quick Start
To get this project up and running locally on your computer:
1. Download [Python 3.9](https://www.python.org/downloads/).
2. Download [Git](https://git-scm.com/downloads).
3. Download the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli).
4. To run the webpage on your local server, we have added two files to simplify the process:
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
**IMPORTANT**
After you push your changes to Github AND after the Heroku build has finished (usually takes a few minutes), you must run one of the following scripts:
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

## Further Documentation
For more information about using Python on Heroku, see these Dev Center articles:
- [Python on Heroku](https://devcenter.heroku.com/categories/python)
