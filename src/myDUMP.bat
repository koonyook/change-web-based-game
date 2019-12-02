python manage.py dumpdata auth.user --format yaml --indent 2 > myYAML/User.yaml
python manage.py dumpdata core.Player --format yaml --indent 2 > myYAML/Player.yaml
python manage.py dumpdata core.Ownership --format yaml --indent 2 > myYAML/Ownership.yaml