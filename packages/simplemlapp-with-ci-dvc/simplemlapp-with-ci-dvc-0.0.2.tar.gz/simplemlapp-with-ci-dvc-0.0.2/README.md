mkdir simple_app

create environment

```bash
conda create -n wineq python=3.7 -y
```

activate the environment

```bash
conda activate wineq
```

create a requirements.txt file

```bash
touch requirements.txt
```

install dependencies by adding below dependencies
==>dvc
==>dvc[gdrive]
==>scikit-learn

```bash
pip install -r requirements.txt 
```

```bash
touch README.md
```

```bash
touch template.py
```


download the data from
https://drive.google.com/drive/folders/18zqQiCJVgF7uzXgfbIJ-04zgz1ItNfF5?usp=sharing


```bash
git init
```

```bash
dvc init
```

```bash
dvc add data_given/winequality.csv
```

```bash
git add . && git commit -m "first commit" 
```

create a new github repo
```bash
git branch -M main
git remote add origin https://github.com/shashiKumar14/simple-dvc-demo.git
```
```bash
git push -u origin main
```

================================================================

# coding part

1)In params.yaml file add the input parameters and the output parameters and input/output paths

2)Create get_data.py in simplemlapp-with-ci-dvc folder . It reads params from param.yaml file & process and returns the dataframe

3)Create load_data.py in simplemlapp-with-ci-dvc folder . It gets the data from get_data.py in simplemlapp-with-ci-dvc folder . using the functions it calls and stores the csv into data/raw folder.

4)In dvc.yaml file add the first stage.It has cmd,input dependencies,output paths

5)dvc repro

6)Create split_data.py in simplemlapp-with-ci-dvc folder . It reads params from param.yaml file then takes the data from raw folder and splits it into train and test and then inserts it into processed folder.

7)continue 4th and 5th step

8)create train_and_evaluate.py in simplemlapp-with-ci-dvc folder . It reads params from param.yaml file and takes the data from processed folder and it trains and evaluates the data 

9)continue 4th and 5th step

10)install necessary dependencies if any like tox,pytest

11)create tox.ini file e.x: touch tox.ini

12)create tests folder and create inside __init__.py,conftest.py,test_config.py 

13)To run the test cases command is : pytest -v .
==>inthis code writing the test cases in test_config.py .For the functions have to use  prefixed with "test_" 

14)To run tox command -
```bash
tox
```
15)for rebuilding -
```bash
tox -r
```

16)touch setup.py and 

```bash
pip install -e .
```

To freeze the dependencies which are installed.
```bash
pip freeze
```

build your own package commands-

```bash
python setup.py sdist bdist_wheel
```
```bash
pip install jupyterlab
```

To open the notebook using command
```bash
jupyter-lab notebooks
```

==>flake8 is the automatically chages the based on PEP8 standards.

==>we can do by manually by using the right click on the file and click format this document.

mkdir -p prediction_service/model

mkdir webapp

touch app.py

mkdir -p webapp/static/css

mkdir -p webapp/static/script

touch webapp/static/css/main.css

touch webapp/static/css/index.js

mkdir webapp/templates

touch webapp/templates/index.html

touch webapp/templates/404.html

touch webapp/templates/base.html

adding the code in main.css,404.html,index.html,base.html

we have base.html one but as many as we can  add index.html

add flask,gunicorn in requirements.txt

add the code in app.py

cp saved_models/model.joblib  prediction_service/model/

cp notebooks/schema.json prediction_service/

mkdir -p .github/workflows

touch .github/workflows/ci-cd.yaml

add the codec in ci-cd.yaml file

whenever we commit the code the .github/workflows/  triggers in github Actions

===============================================================================

create heroku application keys insert it into secrets in github
when we commit the code it deploys

===============================================================================

















