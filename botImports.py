from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
import os
import time
import random
import configparser
from utility_methods.utility_methods import *
import urllib.request
import pip._vendor.requests
import sys
from bs4 import BeautifulSoup
import pandas as pd
from pip._vendor import requests
import re