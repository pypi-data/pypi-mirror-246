# cinemator
Command Line Tool for digging up all sort of medias

### Assumptions
 
1. Assumed that If someone knows the imdb id, they are looking for a specific medias details therefore that feature is not search but in get details.

2. OMDB API does not have extended documentation for python libraries ([omdb](https://pypi.org/project/omdb/) and [omdbapi](https://pypi.org/project/omdbapi/)) therefore used requests instead of using the dedicated libraries. Please see for further background; [linkedin blog](https://www.linkedin.com/pulse/rest-apis-python-documentation-lack-jim-kerick/)

3. Rotten Tomatoes details are no longer available at OMDB. I have included the feature to enable the information with a note that a future implementation can be done to retrieve it from fandango directly. I have requested api keys for this. Please see for further background; [omdb rating changes](https://www.patreon.com/posts/rating-changes-8417367), [where to get tomatoes info](https://developer.fandango.com/Rotten_Tomatoes)

4. Asummed that the API key will be passed from a local file for the security concerns. This would be a centralised secret management parameter if the service was deployed to production.

### Resources and Design Decisions
1. Used cookie cutter for project structure. [cookiecutter](https://cookiecutter.readthedocs.io/en/1.7.2/)
2. Used a tool using the cookie cutter to cut cli projects. [cli cutter](https://github.com/nvie/cookiecutter-python-cli)
3. Used requests for restful events as mentioned at Assumptions
4. The cli cookie cutter comes with "click". I would use click for a command line implemenetation in any case as it is most convenient cli implementation tool.Providing extensive options and configurations for arguments as well.
5. Mainly used unittest.mock for tests, avoided calling functions for real. 


# Setup And Configuration

###  API KEY 
In order to access to omdb api, you need to retrieve an api key. Please find the request page [here](http://www.omdbapi.com/apikey.aspx).

1. Update ```config.py``` with path to the api key file
## Initialize virtual machine and run the code
1. ```python3 -m venv venv```
2. ```source . venv/bin/activate```
3. make sure that you are at /cinemator/
4. ```make setup```  
5. ```ln -s path_to/cinemator/cinemat/__main__.py cinemator```

## CINEMATOR Commands
1. ```cinemator details``` gets the extended details for the sepcific media,
2. ```cinemator imdb``` gets the info for the specific imdb id ,
3. ```cinemator info``` gives information about the tool and the background,
4. ```cinemator search``` searches medias by keyword without specification,
5. ```cinemator type``` serches medias by type and title,
6. ```cinemator year``` searches medias by year and title

## MAKE Commands
1. ``` make clean``` to clean unnecessary files before commits
2. ```make lint``` to check linting with flake8
3. ``` make lint-fix``` to fix code with black
4. ```make setup``` to build and install the application