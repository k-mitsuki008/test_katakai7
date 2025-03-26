import sys
import os

parent_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_path + '/common')
sys.path.append(parent_path + '/common/cerberus')
