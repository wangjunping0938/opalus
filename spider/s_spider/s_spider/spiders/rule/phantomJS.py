#!/bin/env python
# -*- coding: utf-8 -*-
import re
import os
from selenium import webdriver
import sys

#调用浏览器
def browser():
	js = re.sub(r'\n','',os.popen('which phantomjs').read())
	log_path = os.path.dirname(os.path.abspath('..'))  + '/log/logfile'
	browser = webdriver.PhantomJS(executable_path = js,service_log_path = log_path)
	return browser
