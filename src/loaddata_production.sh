#!/bin/bash
python manage.py loaddata 'core/fixtures/initial_data.yaml'
python manage.py loaddata yaml/EffectType.yaml
python manage.py loaddata yaml/Effect.yaml
python manage.py loaddata yaml/ItemType.yaml
python manage.py loaddata yaml/Item.yaml
python manage.py loaddata yaml/Items_UseEffects.yaml
python manage.py loaddata yaml/Items_HoldEffects.yaml
python manage.py loaddata yaml/Rarity.yaml
python manage.py loaddata yaml/Harvesting.yaml
python manage.py loaddata yaml/Formula.yaml
python manage.py loaddata yaml/Result.yaml
python manage.py loaddata yaml/Formulas_Effects.yaml
python manage.py loaddata yaml/Patent.yaml
python manage.py loaddata yaml/QuestionAnswer.yaml
python manage.py loaddata yaml/Production/ServerStatus.yaml
