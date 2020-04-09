# 此文件用于发送页面

from django.http import HttpResponseRedirect
from showproject.models import *
from django.shortcuts import render
from showproject.connect import *
import datetime