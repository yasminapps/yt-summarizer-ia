#!/bin/bash
gunicorn -w 4 -b 0.0.0.0:5005 app:app