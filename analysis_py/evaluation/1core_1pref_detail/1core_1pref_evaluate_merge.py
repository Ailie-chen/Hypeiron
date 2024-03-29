import importlib

script1 = importlib.import_module('1core_1pref_evaluate_cs')
script2 = importlib.import_module('1core_1pref_evaluate_gap')
script3 = importlib.import_module('1core_1pref_evaluate_ligra')
script4 = importlib.import_module('1core_1pref_evaluate_spec')

script1.bingo_evaluate()
script2.bingo_evaluate()
script3.bingo_evaluate()
script4.bingo_evaluate()
