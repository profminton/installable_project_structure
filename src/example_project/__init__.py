# It is not strictly necessary to have anything in here. However, this can let you "flatten" the project structure. Without this line you would have to do the following:
#
#     from example_project.main import function
#
# But instead you only have to do this:
#
#    from example_project import function
# 
# Best practice is to avoid using "import *" and actually list the items you want users to actually use
from example_project.main import CurveFitter, function, whocalled